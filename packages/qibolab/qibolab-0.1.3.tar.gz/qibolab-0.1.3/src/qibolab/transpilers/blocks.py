from typing import Optional, Union

from qibo import Circuit
from qibo.gates import Gate


class BlockingError(Exception):
    """Raise when an error occurs in the blocking procedure"""


class Block:
    """A block contains a subset of gates acting on two qubits.

    Args:
        qubits (tuple): qubits where the block is acting.
        gates (list): list of gates that compose the block.
        name (str or int): name of the block.

    Properties:
        entangled (bool): True if the block entangles the qubits (there is at least one two qubit gate).
    """

    def __init__(self, qubits: tuple, gates: list, name: Optional[Union[str, int]] = None):
        self.qubits = qubits
        self.gates = gates
        self.name = name

    @property
    def entangled(self):
        return self.count_2q_gates() > 0

    def rename(self, name):
        """Rename block"""
        self.name = name

    def add_gate(self, gate: Gate):
        """Add a new gate to the block."""
        if not set(gate.qubits).issubset(self.qubits):
            raise BlockingError(
                "Gate acting on qubits {} can't be added to block acting on qubits {}.".format(
                    gate.qubits, self._qubits
                )
            )
        self.gates.append(gate)

    def count_2q_gates(self):
        """Return the number of two qubit gates in the block."""
        return count_2q_gates(self.gates)

    @property
    def qubits(self):
        """Return a sorted tuple with qubits of the block."""
        return tuple(sorted(self._qubits))

    @qubits.setter
    def qubits(self, qubits):
        self._qubits = qubits

    def fuse(self, block: "Block", name: str = None):
        """Fuse the current block with a new one, the qubits they are acting on must coincide.

        Args:
            block (:class:`qibolab.transpilers.blocks.Block`): block to fuse.
            name (str): name of the fused block.

        Return:
            fused_block (:class:`qibolab.transpilers.blocks.Block`): fusion of the two input blocks.
        """
        if not self.qubits == block.qubits:
            raise BlockingError("In order to fuse two blocks their qubits must coincide.")
        return Block(qubits=self.qubits, gates=self.gates + block.gates, name=name)

    def on_qubits(self, new_qubits):
        """Return a new block acting on the new qubits.

        Args:
            new_qubits (tuple): new qubits where the block is acting.
        """
        qubits_dict = dict(zip(self.qubits, new_qubits))
        new_gates = [gate.on_qubits(qubits_dict) for gate in self.gates]
        return Block(qubits=new_qubits, gates=new_gates, name=self.name)

    # TODO: use real QM properties to check commutation
    def commute(self, block: "Block"):
        """Check if a block commutes with the current one.

        Args:
            block (:class:`qibolab.transpilers.blocks.Block`): block to check commutation.

        Return:
            True if the two blocks don't share any qubit.
            False otherwise.
        """
        if len(set(self.qubits).intersection(block.qubits)) > 0:
            return False
        return True

    # TODO
    def kak_decompose(self):  # pragma: no cover
        """Return KAK decomposition of the block.
        This should be done only if the block is entangled and the number of
        two qubit gates is higher than the number after the decomposition.
        """
        raise NotImplementedError


class CircuitBlocks:
    """A CircuitBlocks contains a quantum circuit decomposed in two qubits blocks.

    Args:
        circuit (qibo.models.Circuit): circuit to be decomposed.
        index_names (bool): assign names to the blocks
    """

    def __init__(self, circuit: Circuit, index_names: bool = False):
        self.block_list = block_decomposition(circuit)
        self._index_names = index_names
        if index_names:
            for index, block in enumerate(self.block_list):
                block.rename(index)
        self.qubits = circuit.nqubits

    def __call__(self):
        return self.block_list

    def search_by_index(self, index: int):
        """Find a block from its index, requires index_names == True"""
        if not self._index_names:
            raise BlockingError("You need to assign index names in order to use search_by_index.")
        for block in self.block_list:
            if block.name == index:
                return block
        raise BlockingError("No block found with index {}.".format(index))

    def add_block(self, block: "Block"):
        """Add a two qubits block."""
        if not set(block.qubits).issubset(range(self.qubits)):
            raise BlockingError("The block can't be added to the circuit because it acts on different qubits")
        self.block_list.append(block)

    def circuit(self):
        """Return the quantum circuit."""
        circuit = Circuit(self.qubits)
        for block in self.block_list:
            for gate in block.gates:
                circuit.add(gate)
        return circuit

    def remove_block(self, block: "Block"):
        """Remove a block from the circuit blocks."""
        try:
            self.block_list.remove(block)
        except ValueError:
            raise BlockingError("The block you are trying to remove is not present in the circuit blocks.")


def block_decomposition(circuit: Circuit, fuse: bool = True):
    """Decompose a circuit into blocks of gates acting on two qubits.

    Args:
        circuit (qibo.models.Circuit): circuit to be decomposed.
        fuse (bool): fuse adjacent blocks acting on the same qubits.

    Return:
        blocks (list): list of blocks that act on two qubits.
    """
    if circuit.nqubits < 2:
        raise BlockingError("Only circuits with at least two qubits can be decomposed with block_decomposition.")
    initial_blocks = initial_block_decomposition(circuit)
    if not fuse:
        return initial_blocks
    blocks = []
    while len(initial_blocks) > 0:
        first_block = initial_blocks[0]
        remove_list = [first_block]
        if len(initial_blocks[1:]) > 0:
            for second_block in initial_blocks[1:]:
                try:
                    first_block = first_block.fuse(second_block)
                    remove_list.append(second_block)
                except BlockingError:
                    if not first_block.commute(second_block):
                        break
        blocks.append(first_block)
        remove_gates(initial_blocks, remove_list)
    return blocks


def initial_block_decomposition(circuit: Circuit):
    """Decompose a circuit into blocks of gates acting on two qubits.
    This decomposition is not minimal.

    Args:
        circuit (qibo.models.Circuit): circuit to be decomposed.

    Return:
        blocks (list): list of blocks that act on two qubits.
    """
    blocks = []
    all_gates = list(circuit.queue)
    two_qubit_gates = count_multi_qubit_gates(all_gates)
    while two_qubit_gates > 0:
        for idx, gate in enumerate(all_gates):
            if len(gate.qubits) == 2:
                qubits = gate.qubits
                block_gates = _find_previous_gates(all_gates[0:idx], qubits)
                block_gates.append(gate)
                block_gates.extend(_find_successive_gates(all_gates[idx + 1 :], qubits))
                block = Block(qubits=qubits, gates=block_gates)
                remove_gates(all_gates, block_gates)
                two_qubit_gates -= 1
                blocks.append(block)
                break
            elif len(gate.qubits) > 2:
                raise BlockingError("Gates targeting more than 2 qubits are not supported.")
    # Now we need to deal with the remaining spare single qubit gates
    while len(all_gates) > 0:
        first_qubit = all_gates[0].qubits[0]
        block_gates = gates_on_qubit(gatelist=all_gates, qubit=first_qubit)
        remove_gates(all_gates, block_gates)
        # Add other single qubits if there are still single qubit gates
        if len(all_gates) > 0:
            second_qubit = all_gates[0].qubits[0]
            second_qubit_block_gates = gates_on_qubit(gatelist=all_gates, qubit=second_qubit)
            block_gates += second_qubit_block_gates
            remove_gates(all_gates, second_qubit_block_gates)
            block = Block(qubits=(first_qubit, second_qubit), gates=block_gates)
        # In case there are no other spare single qubit gates create a block using a following qubit as placeholder
        else:
            block = Block(qubits=(first_qubit, (first_qubit + 1) % circuit.nqubits), gates=block_gates)
        blocks.append(block)
    return blocks


def gates_on_qubit(gatelist, qubit):
    """Return a list of all single qubit gates in gatelist acting on a specific qubit."""
    selected_gates = []
    for gate in gatelist:
        if gate.qubits[0] == qubit:
            selected_gates.append(gate)
    return selected_gates


def remove_gates(gatelist, remove_list):
    """Remove all gates present in remove_list from gatelist."""
    for gate in remove_list:
        gatelist.remove(gate)


def count_2q_gates(gatelist: list):
    """Return the number of two qubit gates in a list of gates."""
    return len([gate for gate in gatelist if len(gate.qubits) == 2])


def count_multi_qubit_gates(gatelist: list):
    """Return the number of multi qubit gates in a list of gates."""
    return len([gate for gate in gatelist if len(gate.qubits) >= 2])


def _find_successive_gates(gates: list, qubits: tuple):
    """Return a list containing all gates acting on qubits until a new two qubit gate acting on qubits is found."""
    successive_gates = []
    for qubit in qubits:
        for gate in gates:
            if (len(gate.qubits) == 1) and (gate.qubits[0] == qubit):
                successive_gates.append(gate)
            elif (len(gate.qubits) == 2) and (qubit in gate.qubits):
                break
    return successive_gates


def _find_previous_gates(gates: list, qubits: tuple):
    """Return a list containing all gates acting on qubits."""
    previous_gates = []
    for gate in gates:
        if gate.qubits[0] in qubits:
            previous_gates.append(gate)
    return previous_gates
