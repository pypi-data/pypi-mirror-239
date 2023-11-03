""" Qblox Cluster QRM-RF driver."""

import json

import numpy as np
from qblox_instruments.qcodes_drivers.cluster import Cluster as QbloxCluster
from qblox_instruments.qcodes_drivers.qcm_qrm import QcmQrm as QbloxQrmQcm
from qibo.config import log

from qibolab.instruments.abstract import Instrument
from qibolab.instruments.qblox.port import (
    ClusterRF_OutputPort,
    ClusterRF_OutputPort_Settings,
    QbloxInputPort,
    QbloxInputPort_Settings,
)
from qibolab.instruments.qblox.q1asm import (
    Block,
    Register,
    convert_phase,
    loop_block,
    wait_block,
)
from qibolab.instruments.qblox.sequencer import Sequencer, WaveformsBuffer
from qibolab.instruments.qblox.sweeper import QbloxSweeper, QbloxSweeperType
from qibolab.pulses import Pulse, PulseSequence, PulseShape, PulseType
from qibolab.sweeper import Parameter, Sweeper, SweeperType


class ClusterQRM_RF_Settings:
    def __init__(self, ports=None):
        if not ports:
            ports: dict = {
                "o1": ClusterRF_OutputPort_Settings(),
                "i1": QbloxInputPort_Settings(),
            }
        self.ports = ports


class ClusterQRM_RF(Instrument):
    """Qblox Cluster Qubit Readout Module RF driver.

    Qubit Readout Module RF (QRM-RF) is an instrument that integrates an arbitrary wave generator, a digitizer,
    a local oscillator and a mixer. It has one output and one input port. Each port has a path0 and path1 for the
    i(in-phase) and q(quadrature) components of the RF signal. The sampling rate of its ADC/DAC is 1 GSPS.
    https://www.qblox.com/cluster

    The class aims to simplify the configuration of the instrument, exposing only those parameters most frequently
    used and hiding other more complex settings.

    A reference to the underlying `qblox_instruments.qcodes_drivers.qcm_qrm.QRM_QCM` object is provided via the
    attribute `device`, allowing the advanced user to gain access to the features that are not exposed directly
    by the class.

    In order to accelerate the execution, the instrument settings are cached, so that the communication with the
    instrument only happens when the parameters change. This caching is done with the method
    `_set_device_parameter(target, *parameters, value)`.

    .. code-block:: text

        ports:
            o1:                                             # output port settings
                channel                     : L3-25a
                attenuation                 : 30                # (dB) 0 to 60, must be multiple of 2
                lo_enabled                  : true
                lo_frequency                : 6_000_000_000     # (Hz) from 2e9 to 18e9
                gain                        : 1                 # for path0 and path1 -1.0<=v<=1.0
            i1:                                             # input port settings
                channel                     : L2-5a
                acquisition_hold_off        : 130               # minimum 4ns
                acquisition_duration        : 1800

        classification_parameters:
            0: # qubit id
                rotation_angle              : 0                 # in degrees 0.0<=v<=360.0
                threshold                   : 0                 # in V
            1:
                rotation_angle              : 194.272
                threshold                   : 0.011197
            2:
                rotation_angle              : 104.002
                threshold                   : 0.012745

    Attributes:
        name (str): A unique name given to the instrument.
        address (str): IP_address:module_number; the IP address of the cluster and
            the module number.
        device (QbloxQrmQcm): A reference to the underlying `qblox_instruments.qcodes_drivers.qcm_qrm.QcmQrm` object.
            It can be used to access other features not directly exposed by this wrapper.
            https://qblox-qblox-instruments.readthedocs-hosted.com/en/master/api_reference/qcm_qrm.html

        ports = A dictionary giving access to the input and output ports objects.

            - ports['o1']: Output port
            - ports['i1']: Input port

            - ports['o1'].channel (int | str): the id of the refrigerator channel the output port o1 is connected to.
            - ports['o1'].attenuation (int): (mapped to qrm.out0_att) Controls the attenuation applied to the output
              port. It must be a multiple of 2.
            - ports['o1'].lo_enabled (bool): (mapped to qrm.out0_in0_lo_en) Enables or disables the local oscillator.
            - ports['o1'].lo_frequency (int): (mapped to qrm.out0_in0_lo_freq) Sets the frequency of the local oscillator.
            - ports['o1'].gain (float): (mapped to qrm.sequencers[0].gain_awg_path0 and qrm.sequencers[0].gain_awg_path1)
              Sets the gain on both paths of the output port.
            - ports['o1'].hardware_mod_en (bool): (mapped to qrm.sequencers[0].mod_en_awg) Enables pulse modulation
              in hardware. When set to False, pulse modulation is done in software, at the host computer, and the
              modulated pulse waveform is uploaded to the instrument. When set to True, the envelope of the pulse
              is uploaded to the instrument and it is modulated in real time by the FPGA of the instrument, using
              the sequencer nco (numerically controlled oscillator).
            - ports['o1'].nco_freq (int): (mapped to qrm.sequencers[0].nco_freq). Mapped, but not configurable from
              the runcard.
            - ports['o1'].nco_phase_offs = (mapped to qrm.sequencers[0].nco_phase_offs). Mapped, but not configurable
              from the runcard.

            - ports['i1'].channel (int | str): the id of the refrigerator channel the input port o1 is connected to.
            - ports['i1'].acquisition_hold_off (int): Delay between the moment the readout pulse starts to be played and
              the start of the acquisition, in ns. It must be > 0 and multiple of 4.
            - ports['i1'].acquisition_duration (int): (mapped to qrm.sequencers[0].integration_length_acq) Duration
              of the pulse acquisition, in ns. It must be > 0 and multiple of 4.
            - ports['i1'].hardware_demod_en (bool): (mapped to qrm.sequencers[0].demod_en_acq) Enables demodulation
              and integration of the acquired pulses in hardware. When set to False, the filtration, demodulation
              and integration of the acquired pulses is done at the host computer. When set to True, the
              demodulation, integration and discretization of the pulse is done in real time at the FPGA of the
              instrument.

                - Sequencer 0 is used always for acquisitions and it is the first sequencer used to synthesise pulses.
                - Sequencer 1 to 6 are used as needed to synthesise simultaneous pulses on the same channel (required in
                  multiplexed readout) or when the memory of the default sequencers rans out.

        classification_parameters (dict): A dictionary containing the parameters needed classify the state of each qubit.
            from a single shot measurement:
        qubit_id (dict): the id of the qubit
            rotation_angle (float): 0   # in degrees 0.0<=v<=360.0. The angle of the rotation applied at the
            origin of the i q plane, that put the centroids of the state ``|0>`` and state ``|1>`` in a horizontal line.
            The rotation puts the centroid of state ``|1>`` to the right side of centroid of state ``|0>``.
        threshold (float): 0        # in V. The real component of the point along the horizontal line
            connecting both state centroids (after being rotated), that maximises the fidelity of the
            classification.

        channels (list): A list of the channels to which the instrument is connected.


    """

    DEFAULT_SEQUENCERS: dict = {"o1": 0, "i1": 0}
    SAMPLING_RATE: int = 1e9  # 1 GSPS
    FREQUENCY_LIMIT = 500e6  # 500 MHz

    property_wrapper = lambda parent, *parameter: property(
        lambda self: parent.device.get(parameter[0]),
        lambda self, x: parent._set_device_parameter(parent.device, *parameter, value=x),
    )
    property_wrapper.__doc__ = """A lambda function used to create properties that wrap around the device parameters
    and caches their value using `_set_device_parameter()`.
    """
    sequencer_property_wrapper = lambda parent, sequencer, *parameter: property(
        lambda self: parent.device.sequencers[sequencer].get(parameter[0]),
        lambda self, x: parent._set_device_parameter(parent.device.sequencers[sequencer], *parameter, value=x),
    )
    sequencer_property_wrapper.__doc__ = """A lambda function used to create properties that wrap around the device
    sequencer parameters and caches their value using `_set_device_parameter()`.
    """

    def __init__(self, name: str, address: str, settings: ClusterQRM_RF_Settings):
        """Initialises the instance.

        All class attributes are defined and initialised.
        """

        super().__init__(name, address)
        self.settings: ClusterQRM_RF_Settings = settings
        self.device: QbloxQrmQcm = None
        self.ports: dict = {}
        self.ports["o1"] = ClusterRF_OutputPort(module=self, sequencer_number=self.DEFAULT_SEQUENCERS["o1"], number=1)
        self.ports["i1"] = QbloxInputPort(
            module=self,
            output_sequencer_number=self.DEFAULT_SEQUENCERS["o1"],
            input_sequencer_number=self.DEFAULT_SEQUENCERS["i1"],
            number=1,
        )
        self.classification_parameters: dict = {}
        self.channels: list = []

        self._debug_folder: str = ""
        self._cluster: QbloxCluster = None
        self._input_ports_keys = ["i1"]
        self._output_ports_keys = ["o1"]
        self._sequencers: dict[Sequencer] = {"o1": []}
        self._port_channel_map: dict = {}
        self._channel_port_map: dict = {}
        self._device_parameters = {}
        self._device_num_output_ports = 1
        self._device_num_sequencers: int
        self._free_sequencers_numbers: list[int] = []
        self._used_sequencers_numbers: list[int] = []
        self._unused_sequencers_numbers: list[int] = []
        self._execution_time: float = 0

    def connect(self, cluster: QbloxCluster):
        """Connects to the instrument using the instrument settings in the runcard.

        Once connected, it creates port classes with properties mapped to various instrument
        parameters, and initialises the the underlying device parameters.
        """
        if not self.is_connected:
            if cluster:
                # save a reference to the underlying object
                self.device: QbloxQrmQcm = cluster.modules[int(self.address.split(":")[1]) - 1]
                # TODO: test connection with the module before continuing. Currently if there is no
                # connection the instruction self._set_device_parameter(self.device, "in0_att", value=0)
                # fails, providing a misleading error message

                # save reference to cluster
                self._cluster = cluster
                self.is_connected = True

                # once connected, initialise the parameters of the device to the default values
                self._set_device_parameter(self.device, "in0_att", value=0)
                self._set_device_parameter(
                    self.device, "out0_offset_path0", "out0_offset_path1", value=0
                )  # Default after reboot = 7.625
                self._set_device_parameter(
                    self.device, "scope_acq_avg_mode_en_path0", "scope_acq_avg_mode_en_path1", value=True
                )
                self._set_device_parameter(
                    self.device, "scope_acq_sequencer_select", value=self.DEFAULT_SEQUENCERS["i1"]
                )
                self._set_device_parameter(
                    self.device, "scope_acq_trigger_level_path0", "scope_acq_trigger_level_path1", value=0
                )
                self._set_device_parameter(
                    self.device, "scope_acq_trigger_mode_path0", "scope_acq_trigger_mode_path1", value="sequencer"
                )

                # initialise the parameters of the default sequencer to the default values,
                # the rest of the sequencers are not configured here, but will be configured
                # with the same parameters as the default in process_pulse_sequence()
                target = self.device.sequencers[self.DEFAULT_SEQUENCERS["o1"]]

                self._set_device_parameter(target, "connect_out0", value="IQ")
                self._set_device_parameter(target, "connect_acq", value="in0")
                self._set_device_parameter(target, "cont_mode_en_awg_path0", "cont_mode_en_awg_path1", value=False)
                self._set_device_parameter(
                    target, "cont_mode_waveform_idx_awg_path0", "cont_mode_waveform_idx_awg_path1", value=0
                )
                self._set_device_parameter(target, "marker_ovr_en", value=True)  # Default after reboot = False
                self._set_device_parameter(target, "marker_ovr_value", value=15)  # Default after reboot = 0
                self._set_device_parameter(target, "mixer_corr_gain_ratio", value=1)
                self._set_device_parameter(target, "mixer_corr_phase_offset_degree", value=0)
                self._set_device_parameter(target, "offset_awg_path0", value=0)
                self._set_device_parameter(target, "offset_awg_path1", value=0)
                self._set_device_parameter(target, "sync_en", value=False)  # Default after reboot = False
                self._set_device_parameter(target, "upsample_rate_awg_path0", "upsample_rate_awg_path1", value=0)

                # on initialisation, disconnect all other sequencers from the ports
                self._device_num_sequencers = len(self.device.sequencers)
                for sequencer in range(1, self._device_num_sequencers):
                    self._set_device_parameter(
                        self.device.sequencers[sequencer],
                        "connect_out0",
                        value="off",
                    )  # Default after reboot = True

    def _set_device_parameter(self, target, *parameters, value):
        """Sets a parameter of the instrument, if it changed from the last stored in the cache.

        Args:
            target = an instance of qblox_instruments.qcodes_drivers.qcm_qrm.QcmQrm or
                                    qblox_instruments.qcodes_drivers.sequencer.Sequencer
            *parameters (list): A list of parameters to be cached and set.
            value = The value to set the paramters.
        Raises:
            Exception = If attempting to set a parameter without a connection to the instrument.
        """
        if self.is_connected:
            key = target.name + "." + parameters[0]
            if not key in self._device_parameters:
                for parameter in parameters:
                    if not hasattr(target, parameter):
                        raise Exception(f"The instrument {self.name} does not have parameters {parameter}.")
                    target.set(parameter, value)
                self._device_parameters[key] = value
            elif self._device_parameters[key] != value:
                for parameter in parameters:
                    target.set(parameter, value)
                self._device_parameters[key] = value
        else:
            raise Exception(f"There is no connection to the instrument {self.name}.")

    def _erase_device_parameters_cache(self):
        """Erases the cache of instrument parameters."""
        self._device_parameters = {}

    def setup(self):
        """Configures the instrument with the settings of the runcard.

        A connection to the instrument needs to be established beforehand.
        Args:
            **kwargs: dict = A dictionary of settings loaded from the runcard:

                - kwargs['ports']['o1']['channel'] (int | str): the id of the refrigerator channel the output port o1 is
                  connected to.
                - kwargs['ports']['o1']['attenuation'] (int): [0 to 60 dBm, in multiples of 2] attenuation at the output.
                - kwargs['ports']['o1']['lo_enabled'] (bool): enable or disable local oscillator for up-conversion.
                - kwargs['ports']['o1']['lo_frequency'] (int): [2_000_000_000 to 18_000_000_000 Hz] local oscillator
                  frequency.
                - kwargs['ports']['o1']['gain'] (float): [0.0 - 1.0 unitless] gain applied prior to up-conversion. Qblox
                  recommends to keep `pulse_amplitude * gain` below 0.3 to ensure the mixers are working in their
                  linear regime, if necessary, lowering the attenuation applied at the output.
                - kwargs['ports']['o1']['hardware_mod_en'] (bool): enables Hardware Modulation. In this mode, pulses are
                  modulated to the intermediate frequency using the numerically controlled oscillator within the
                  fpga. It only requires the upload of the pulse envelope waveform.
                - kwargs['ports']['i1']['channel'] (int | str): the id of the refrigerator channel the input port i1 is
                  connected to.
                - kwargs['ports']['i1']['hardware_demod_en'] (bool): enables Hardware Demodulation. In this mode, the
                  sequencers of the fpga demodulate, integrate and classify the results for every shot. Once
                  integrated, the i and q values and the result of the classification requires much less memory,
                  so they can be stored for every shot in separate `bins` and retrieved later. Hardware Demodulation
                  also allows making multiple readouts on the same qubit at different points in the circuit, which is
                  not possible with Software Demodulation.
                - kwargs['acquisition_hold_off'] (int): [0 to 16834 ns, in multiples of 4] the time between the moment
                  the start of the readout pulse begins to be played, and the start of the acquisition. This is used
                  to account for the time of flight of the pulses from the output port to the input port.
                - kwargs['acquisition_duration'] (int): [0 to 8192 ns] the duration of the acquisition. It is limited by
                  the amount of memory available in the fpga to store i q samples.
                - kwargs['classification_parameters'][qubit_id][rotation_angle] (float): [0.0 to 359.999 deg] the angle
                  to rotate the results so that the projection on the real axis renders the maximum fidelity.
                - kwargs['classification_parameters'][qubit_id][threshold] (float): [-1.0 to 1.0 Volt] the voltage to be
                  used as threshold to classify the state of each shot.

        Raises:
            Exception = If attempting to set a parameter without a connection to the instrument.
        """
        settings: ClusterQRM_RF_Settings = self.settings
        if self.is_connected:
            # Load settings
            port_settings: ClusterRF_OutputPort_Settings = settings.ports["o1"]
            self.ports["o1"].channel = port_settings.channel
            self._port_channel_map["o1"] = self.ports["o1"].channel
            self.ports["o1"].attenuation = port_settings.attenuation
            self.ports["o1"].lo_enabled = port_settings.lo_enabled
            self.ports["o1"].lo_frequency = port_settings.lo_frequency
            self.ports["o1"].gain = port_settings.gain
            self.ports["o1"].hardware_mod_en = port_settings.hardware_mod_en

            self.ports["o1"].nco_freq = 0
            self.ports["o1"].nco_phase_offs = 0

            port_settings: QbloxInputPort_Settings = settings.ports["i1"]
            self.ports["i1"].channel = port_settings.channel
            self._port_channel_map["i1"] = self.ports["i1"].channel
            self.ports["i1"].hardware_demod_en = port_settings.hardware_demod_en
            self.ports["i1"].acquisition_hold_off = port_settings.acquisition_hold_off
            self.ports["i1"].acquisition_duration = port_settings.acquisition_duration

            self._channel_port_map = {v: k for k, v in self._port_channel_map.items()}
            self.channels = list(self._channel_port_map.keys())
        else:
            raise Exception("The instrument cannot be set up, there is no connection")

    def _get_next_sequencer(self, port: str, frequency: int, qubits: dict, qubit: None):
        """Retrieves and configures the next avaliable sequencer.

        The parameters of the new sequencer are copied from those of the default sequencer, except for the intermediate
        frequency and classification parameters.

        Args:
            port (str):
            frequency (int):
            qubit (str|int):
        Raises:
            Exception = If attempting to set a parameter without a connection to the instrument.
        """

        # select a new sequencer and configure it as required
        next_sequencer_number = self._free_sequencers_numbers.pop(0)
        if next_sequencer_number != self.DEFAULT_SEQUENCERS[port]:
            for parameter in self.device.sequencers[self.DEFAULT_SEQUENCERS[port]].parameters:
                # exclude read-only parameter `sequence` and others that have wrong default values (qblox bug)
                if not parameter in ["sequence", "thresholded_acq_marker_address", "thresholded_acq_trigger_address"]:
                    value = self.device.sequencers[self.DEFAULT_SEQUENCERS[port]].get(param_name=parameter)
                    if value:
                        target = self.device.sequencers[next_sequencer_number]
                        self._set_device_parameter(target, parameter, value=value)

        # if hardware demodulation is enabled, configure nco_frequency and classification parameters
        if self.ports["i1"].hardware_demod_en or self.ports["o1"].hardware_mod_en:
            self._set_device_parameter(
                self.device.sequencers[next_sequencer_number],
                "nco_freq",
                value=frequency,
                # It assumes all pulses in non_overlapping_pulses set have the same frequency.
                # Non-overlapping pulses of different frequencies on the same qubit channel, with hardware_demod_en
                # would lead to wrong results.
                # TODO: Throw error in that event or implement non_overlapping_same_frequency_pulses
                #       Even better, set the frequency before each pulse is played (would work with hardware modulation only)
            )
        # if self.ports["i1"].hardware_demod_en and qubit in self.classification_parameters:
        if self.ports["i1"].hardware_demod_en and not qubits[qubit].threshold is None:
            self._set_device_parameter(
                self.device.sequencers[next_sequencer_number],
                "thresholded_acq_rotation",
                # value=self.classification_parameters[qubit]["rotation_angle"],
                value=(qubits[qubit].iq_angle * 360 / (2 * np.pi)) % 360,
            )
            self._set_device_parameter(
                self.device.sequencers[next_sequencer_number],
                "thresholded_acq_threshold",
                # value=self.classification_parameters[qubit]["threshold"] * self.ports["i1"].acquisition_duration,
                value=qubits[qubit].threshold * self.ports["i1"].acquisition_duration,
            )
        # create sequencer wrapper
        sequencer = Sequencer(next_sequencer_number)
        sequencer.qubit = qubit
        return sequencer

    def get_if(self, pulse: Pulse):
        """Returns the intermediate frequency needed to synthesise a pulse based on the port lo frequency."""

        _rf = pulse.frequency
        _lo = self.ports[self._channel_port_map[pulse.channel]].lo_frequency
        _if = _rf - _lo
        if abs(_if) > self.FREQUENCY_LIMIT:
            raise Exception(
                f"""
            Pulse frequency {_rf:_} cannot be synthesised with current lo frequency {_lo:_}.
            The intermediate frequency {_if:_} would exceed the maximum frequency of {self.FREQUENCY_LIMIT:_}
            """
            )
        return _if

    def process_pulse_sequence(
        self,
        qubits: dict,
        instrument_pulses: PulseSequence,
        navgs: int,
        nshots: int,
        repetition_duration: int,
        sweepers=None,
    ):
        """Processes a sequence of pulses and sweepers, generating the waveforms and program required by
        the instrument to synthesise them.

        The output of the process is a list of sequencers used for each port, configured with the information
        required to play the sequence.
        The following features are supported:

            - multiplexed readout of up to 6 qubits
            - overlapping pulses
            - hardware modulation, demodulation, and classification
            - software modulation, with support for arbitrary pulses
            - software demodulation
            - binned acquisition
            -  real-time sweepers of

                - pulse frequency (requires hardware modulation)
                - pulse relative phase (requires hardware modulation)
                - pulse amplitude
                - pulse start
                - pulse duration
                - port gain
                - port offset

            - multiple readouts for the same qubit (sequence unrolling)
            - pulses of up to 8192 pairs of i, q samples
            - sequencer memory optimisation (waveforms cache)
            - extended waveform memory with the use of multiple sequencers
            - intrument parameters cache

        Args:
            instrument_pulses (PulseSequence): A collection of Pulse objects to be played by the instrument.
            navgs (int): The number of times the sequence of pulses should be executed averaging the results.
            nshots (int): The number of times the sequence of pulses should be executed without averaging.
            repetition_duration (int): The total duration of the pulse sequence execution plus the reset/relaxation time.
            sweepers (list(Sweeper)): A list of Sweeper objects to be implemented.
        """
        if sweepers is None:
            sweepers = []
        sequencer: Sequencer
        sweeper: Sweeper

        # calculate the number of bins
        num_bins = nshots
        for sweeper in sweepers:
            num_bins *= len(sweeper.values)

        # estimate the execution time
        self._execution_time = navgs * num_bins * ((repetition_duration + 1000 * len(sweepers)) * 1e-9)

        port = "o1"
        # initialise the list of free sequencer numbers to include the default for each port {'o1': 0}
        self._free_sequencers_numbers = [self.DEFAULT_SEQUENCERS[port]] + [1, 2, 3, 4, 5]

        # split the collection of instruments pulses by ports
        port_pulses: PulseSequence = instrument_pulses.get_channel_pulses(self._port_channel_map[port])

        # initialise the list of sequencers required by the port
        self._sequencers[port] = []

        if not port_pulses.is_empty:
            # split the collection of port pulses in non overlapping pulses
            non_overlapping_pulses: PulseSequence
            for non_overlapping_pulses in port_pulses.separate_overlapping_pulses():
                # each set of not overlapping pulses will be played by a separate sequencer
                # check sequencer availability
                if len(self._free_sequencers_numbers) == 0:
                    raise Exception(
                        f"The number of sequencers requried to play the sequence exceeds the number available {self._device_num_sequencers}."
                    )
                # get next sequencer
                sequencer = self._get_next_sequencer(
                    port=port,
                    frequency=self.get_if(non_overlapping_pulses[0]),
                    qubits=qubits,
                    qubit=non_overlapping_pulses[0].qubit,
                )
                # add the sequencer to the list of sequencers required by the port
                self._sequencers[port].append(sequencer)

                # make a temporary copy of the pulses to be processed
                pulses_to_be_processed = non_overlapping_pulses.shallow_copy()
                while not pulses_to_be_processed.is_empty:
                    pulse: Pulse = pulses_to_be_processed[0]
                    # attempt to save the waveforms to the sequencer waveforms buffer
                    try:
                        sequencer.waveforms_buffer.add_waveforms(pulse, self.ports[port].hardware_mod_en, sweepers)
                        sequencer.pulses.add(pulse)
                        pulses_to_be_processed.remove(pulse)

                    # if there is not enough memory in the current sequencer, use another one
                    except WaveformsBuffer.NotEnoughMemory:
                        if len(pulse.waveform_i) + len(pulse.waveform_q) > WaveformsBuffer.SIZE:
                            raise NotImplementedError(
                                f"Pulses with waveforms longer than the memory of a sequencer ({WaveformsBuffer.SIZE // 2}) are not supported."
                            )
                        if len(self._free_sequencers_numbers) == 0:
                            raise Exception(
                                f"The number of sequencers requried to play the sequence exceeds the number available {self._device_num_sequencers}."
                            )
                        # get next sequencer
                        sequencer = self._get_next_sequencer(
                            port=port,
                            frequency=self.get_if(non_overlapping_pulses[0]),
                            qubits=qubits,
                            qubit=non_overlapping_pulses[0].qubit,
                        )
                        # add the sequencer to the list of sequencers required by the port
                        self._sequencers[port].append(sequencer)

        # update the lists of used and unused sequencers that will be needed later on
        self._used_sequencers_numbers = []
        for port in self._output_ports_keys:
            for sequencer in self._sequencers[port]:
                self._used_sequencers_numbers.append(sequencer.number)
        self._unused_sequencers_numbers = []
        for n in range(self._device_num_sequencers):
            if not n in self._used_sequencers_numbers:
                self._unused_sequencers_numbers.append(n)

        # generate and store the Waveforms dictionary, the Acquisitions dictionary, the Weights and the Program
        for port in self._output_ports_keys:
            for sequencer in self._sequencers[port]:
                pulses = sequencer.pulses
                program = sequencer.program

                ## pre-process sweepers ##
                # TODO: move qibolab sweepers preprocessing to qblox controller

                # attach a sweeper attribute to the pulse so that it is easily accesible by the code that generates
                # the pseudo-assembly program
                pulse = None
                for pulse in pulses:
                    pulse.sweeper = None

                pulse_sweeper_parameters = [
                    Parameter.frequency,
                    Parameter.amplitude,
                    Parameter.duration,
                    Parameter.relative_phase,
                    Parameter.start,
                ]

                for sweeper in sweepers:
                    if sweeper.parameter in pulse_sweeper_parameters:
                        # check if this sequencer takes an active role in the sweep
                        if sweeper.pulses and set(sequencer.pulses) & set(sweeper.pulses):
                            # plays an active role
                            reference_value = None
                            if sweeper.parameter == Parameter.frequency:
                                if sequencer.pulses:
                                    reference_value = self.get_if(
                                        sequencer.pulses[0]
                                    )  # uses the frequency of the first pulse (assuming all same freq)
                            if sweeper.parameter == Parameter.amplitude:
                                for pulse in pulses:
                                    if pulse in sweeper.pulses:
                                        reference_value = pulse.amplitude  # uses the amplitude of the first pulse
                            if sweeper.parameter == Parameter.duration and pulse in sweeper.pulses:
                                # for duration sweepers bake waveforms
                                sweeper.qs = QbloxSweeper(
                                    program=program, type=QbloxSweeperType.duration, rel_values=pulse.idx_range
                                )
                            else:
                                # create QbloxSweepers and attach them to qibolab sweeper
                                if sweeper.type == SweeperType.OFFSET and reference_value:
                                    sweeper.qs = QbloxSweeper.from_sweeper(
                                        program=program, sweeper=sweeper, add_to=reference_value
                                    )
                                elif sweeper.type == SweeperType.FACTOR and reference_value:
                                    sweeper.qs = QbloxSweeper.from_sweeper(
                                        program=program, sweeper=sweeper, multiply_to=reference_value
                                    )
                                else:
                                    sweeper.qs = QbloxSweeper.from_sweeper(program=program, sweeper=sweeper)

                            # finally attach QbloxSweepers to the pulses being swept
                            sweeper.qs.update_parameters = True
                            pulse.sweeper = sweeper.qs
                        else:
                            # does not play an active role
                            sweeper.qs = QbloxSweeper(
                                program=program,
                                type=QbloxSweeperType.number,
                                rel_values=range(len(sweeper.values)),
                                name=sweeper.parameter.name,
                            )

                    # else: # qubit_sweeper_parameters
                    #     if sweeper.qubits and sequencer.qubit in [_.name for _ in sweeper.qubits]:
                    #         # plays an active role
                    #         if sweeper.parameter == Parameter.bias:
                    #             reference_value = self.ports[port].offset
                    #             # create QbloxSweepers and attach them to qibolab sweeper
                    #             if sweeper.type == SweeperType.ABSOLUTE:
                    #                 sweeper.qs = QbloxSweeper.from_sweeper(
                    #                     program=program, sweeper=sweeper, add_to=-reference_value
                    #                 )
                    #             elif sweeper.type == SweeperType.OFFSET:
                    #                 sweeper.qs = QbloxSweeper.from_sweeper(program=program, sweeper=sweeper)
                    #             elif sweeper.type == SweeperType.FACTOR:
                    #                 raise Exception("SweeperType.FACTOR for Parameter.bias not supported")
                    #             sweeper.qs.update_parameters = True
                    #     else:
                    #         # does not play an active role
                    #         sweeper.qs = QbloxSweeper(
                    #             program=program, type=QbloxSweeperType.number, rel_values=range(len(sweeper.values)),
                    #             name = sweeper.parameter.name
                    #         )
                    else:
                        # does not play an active role
                        sweeper.qs = QbloxSweeper(
                            program=program,
                            type=QbloxSweeperType.number,
                            rel_values=range(len(sweeper.values)),
                            name=sweeper.parameter.name,
                        )

                    # # FIXME: for qubit sweepers (Parameter.bias, Parameter.attenuation, Parameter.gain), the qubit
                    # # information alone is not enough to determine what instrument parameter is to be swept.
                    # # For example port gain, both the drive and readout ports have gain parameters.
                    # # Until this is resolved, and since bias is only implemented with QCMs offset, this instrument will
                    # # never take an active role in those sweeps.

                # Waveforms
                for index, waveform in enumerate(sequencer.waveforms_buffer.unique_waveforms):
                    sequencer.waveforms[waveform.serial] = {"data": waveform.data.tolist(), "index": index}

                # Acquisitions
                for acquisition_index, pulse in enumerate(sequencer.pulses.ro_pulses):
                    sequencer.acquisitions[pulse.serial] = {"num_bins": num_bins, "index": acquisition_index}

                # Add scope_acquisition to default sequencer
                if sequencer.number == self.DEFAULT_SEQUENCERS[port]:
                    sequencer.acquisitions["scope_acquisition"] = {"num_bins": 1, "index": acquisition_index + 1}

                # Program
                minimum_delay_between_instructions = 4

                # Active reset is not fully tested yet
                active_reset = False
                active_reset_address = 1
                active_reset_pulse_idx_I = 1
                active_reset_pulse_idx_Q = 1

                sequence_total_duration = pulses.finish  # the minimum delay between instructions is 4ns
                time_between_repetitions = repetition_duration - sequence_total_duration
                assert time_between_repetitions > minimum_delay_between_instructions
                # TODO: currently relaxation_time needs to be greater than acquisition_hold_off
                # so that the time_between_repetitions is equal to the sequence_total_duration + relaxation_time
                # to be compatible with th erest of the platforms, change it so that time_between_repetitions
                # is equal to pulsesequence duration + acquisition_hold_off if relaxation_time < acquisition_hold_off

                # create registers for key variables
                # nshots is used in the loop that iterates over the number of shots
                nshots_register = Register(program, "nshots")
                # during a sweep, each shot is saved in the bin bin_n
                bin_n = Register(program, "bin_n")
                # navgs is used in the loop of hardware averages
                navgs_register = Register(program, "navgs")

                header_block = Block("setup")
                if active_reset:
                    header_block.append(
                        f"set_latch_en {active_reset_address}, 4", f"monitor triggers on address {active_reset_address}"
                    )

                body_block = Block()

                body_block.append(f"wait_sync {minimum_delay_between_instructions}")
                if self.ports["i1"].hardware_demod_en or self.ports["o1"].hardware_mod_en:
                    body_block.append("reset_ph")
                    body_block.append_spacer()

                pulses_block = Block("play_and_acquire")
                # Add an initial wait instruction for the first pulse of the sequence
                initial_wait_block = wait_block(
                    wait_time=pulses[0].start, register=Register(program), force_multiples_of_four=True
                )
                pulses_block += initial_wait_block

                for n in range(pulses.count):
                    if pulses[n].sweeper and pulses[n].sweeper.type == QbloxSweeperType.start:
                        pulses_block.append(f"wait {pulses[n].sweeper.register}")

                    if self.ports["o1"].hardware_mod_en:
                        # # Set frequency
                        # _if = self.get_if(pulses[n])
                        # pulses_block.append(f"set_freq {convert_frequency(_if)}", f"set intermediate frequency to {_if} Hz")

                        # Set phase
                        if pulses[n].sweeper and pulses[n].sweeper.type == QbloxSweeperType.relative_phase:
                            pulses_block.append(f"set_ph {pulses[n].sweeper.register}")
                        else:
                            pulses_block.append(
                                f"set_ph {convert_phase(pulses[n].relative_phase)}",
                                comment=f"set relative phase {pulses[n].relative_phase} rads",
                            )

                    if pulses[n].type == PulseType.READOUT:
                        delay_after_play = self.ports["i1"].acquisition_hold_off

                        if len(pulses) > n + 1:
                            # If there are more pulses to be played, the delay is the time between the pulse end and the next pulse start
                            delay_after_acquire = (
                                pulses[n + 1].start - pulses[n].start - self.ports["i1"].acquisition_hold_off
                            )
                        else:
                            delay_after_acquire = sequence_total_duration - pulses[n].start
                            time_between_repetitions = (
                                repetition_duration - sequence_total_duration - self.ports["i1"].acquisition_hold_off
                            )
                            assert time_between_repetitions > 0

                        if delay_after_acquire < minimum_delay_between_instructions:
                            raise Exception(
                                f"The minimum delay after starting acquisition is {minimum_delay_between_instructions}ns."
                            )

                        if pulses[n].sweeper and pulses[n].sweeper.type == QbloxSweeperType.duration:
                            RI = pulses[n].sweeper.register
                            if pulses[n].type == PulseType.FLUX:
                                RQ = pulses[n].sweeper.register
                            else:
                                RQ = pulses[n].sweeper.aux_register

                            pulses_block.append(
                                f"play  {RI},{RQ},{delay_after_play}",  # FIXME delay_after_play won't work as the duration increases
                                comment=f"play pulse {pulses[n]} sweeping its duration",
                            )
                        else:
                            # Prepare play instruction: play wave_i_index, wave_q_index, delay_next_instruction
                            pulses_block.append(
                                f"play  {sequencer.waveforms_buffer.unique_waveforms.index(pulses[n].waveform_i)},{sequencer.waveforms_buffer.unique_waveforms.index(pulses[n].waveform_q)},{delay_after_play}",
                                comment=f"play waveforms {pulses[n]}",
                            )

                        # Prepare acquire instruction: acquire acquisition_index, bin_index, delay_next_instruction
                        if active_reset:
                            pulses_block.append(f"acquire {pulses.ro_pulses.index(pulses[n])},{bin_n},4")
                            pulses_block.append(f"latch_rst {delay_after_acquire + 300 - 4}")
                        else:
                            pulses_block.append(
                                f"acquire {pulses.ro_pulses.index(pulses[n])},{bin_n},{delay_after_acquire}"
                            )

                    else:
                        # Calculate the delay_after_play that is to be used as an argument to the play instruction
                        if len(pulses) > n + 1:
                            # If there are more pulses to be played, the delay is the time between the pulse end and the next pulse start
                            delay_after_play = pulses[n + 1].start - pulses[n].start
                        else:
                            delay_after_play = sequence_total_duration - pulses[n].start

                        if delay_after_play < minimum_delay_between_instructions:
                            raise Exception(
                                f"The minimum delay between the start of two pulses in the same channel is {minimum_delay_between_instructions}ns."
                            )

                        if pulses[n].sweeper and pulses[n].sweeper.type == QbloxSweeperType.duration:
                            RI = pulses[n].sweeper.register
                            if pulses[n].type == PulseType.FLUX:
                                RQ = pulses[n].sweeper.register
                            else:
                                RQ = pulses[n].sweeper.aux_register

                            pulses_block.append(
                                f"play  {RI},{RQ},{delay_after_play}",  # FIXME delay_after_play won't work as the duration increases
                                comment=f"play pulse {pulses[n]} sweeping its duration",
                            )
                        else:
                            # Prepare play instruction: play wave_i_index, wave_q_index, delay_next_instruction
                            pulses_block.append(
                                f"play  {sequencer.waveforms_buffer.unique_waveforms.index(pulses[n].waveform_i)},{sequencer.waveforms_buffer.unique_waveforms.index(pulses[n].waveform_q)},{delay_after_play}",
                                comment=f"play waveforms {pulses[n]}",
                            )

                body_block += pulses_block
                body_block.append_spacer()

                if active_reset:
                    final_reset_block = Block()
                    final_reset_block.append(f"set_cond 1, {active_reset_address}, 0, 4", comment="active reset")
                    final_reset_block.append(f"play {active_reset_pulse_idx_I}, {active_reset_pulse_idx_Q}, 4", level=1)
                    final_reset_block.append(f"set_cond 0, {active_reset_address}, 0, 4")
                else:
                    final_reset_block = wait_block(
                        wait_time=time_between_repetitions, register=Register(program), force_multiples_of_four=False
                    )
                final_reset_block.append_spacer()
                final_reset_block.append(f"add {bin_n}, 1, {bin_n}", "increase bin counter")

                body_block += final_reset_block

                footer_block = Block("cleaup")
                footer_block.append(f"stop")

                # wrap pulses block in sweepers loop blocks
                for sweeper in sweepers:
                    body_block = sweeper.qs.block(inner_block=body_block)

                nshots_block: Block = loop_block(
                    start=0, stop=nshots, step=1, register=nshots_register, block=body_block
                )
                nshots_block.prepend(f"move 0, {bin_n}", "reset bin counter")
                nshots_block.append_spacer()

                navgs_block = loop_block(start=0, stop=navgs, step=1, register=navgs_register, block=nshots_block)
                program.add_blocks(header_block, navgs_block, footer_block)

                sequencer.program = repr(program)

    def upload(self):
        """Uploads waveforms and programs of all sequencers and arms them in preparation for execution.

        This method should be called after `process_pulse_sequence()`.
        It configures certain parameters of the instrument based on the needs of resources determined
        while processing the pulse sequence.
        """
        # Setup
        for sequencer_number in self._used_sequencers_numbers:
            target = self.device.sequencers[sequencer_number]
            self._set_device_parameter(target, "sync_en", value=True)
            self._set_device_parameter(target, "marker_ovr_en", value=True)  # Default after reboot = False
            self._set_device_parameter(target, "marker_ovr_value", value=15)  # Default after reboot = 0

        for sequencer_number in self._unused_sequencers_numbers:
            target = self.device.sequencers[sequencer_number]
            self._set_device_parameter(target, "sync_en", value=False)
            self._set_device_parameter(target, "marker_ovr_en", value=False)  # Default after reboot = False
            self._set_device_parameter(target, "marker_ovr_value", value=0)  # Default after reboot = 0
            if sequencer_number >= 1:  # Never disconnect default sequencers
                self._set_device_parameter(target, "connect_out0", value="off")
                self._set_device_parameter(target, "connect_acq", value="in0")

        # Upload waveforms and program
        qblox_dict = {}
        sequencer: Sequencer
        for port in self._output_ports_keys:
            for sequencer in self._sequencers[port]:
                # Add sequence program and waveforms to single dictionary
                qblox_dict[sequencer] = {
                    "waveforms": sequencer.waveforms,
                    "weights": sequencer.weights,
                    "acquisitions": sequencer.acquisitions,
                    "program": sequencer.program,
                }

                # Upload dictionary to the device sequencers
                self.device.sequencers[sequencer.number].sequence(qblox_dict[sequencer])

                # DEBUG: QRM RF Save sequence to file
                if self._debug_folder != "":
                    filename = self._debug_folder + f"Z_{self.name}_sequencer{sequencer.number}_sequence.json"
                    with open(filename, "w", encoding="utf-8") as file:
                        json.dump(qblox_dict[sequencer], file, indent=4)
                        file.write(sequencer.program)

        # Clear acquisition memory and arm sequencers
        for sequencer_number in self._used_sequencers_numbers:
            self.device.sequencers[sequencer_number].delete_acquisition_data(all=True)
            self.device.arm_sequencer(sequencer_number)

        # DEBUG: QRM RF Print Readable Snapshot
        # print(self.name)
        # self.device.print_readable_snapshot(update=True)

        # DEBUG: QRM RF Save Readable Snapshot
        from qibolab.instruments.qblox.debug import print_readable_snapshot

        if self._debug_folder != "":
            filename = self._debug_folder + f"Z_{self.name}_snapshot.json"
            with open(filename, "w", encoding="utf-8") as file:
                print_readable_snapshot(self.device, file, update=True)

    def play_sequence(self):
        """Plays the sequence of pulses.

        Starts the sequencers needed to play the sequence of pulses."""

        # Start used sequencers
        for sequencer_number in self._used_sequencers_numbers:
            self.device.start_sequencer(sequencer_number)

    def acquire(self):
        """Retrieves the readout results.

        Returns:
            The results returned vary depending on whether demodulation is performed in software or hardware:
            - Software Demodulation:
              Every readout pulse triggers an acquisition, where the 16384 i and q samples of the waveform
              acquired by the ADC are saved into a dedicated memory within the FPGA. This is what qblox calls
              *scoped acquisition*. The results of multiple shots are averaged in this memory, and cannot be
              retrieved independently. The resulting waveforms averages (i and q) are then demodulated and
              integrated in software (and finally divided by the number of samples).
              Since Software Demodulation relies on the data of the scoped acquisition and that data is the
              average of all acquisitions, **only one readout pulse per qubit is supported**, so that
              the averages all correspond to reading the same quantum state.
              Multiple symultaneous readout pulses on different qubits are supported.
              The results returned are:

                - acquisition_results["averaged_raw"] (dict): a dictionary containing tuples with the averages of
                  the i and q waveforms for every readout pulse:
                  ([i samples], [q samples])
                  The data for a specific reaout pulse can be obtained either with:

                    - `acquisition_results["averaged_raw"][ro_pulse.serial]`
                    - `acquisition_results["averaged_raw"][ro_pulse.qubit]`

                - acquisition_results["averaged_demodulated_integrated"] (dict): a dictionary containing tuples
                  with the results of demodulating and integrating (averaging over time) the average of the
                  waveforms for every pulse: ``(amplitude[V], phase[rad], i[V], q[V])``

              The data for a specific readout pulse can be obtained either with:

                - `acquisition_results["averaged_demodulated_integrated"][ro_pulse.serial]`
                - `acquisition_results["averaged_demodulated_integrated"][ro_pulse.qubit]`

              Or directly with:

                - `acquisition_results[ro_pulse.serial]`
                - `acquisition_results[ro_pulse.qubit]`

            - Hardware Demodulation:
              With hardware demodulation activated, the FPGA can demodulate, integrate (average over time), and classify
              each shot individually, saving the results on separate bins. The raw data of each acquisition continues to
              be averaged as with software modulation, so there is no way to access the raw data of each shot (unless
              executed one shot at a time). The FPGA uses fixed point arithmetic for the demodulation and integration;
              if the power level of the signal at the input port is low (the minimum resolution of the ADC is 240uV)
              rounding precission errors can accumulate and render wrong results. It is advisable to have a power level
              at least higher than 5mV.
              The results returned are:

                - acquisition_results["demodulated_integrated_averaged"] (dict): a dictionary containing tuples
                  with the results of demodulating and integrating (averaging over time) each shot waveform and then
                  averaging of the many shots: ``(amplitude[V], phase[rad], i[V], q[V])``
                - acquisition_results["demodulated_integrated_binned"] (dict): a dictionary containing tuples of lists
                  with the results of demodulating and integrating every shot waveform: ``([amplitudes[V]], [phases[rad]], [is[V]], [qs[V]])``
                - acquisition_results["demodulated_integrated_classified_binned"] (dict): a dictionary containing lists
                  with the results of demodulating, integrating and classifying every shot: ``([states[0 or 1]])``
                - acquisition_results["probability"] (dict): a dictionary containing the frequency of state 1 measurements:
                      total number of shots classified as 1 / number of shots

              If the number of readout pulses per qubit is only one, then the following is also provided:

                - acquisition_results["averaged_raw"] (dict): a dictionary containing tuples with the averages of
                  the i and q waveforms for every readout pulse: ``([i samples], [q samples])``
                - acquisition_results["averaged_demodulated_integrated"] (dict): a dictionary containing tuples
                  with the results of demodulating and integrating (averaging over time) the average of the
                  waveforms for every pulse: ``(amplitude[V], phase[rad], i[V], q[V])``

              The data within each of the above dictionaries, for a specific readout pulse or for the last readout
              pulse of a qubit can be retrieved either with:

                - `acquisition_results[dictionary_name][ro_pulse.serial]`
                - `acquisition_results[dictionary_name][ro_pulse.qubit]`

              And acquisition_results["averaged_demodulated_integrated"] directly with:

                - `acquisition_results[ro_pulse.serial]`
                - `acquisition_results[ro_pulse.qubit]`

        """

        # wait until all sequencers stop
        time_out = int(self._execution_time) + 60
        import time

        from qibo.config import log

        t = time.time()

        for sequencer_number in self._used_sequencers_numbers:
            while True:
                try:
                    state = self.device.get_sequencer_state(sequencer_number)
                except:
                    pass
                else:
                    if state.status == "STOPPED":
                        # log.info(f"{self.device.sequencers[sequencer_number].name} state: {state}")
                        # TODO: check flags for errors
                        break
                    elif time.time() - t > time_out:
                        log.info(f"Timeout - {self.device.sequencers[sequencer_number].name} state: {state}")
                        self.device.stop_sequencer(sequencer_number)
                        break
                time.sleep(1)

        acquisition_results = {}

        # Qblox qrm modules only have one memory for scope acquisition.
        # Only one sequencer can save data to that memory.
        # Several acquisitions at different points in the circuit will result in the undesired averaging
        # of the results.
        # Scope Acquisition should only be used with one acquisition per module.
        # Several readout pulses are supported for as long as they take place symultaneously.
        # Scope Acquisition data should be ignored with more than one acquisition or with Hardware Demodulation.

        # Software Demodulation requires the data from Scope Acquisition, therefore Software Demodulation only works
        # with one acquisition per module.

        # The data is retrieved by storing it first in one of the acquisitions of one of the sequencers.
        # Any could be used, but we always use 'scope_acquisition' acquisition of the default sequencer to store it.

        # Store scope acquisition data on 'scope_acquisition' acquisition of the default sequencer
        for port in self._output_ports_keys:
            for sequencer in self._sequencers[port]:
                if sequencer.number == self.DEFAULT_SEQUENCERS[port]:
                    self.device.store_scope_acquisition(sequencer.number, "scope_acquisition")
                    scope_acquisition_raw_results = self.device.get_acquisitions(sequencer.number)["scope_acquisition"]

        acquisition_results["demodulated_integrated_averaged"] = {}
        acquisition_results["averaged_raw"] = {}
        acquisition_results["averaged_demodulated_integrated"] = {}
        acquisition_results["demodulated_integrated_binned"] = {}
        acquisition_results["demodulated_integrated_classified_binned"] = {}
        acquisition_results["probability"] = {}
        data = {}
        for port in self._output_ports_keys:
            for sequencer in self._sequencers[port]:
                if not self.ports["i1"].hardware_demod_en:  # Software Demodulation
                    if len(sequencer.pulses.ro_pulses) == 1:
                        pulse = sequencer.pulses.ro_pulses[0]

                        acquisition_results["averaged_raw"][pulse.serial] = (
                            scope_acquisition_raw_results["acquisition"]["scope"]["path0"]["data"][
                                0 : self.ports["i1"].acquisition_duration
                            ],
                            scope_acquisition_raw_results["acquisition"]["scope"]["path1"]["data"][
                                0 : self.ports["i1"].acquisition_duration
                            ],
                        )
                        acquisition_results["averaged_raw"][pulse.qubit] = acquisition_results["averaged_raw"][
                            pulse.serial
                        ]

                        i, q = self._process_acquisition_results(scope_acquisition_raw_results, pulse, demodulate=True)
                        acquisition_results["averaged_demodulated_integrated"][pulse.serial] = (
                            np.sqrt(i**2 + q**2),
                            np.arctan2(q, i),
                            i,
                            q,
                        )
                        acquisition_results["averaged_demodulated_integrated"][pulse.qubit] = acquisition_results[
                            "averaged_demodulated_integrated"
                        ][pulse.serial]

                        # Default Results = Averaged Demodulated Integrated
                        acquisition_results[pulse.serial] = acquisition_results["averaged_demodulated_integrated"][
                            pulse.serial
                        ]
                        acquisition_results[pulse.qubit] = acquisition_results["averaged_demodulated_integrated"][
                            pulse.qubit
                        ]

                        # ignores the data available in acquisition results and returns only i and q voltages
                        # TODO: to be updated once the functionality of ExecutionResults is extended
                        data[pulse.serial] = (i, q)

                    else:
                        raise Exception(
                            """Software Demodulation only supports one acquisition per channel.
                        Multiple readout pulses are supported as long as they are symultaneous (requiring one acquisition)"""
                        )

                else:  # Hardware Demodulation
                    binned_raw_results = self.device.get_acquisitions(sequencer.number)
                    for pulse in sequencer.pulses.ro_pulses:
                        acquisition_name = pulse.serial
                        i, q = self._process_acquisition_results(
                            binned_raw_results[acquisition_name], pulse, demodulate=False
                        )
                        acquisition_results["demodulated_integrated_averaged"][pulse.serial] = (
                            np.sqrt(i**2 + q**2),
                            np.arctan2(q, i),
                            i,
                            q,
                        )
                        acquisition_results["demodulated_integrated_averaged"][pulse.qubit] = acquisition_results[
                            "demodulated_integrated_averaged"
                        ][pulse.serial]

                        # Default Results = Demodulated Integrated Averaged
                        acquisition_results[pulse.serial] = acquisition_results["demodulated_integrated_averaged"][
                            pulse.serial
                        ]
                        acquisition_results[pulse.qubit] = acquisition_results["demodulated_integrated_averaged"][
                            pulse.qubit
                        ]

                        # Save individual shots
                        shots_i = (
                            np.array(
                                binned_raw_results[acquisition_name]["acquisition"]["bins"]["integration"]["path0"]
                            )
                            / self.ports["i1"].acquisition_duration
                        )
                        shots_q = (
                            np.array(
                                binned_raw_results[acquisition_name]["acquisition"]["bins"]["integration"]["path1"]
                            )
                            / self.ports["i1"].acquisition_duration
                        )

                        acquisition_results["demodulated_integrated_binned"][pulse.serial] = (
                            np.sqrt(shots_i**2 + shots_q**2),
                            np.arctan2(shots_q, shots_i),
                            shots_i,
                            shots_q,
                        )
                        acquisition_results["demodulated_integrated_binned"][pulse.qubit] = acquisition_results[
                            "demodulated_integrated_binned"
                        ][pulse.serial]

                        acquisition_results["demodulated_integrated_classified_binned"][
                            pulse.serial
                        ] = binned_raw_results[acquisition_name]["acquisition"]["bins"]["threshold"]
                        acquisition_results["demodulated_integrated_classified_binned"][
                            pulse.qubit
                        ] = acquisition_results["demodulated_integrated_classified_binned"][pulse.serial]

                        acquisition_results["probability"][pulse.serial] = np.mean(
                            acquisition_results["demodulated_integrated_classified_binned"][pulse.serial]
                        )
                        acquisition_results["probability"][pulse.qubit] = acquisition_results["probability"][
                            pulse.serial
                        ]

                        # Provide Scope Data for verification (assuming memory reseet is being done)
                        if len(sequencer.pulses.ro_pulses) == 1:
                            pulse = sequencer.pulses.ro_pulses[0]

                            acquisition_results["averaged_raw"][pulse.serial] = (
                                scope_acquisition_raw_results["acquisition"]["scope"]["path0"]["data"][
                                    0 : self.ports["i1"].acquisition_duration
                                ],
                                scope_acquisition_raw_results["acquisition"]["scope"]["path1"]["data"][
                                    0 : self.ports["i1"].acquisition_duration
                                ],
                            )
                            acquisition_results["averaged_raw"][pulse.qubit] = acquisition_results["averaged_raw"][
                                pulse.serial
                            ]

                            i, q = self._process_acquisition_results(
                                scope_acquisition_raw_results, pulse, demodulate=True
                            )

                            acquisition_results["averaged_demodulated_integrated"][pulse.serial] = (
                                np.sqrt(i**2 + q**2),
                                np.arctan2(q, i),
                                i,
                                q,
                            )
                            acquisition_results["averaged_demodulated_integrated"][pulse.qubit] = acquisition_results[
                                "averaged_demodulated_integrated"
                            ][pulse.serial]

                        # ignores the data available in acquisition results and returns only i and q voltages
                        # TODO: to be updated once the functionality of ExecutionResults is extended
                        data[acquisition_name] = (
                            shots_i,
                            shots_q,
                            np.array(acquisition_results["demodulated_integrated_classified_binned"][acquisition_name]),
                        )

                    # DEBUG: QRM RF Plot Incomming Pulses
                    # import qibolab.instruments.debug.incomming_pulse_plotting as pp
                    # pp.plot(raw_results)
                    # DEBUG: QRM RF Plot Acquisition_results
                    # from qibolab.debug.debug import plot_acquisition_results
                    # plot_acquisition_results(acquisition_results, pulse, savefig_filename="acquisition_results.png")
        return data

    def _process_acquisition_results(self, acquisition_results, readout_pulse: Pulse, demodulate=True):
        """Processes the results of the acquisition.

        If hardware demodulation is disabled, it demodulates and integrates the acquired pulse. If enabled,
        if processes the results as required by qblox (calculating the average by dividing the integrated results by
        the number of smaples acquired).
        """
        if demodulate:
            acquisition_frequency = self.get_if(readout_pulse)

            # DOWN Conversion
            n0 = 0
            n1 = self.ports["i1"].acquisition_duration
            input_vec_I = np.array(acquisition_results["acquisition"]["scope"]["path0"]["data"][n0:n1])
            input_vec_Q = np.array(acquisition_results["acquisition"]["scope"]["path1"]["data"][n0:n1])
            input_vec_I -= np.mean(input_vec_I)  # qblox does not remove the offsets in hardware
            input_vec_Q -= np.mean(input_vec_Q)

            modulated_i = input_vec_I
            modulated_q = input_vec_Q

            num_samples = modulated_i.shape[0]
            time = np.arange(num_samples) / PulseShape.SAMPLING_RATE

            cosalpha = np.cos(2 * np.pi * acquisition_frequency * time)
            sinalpha = np.sin(2 * np.pi * acquisition_frequency * time)
            demod_matrix = np.sqrt(2) * np.array([[cosalpha, sinalpha], [-sinalpha, cosalpha]])
            result = []
            for it, t, ii, qq in zip(np.arange(modulated_i.shape[0]), time, modulated_i, modulated_q):
                result.append(demod_matrix[:, :, it] @ np.array([ii, qq]))
            demodulated_signal = np.array(result)
            integrated_signal = np.mean(demodulated_signal, axis=0)

            # import matplotlib.pyplot as plt
            # plt.plot(input_vec_I[:400])
            # plt.plot(list(map(list, zip(*demodulated_signal)))[0][:400])
            # plt.show()
        else:
            i = np.mean(
                np.array(acquisition_results["acquisition"]["bins"]["integration"]["path0"])
                / self.ports["i1"].acquisition_duration
            )
            q = np.mean(
                np.array(acquisition_results["acquisition"]["bins"]["integration"]["path1"])
                / self.ports["i1"].acquisition_duration
            )
            integrated_signal = i, q
        return integrated_signal

    def start(self):
        """Empty method to comply with Instrument interface."""
        pass

    def stop(self):
        """Stops all sequencers"""
        try:
            self.device.stop_sequencer()
        except:
            pass

    def disconnect(self):
        """Empty method to comply with Instrument interface."""
        self._erase_device_parameters_cache()
        self._cluster = None
        self.is_connected = False
