import networkx as nx
from qibo import gates
from qibo.models import Circuit

from qibolab.transpilers.abstract import Optimizer


class Preprocessing(Optimizer):
    """Match the number of qubits of the circuit with the number of qubits of the chip if possible.

    Args:
        connectivity (nx.Graph): hardware chip connectivity.
    """

    def __init__(self, connectivity: nx.Graph):
        self.connectivity = connectivity

    def __call__(self, circuit: Circuit) -> Circuit:
        physical_qubits = self.connectivity.number_of_nodes()
        logical_qubits = circuit.nqubits
        if logical_qubits > physical_qubits:
            raise ValueError("The number of qubits in the circuit can't be greater than the number of physical qubits.")
        if logical_qubits == physical_qubits:
            return circuit
        new_circuit = Circuit(physical_qubits)
        for gate in circuit.queue:
            new_circuit.add(gate)
        return new_circuit


class Rearrange(Optimizer):
    """Rearranges gates using qibo's fusion algorithm.
    May reduce number of SWAPs when fixing for connectivity
    but this has not been tested.
    """

    def __init__(self, max_qubits: int = 1):
        self.max_qubits = max_qubits

    def __call__(self, circuit: Circuit):
        fcircuit = circuit.fuse(max_qubits=self.max_qubits)
        new = circuit.__class__(circuit.nqubits)
        for fgate in fcircuit.queue:
            if isinstance(fgate, gates.FusedGate):
                new.add(gates.Unitary(fgate.matrix(), *fgate.qubits))
            else:
                new.add(fgate)
        return new
