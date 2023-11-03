from dataclasses import dataclass

import numpy as np
from qibo.config import log, raise_error

from qibolab.instruments.port import Port

FREQUENCY_LIMIT = 500e6


@dataclass
class QbloxOutputPort_Settings:
    channel: str = None
    qubit: str = None
    attenuation: int = 60
    offset: float = 0.0
    hardware_mod_en: bool = True
    gain: float = 1.0
    nco_freq: int = 0
    nco_phase_offs: float = 0


@dataclass
class ClusterRF_OutputPort_Settings(QbloxOutputPort_Settings):
    lo_enabled: bool = True
    lo_frequency: int = 2_000_000_000


@dataclass
class ClusterBB_OutputPort_Settings(QbloxOutputPort_Settings):
    pass


@dataclass
class QbloxInputPort_Settings:
    channel: str = None
    acquisition_hold_off: int = 0
    acquisition_duration: int = 1000
    hardware_demod_en: bool = True


class QbloxOutputPort(Port):
    """qibolab.instruments.port.Port interface implementation for Qblox instruments"""

    def __init__(self, module, sequencer_number: int, number: int):
        self.module = module
        self.sequencer_number: int = sequencer_number
        self.port_number: int = number - 1
        self.channel = None  # To be discontinued
        self.qubit = None  # To be discontinued

        self._settings = QbloxOutputPort_Settings()

    @property
    def attenuation(self) -> str:
        """Attenuation that is applied to this port."""
        if self.module.device:
            self._settings.attenuation = self.module.device.get(f"out{self.port_number}_att")
        return self._settings.attenuation

    @attenuation.setter
    def attenuation(self, value):
        if isinstance(value, (float, np.floating)):
            value = int(value)
        if isinstance(value, (int, np.integer)):
            if value > 60:
                log.warning(f"Qblox attenuation needs to be between 0 and 60 dB. Adjusting {value} to 60dB")
                value = 60

            elif value < 0:
                log.warning(f"Qblox attenuation needs to be between 0 and 60 dB. Adjusting {value} to 0")
                value = 0

            if (value % 2) != 0:
                log.warning(
                    f"Qblox attenuation needs to be a multiple of 2 dB. Adjusting {value} to {round(value/2) * 2}"
                )
                value = round(value / 2) * 2
        else:
            raise_error(ValueError, f"Invalid attenuation {value}")

        self._settings.attenuation = value
        if self.module.device:
            self.module._set_device_parameter(self.module.device, f"out{self.port_number}_att", value=value)

    @property
    def offset(self):
        """DC offset that is applied to this port."""
        if self.module.device:
            self._settings.offset = self.module.device.get(f"out{self.port_number}_offset")
        return self._settings.offset

    @offset.setter
    def offset(self, value):
        if isinstance(value, (int, np.integer)):
            value = float(value)
        if isinstance(value, (float, np.floating)):
            if value > 2.5:
                log.warning(f"Qblox offset needs to be between -2.5 and 2.5 V. Adjusting {value} to 2.5 V")
                value = 2.5

            elif value < -2.5:
                log.warning(f"Qblox offset needs to be between -2.5 and 2.5 V. Adjusting {value} to -2.5 V")
                value = -2.5
        else:
            raise_error(ValueError, f"Invalid offset {value}")

        self._settings.offset = value
        if self.module.device:
            self.module._set_device_parameter(self.module.device, f"out{self.port_number}_offset", value=value)

    # Additional attributes needed by the driver
    @property
    def hardware_mod_en(self):
        """Flag to enable hardware modulation."""
        if self.module.device:
            self._settings.hardware_mod_en = self.module.device.sequencers[self.sequencer_number].get(f"mod_en_awg")
        return self._settings.hardware_mod_en

    @hardware_mod_en.setter
    def hardware_mod_en(self, value):
        if not isinstance(value, bool):
            raise_error(ValueError, f"Invalid hardware_mod_en {value}")

        self._settings.hardware_mod_en = value
        if self.module.device:
            self.module._set_device_parameter(
                self.module.device.sequencers[self.sequencer_number], "mod_en_awg", value=value
            )

    @property
    def nco_freq(self):
        """nco_freq that is applied to this port."""

        if self.module.device:
            self._settings.nco_freq = self.module.device.sequencers[self.sequencer_number].get(f"nco_freq")

        return self._settings.nco_freq

    @nco_freq.setter
    def nco_freq(self, value):
        if isinstance(value, (float, np.floating)):
            value = int(value)
        if isinstance(value, (int, np.integer)):
            if value > FREQUENCY_LIMIT:
                log.warning(
                    f"Qblox nco_freq needs to be between -{FREQUENCY_LIMIT} and {FREQUENCY_LIMIT} MHz. Adjusting {value} to {FREQUENCY_LIMIT} MHz"
                )
                value = int(FREQUENCY_LIMIT)

            elif value < -FREQUENCY_LIMIT:
                log.warning(
                    f"Qblox nco_freq needs to be between -{FREQUENCY_LIMIT} and {FREQUENCY_LIMIT} MHz. Adjusting {value} to -{FREQUENCY_LIMIT} MHz"
                )
                value = int(-FREQUENCY_LIMIT)
        else:
            raise_error(ValueError, f"Invalid nco_freq {value}")

        self._settings.nco_freq = value
        if self.module.device:
            self.module._set_device_parameter(
                self.module.device.sequencers[self.sequencer_number], "nco_freq", value=value
            )

    @property
    def nco_phase_offs(self):
        """nco_phase_offs that is applied to this port."""

        if self.module.device:
            self._settings.nco_phase_offs = self.module.device.sequencers[self.sequencer_number].get(f"nco_phase_offs")
        return self._settings.nco_phase_offs

    @nco_phase_offs.setter
    def nco_phase_offs(self, value):
        if isinstance(value, (int, np.integer)):
            value = float(value)
        if isinstance(value, (float, np.floating)):
            value = value % 360
        else:
            raise_error(ValueError, f"Invalid nco_phase_offs {value}")

        self._settings.nco_phase_offs = value
        if self.module.device:
            self.module._set_device_parameter(
                self.module.device.sequencers[self.sequencer_number], "nco_phase_offs", value=value
            )


class ClusterRF_OutputPort(QbloxOutputPort):
    def __init__(self, module, sequencer_number: int, number: int):
        super().__init__(module, sequencer_number, number)
        self._settings = ClusterRF_OutputPort_Settings()

    @property
    def lo_enabled(self):
        """Flag to enable local oscillator."""

        if self.module.device:
            if self.module.device.is_qrm_type:
                self._settings.lo_enabled = self.module.device.get(f"out{self.port_number}_in{self.port_number}_lo_en")
            elif self.module.device.is_qcm_type:
                self._settings.lo_enabled = self.module.device.get(f"out{self.port_number}_lo_en")
        return self._settings.lo_enabled

    @lo_enabled.setter
    def lo_enabled(self, value):
        if not isinstance(value, bool):
            raise_error(ValueError, f"Invalid lo_enabled {value}")

        self._settings.lo_enabled = value
        if self.module.device:
            if self.module.device.is_qrm_type:
                self.module._set_device_parameter(
                    self.module.device, f"out{self.port_number}_in{self.port_number}_lo_en", value=value
                )
            elif self.module.device.is_qcm_type:
                self.module._set_device_parameter(self.module.device, f"out{self.port_number}_lo_en", value=value)

    @property
    def lo_frequency(self):
        """Local oscillator frequency for the given port."""
        if self.module.device:
            if self.module.device.is_qrm_type:
                self._settings.lo_frequency = self.module.device.get(
                    f"out{self.port_number}_in{self.port_number}_lo_freq"
                )
            elif self.module.device.is_qcm_type:
                self._settings.lo_frequency = self.module.device.get(f"out{self.port_number}_lo_freq")
        return self._settings.lo_frequency

    @lo_frequency.setter
    def lo_frequency(self, value):
        if isinstance(value, (float, np.floating)):
            value = int(value)
        if isinstance(value, (int, np.integer)):
            if value > 18e9:
                log.warning(f"Qblox lo_frequency needs to be between 2e9 and 18e9 Hz. Adjusting {value} to 18e9 Hz")
                value = int(18e9)

            elif value < 2e9:
                log.warning(f"Qblox lo_frequency needs to be between 2e9 and 18e9 Hz. Adjusting {value} to 2e9 Hz")
                value = int(2e9)
        else:
            raise_error(ValueError, f"Invalid lo-frequency {value}")

        self._settings.lo_frequency = value
        if self.module.device:
            if self.module.device.is_qrm_type:
                self.module._set_device_parameter(
                    self.module.device, f"out{self.port_number}_in{self.port_number}_lo_freq", value=value
                )
            elif self.module.device.is_qcm_type:
                self.module._set_device_parameter(self.module.device, f"out{self.port_number}_lo_freq", value=value)

    # Note: for qublos, gain is equivalent to amplitude, since it does not bring any advantages
    # we plan to remove it soon.
    @property
    def gain(self):
        """Gain that is applied to this port."""

        if self.module.device:
            self._settings.gain = self.module.device.sequencers[self.sequencer_number].get(f"gain_awg_path0")
        return self._settings.gain

    @gain.setter
    def gain(self, value):
        if isinstance(value, (int, np.integer)):
            value = float(value)
        if isinstance(value, (float, np.floating)):
            if value > 1.0:
                log.warning(f"Qblox offset needs to be between -1 and 1. Adjusting {value} to 1")
                value = 1.0

            elif value < -1.0:
                log.warning(f"Qblox offset needs to be between -1 and 1. Adjusting {value} to -1")
                value = -1.0
        else:
            raise_error(ValueError, f"Invalid offset {value}")

        self._settings.gain = value
        if self.module.device:
            self.module._set_device_parameter(
                self.module.device.sequencers[self.sequencer_number], "gain_awg_path0", "gain_awg_path1", value=value
            )


class ClusterBB_OutputPort(QbloxOutputPort):
    # Note: for qblox, gain is equivalent to amplitude, since it does not bring any advantages
    # we plan to remove it soon.

    def __init__(self, module, sequencer_number: int, number: int):
        super().__init__(module, sequencer_number, number)
        self._settings = ClusterBB_OutputPort_Settings()

    @property
    def gain(self):
        """Gain that is applied to this port."""

        if self.module.device:
            self._settings.gain = self.module.device.sequencers[self.sequencer_number].get(f"gain_awg_path0")
        return self._settings.gain

    @gain.setter
    def gain(self, value):
        if isinstance(value, (int, np.integer)):
            value = float(value)
        if isinstance(value, (float, np.floating)):
            if value > 1.0:
                log.warning(f"Qblox offset needs to be between -1 and 1. Adjusting {value} to 1")
                value = 1.0

            elif value < -1.0:
                log.warning(f"Qblox offset needs to be between -1 and 1. Adjusting {value} to -1")
                value = -1.0
        else:
            raise_error(ValueError, f"Invalid offset {value}")

        self._settings.gain = value
        if self.module.device:
            self.module._set_device_parameter(
                self.module.device.sequencers[self.sequencer_number], "gain_awg_path0", value=value
            )


class QbloxInputPort:
    def __init__(self, module, output_sequencer_number: int, input_sequencer_number: int, number: int):
        self.module = module
        self.output_sequencer_number: int = output_sequencer_number
        self.input_sequencer_number: int = input_sequencer_number
        self.port_number: int = number - 1
        self.channel = None  # To be discontinued
        self.qubit = None  # To be discontinued

        self.acquisition_hold_off = 4  # To be discontinued

        self._settings = QbloxInputPort_Settings()

    @property
    def hardware_demod_en(self):
        """Flag to enable hardware demodulation."""

        if self.module.device:
            self._settings.hardware_demod_en = self.module.device.sequencers[self.input_sequencer_number].get(
                f"demod_en_acq"
            )
        return self._settings.hardware_demod_en

    @hardware_demod_en.setter
    def hardware_demod_en(self, value):
        if not isinstance(value, bool):
            raise_error(ValueError, f"Invalid hardware_demod_en {value}")

        self._settings.hardware_demod_en = value
        if self.module.device:
            self.module._set_device_parameter(
                self.module.device.sequencers[self.input_sequencer_number], "demod_en_acq", value=value
            )

    @property
    def acquisition_duration(self):
        """Duration of the pulse acquisition, in ns. It must be > 0 and multiple of 4."""

        if self.module.device:
            self._settings.acquisition_duration = self.module.device.sequencers[self.output_sequencer_number].get(
                f"integration_length_acq"
            )
        return self._settings.acquisition_duration

    @acquisition_duration.setter
    def acquisition_duration(self, value):
        if isinstance(value, (float, np.floating)):
            value = int(value)
        if isinstance(value, (int, np.integer)):
            if value < 4:
                log.warning(f"Qblox hardware_demod_en needs to be > 4ns. Adjusting {value} to 4 ns")
                value = 4
            if (value % 4) != 0:
                log.warning(
                    f"Qblox hardware_demod_en needs to be a multiple of 4 ns. Adjusting {value} to {round(value/4) * 4}"
                )
                value = round(value / 4) * 4

        else:
            raise_error(ValueError, f"Invalid acquisition_duration {value}")

        self._settings.acquisition_duration = value
        if self.module.device:
            self.module._set_device_parameter(
                self.module.device.sequencers[self.output_sequencer_number], "integration_length_acq", value=value
            )
