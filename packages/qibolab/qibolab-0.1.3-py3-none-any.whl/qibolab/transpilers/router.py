from copy import deepcopy

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from more_itertools import pairwise
from qibo import gates
from qibo.config import log, raise_error
from qibo.models import Circuit

from qibolab.transpilers.abstract import Router, find_gates_qubits_pairs
from qibolab.transpilers.blocks import Block, CircuitBlocks
from qibolab.transpilers.placer import assert_placement


class ConnectivityError(Exception):
    """Raise for an error in the connectivity"""


def assert_connectivity(connectivity: nx.Graph, circuit: Circuit):
    """Assert if a circuit can be executed on Hardware.
    No gates acting on more than two qubits.
    All two qubit operations can be performed on hardware

    Args:
        circuit (qibo.models.Circuit): circuit model to check.
        connectivity (networkx.graph): chip connectivity.
    """

    for gate in circuit.queue:
        if len(gate.qubits) > 2 and not isinstance(gate, gates.M):
            raise ConnectivityError(f"{gate.name} acts on more than two qubits.")
        if len(gate.qubits) == 2:
            if (gate.qubits[0], gate.qubits[1]) not in connectivity.edges:
                raise ConnectivityError("Circuit does not respect connectivity. " f"{gate.name} acts on {gate.qubits}.")


# TODO: make this class work with CircuitMap
class ShortestPaths(Router):
    """A class to perform initial qubit mapping and connectivity matching.

    Properties:
        sampling_split (float): fraction of paths tested (between 0 and 1).

    Attributes:
        connectivity (networkx.Graph): chip connectivity.
        verbose (bool): print info messages.
        initial_layout (dict): initial physical to logical qubit mapping
        added_swaps (int): number of swaps added to the circuit to match connectivity.
        _gates_qubits_pairs (list): quantum circuit represented as a list (only 2 qubit gates).
        _mapping (dict): circuit to physical qubit mapping during transpiling.
        _graph (networkx.graph): qubit mapped as nodes of the connectivity graph.
        _qubit_map (np.array): circuit to physical qubit mapping during transpiling as vector.
        _circuit_position (int): position in the circuit.

    """

    def __init__(self, connectivity: nx.Graph, sampling_split=1.0, verbose=False):
        self.connectivity = connectivity
        self.sampling_split = sampling_split
        self.verbose = verbose
        self.initial_layout = None
        self._added_swaps = 0
        self.final_map = None
        self._gates_qubits_pairs = None
        self._mapping = None
        self._swap_map = None
        self._added_swaps_list = []
        self._graph = None
        self._qubit_map = None
        self._transpiled_circuit = None
        self._circuit_position = 0

    def __call__(self, circuit: Circuit, initial_layout):
        """Circuit connectivity matching.

        Args:
            circuit (qibo.models.Circuit): circuit to be matched to hardware connectivity.
            initial_layout (dict): initial qubit mapping.

        Returns:
            hardware_mapped_circuit (qibo.models.Circuit): circut mapped to hardware topology.
            final_mapping (dict): final qubit mapping.
        """
        self._mapping = initial_layout
        init_qubit_map = np.asarray(list(initial_layout.values()))
        self.initial_checks(circuit.nqubits)
        self._gates_qubits_pairs = find_gates_qubits_pairs(circuit)
        self._mapping = dict(zip(range(len(initial_layout)), initial_layout.values()))
        self._graph = nx.relabel_nodes(self.connectivity, self._mapping)
        self._qubit_map = np.sort(init_qubit_map)
        self._swap_map = deepcopy(init_qubit_map)
        self.first_transpiler_step(circuit)
        while len(self._gates_qubits_pairs) != 0:
            self.transpiler_step(circuit)
        hardware_mapped_circuit = self.remap_circuit(np.argsort(init_qubit_map), original_circuit=circuit)
        final_mapping = {"q" + str(j): self._swap_map[j] for j in range(self._graph.number_of_nodes())}
        return hardware_mapped_circuit, final_mapping

    def transpiler_step(self, qibo_circuit):
        """Transpilation step. Find new mapping, add swap gates and apply gates that can be run with this configuration.

        Args:
            qibo_circuit (qibo.models.Circuit): circuit to be transpiled.
        """
        len_before_step = len(self._gates_qubits_pairs)
        path, meeting_point = self.relocate()
        self.add_swaps(path, meeting_point)
        self.update_qubit_map()
        self.add_gates(qibo_circuit, len_before_step - len(self._gates_qubits_pairs))

    def first_transpiler_step(self, qibo_circuit):
        """First transpilation step. Apply gates that can be run with the initial qubit mapping.

        Args:
            qibo_circuit (qibo.models.Circuit): circuit to be transpiled.
        """
        self._circuit_position = 0
        self._added_swaps = 0
        self._added_swaps_list = []
        len_2q_circuit = len(self._gates_qubits_pairs)
        self._gates_qubits_pairs = self.reduce(self._graph)
        self.add_gates(qibo_circuit, len_2q_circuit - len(self._gates_qubits_pairs))

    @property
    def sampling_split(self):
        return self._sampling_split

    @sampling_split.setter
    def sampling_split(self, sampling_split):
        """Set the sampling split.

        Args:
            sampling_split (float): define fraction of shortest path tested.
        """

        if 0.0 < sampling_split <= 1.0:
            self._sampling_split = sampling_split
        else:
            raise_error(ValueError, "Sampling_split must be in (0:1].")

    def reduce(self, graph):
        """Reduce the circuit, delete a 2-qubit gate if it can be applied on the current configuration.

        Args:
            graph (networkx.Graph): current hardware qubit mapping.

        Returns:
            new_circuit (list): reduced circuit.
        """
        new_circuit = self._gates_qubits_pairs.copy()
        while new_circuit != [] and (new_circuit[0][0], new_circuit[0][1]) in graph.edges():
            del new_circuit[0]
        return new_circuit

    def map_list(self, path):
        """Return all possible walks of qubits, or a fraction, for a given path.

        Args:
            path (list): path to move qubits.

        Returns:
            mapping_list (list): all possible walks of qubits, or a fraction of them based on self.sampling_split, for a given path.
            meeting_point_list (list): qubit meeting point for each path.
        """
        path_ends = [path[0], path[-1]]
        path_middle = path[1:-1]
        mapping_list = []
        meeting_point_list = []
        test_paths = range(len(path) - 1)
        if self.sampling_split != 1.0:
            test_paths = np.random.choice(
                test_paths, size=int(np.ceil(len(test_paths) * self.sampling_split)), replace=False
            )
        for i in test_paths:
            values = path_middle[:i] + path_ends + path_middle[i:]
            mapping = dict(zip(path, values))
            mapping_list.append(mapping)
            meeting_point_list.append(i)
        return mapping_list, meeting_point_list

    def relocate(self):
        """A small greedy algorithm to decide which path to take, and how qubits should walk.

        Returns:
            final_path (list): best path to move qubits.
            meeting_point (int): qubit meeting point in the path.
        """
        nodes = self._graph.number_of_nodes()
        circuit = self.reduce(self._graph)
        final_circuit = circuit
        keys = list(range(nodes))
        final_graph = self._graph
        final_mapping = dict(zip(keys, keys))
        # Consider all shortest paths
        path_list = [p for p in nx.all_shortest_paths(self._graph, source=circuit[0][0], target=circuit[0][1])]
        self._added_swaps += len(path_list[0]) - 2
        # Here test all paths
        for path in path_list:
            # map_list uses self.sampling_split
            list_, meeting_point_list = self.map_list(path)
            for j, mapping in enumerate(list_):
                new_graph = nx.relabel_nodes(self._graph, mapping)
                new_circuit = self.reduce(new_graph)
                # Greedy looking for the optimal path and the optimal walk on this path
                if len(new_circuit) < len(final_circuit):
                    final_graph = new_graph
                    final_circuit = new_circuit
                    final_mapping = mapping
                    final_path = path
                    meeting_point = meeting_point_list[j]
        self._graph = final_graph
        self._mapping = final_mapping
        self._gates_qubits_pairs = final_circuit
        return final_path, meeting_point

    def initial_checks(self, qubits):
        """Initialize the transpiled circuit and check if it can be mapped to the defined connectivity.

        Args:
            qubits (int): number of qubits in the circuit to be transpiled.
        """
        nodes = self.connectivity.number_of_nodes()
        if qubits > nodes:
            raise_error(ValueError, "There are not enough physical qubits in the hardware to map the circuit.")
        if qubits == nodes:
            new_circuit = Circuit(nodes)
        else:
            if self.verbose:
                log.info(
                    "You are using more physical qubits than required by the circuit, some ancillary qubits will be added to the circuit."
                )
            new_circuit = Circuit(nodes)
        assert_placement(new_circuit, self._mapping)
        self._transpiled_circuit = new_circuit

    def add_gates(self, qibo_circuit: Circuit, matched_gates):
        """Add one and two qubit gates to transpiled circuit until connectivity is matched.

        Args:
            qibo_circuit (qibo.models.Circuit): circuit to be transpiled.
            matched_gates (int): number of two qubit gates that can be applied with the current qubit mapping.
        """
        index = 0
        while self._circuit_position < len(qibo_circuit.queue):
            gate = qibo_circuit.queue[self._circuit_position]
            if isinstance(gate, gates.M):
                measured_qubits = gate.qubits
                self._transpiled_circuit.add(
                    gate.on_qubits(
                        {measured_qubits[i]: self._qubit_map[measured_qubits[i]] for i in range(len(measured_qubits))}
                    )
                )
                self._circuit_position += 1
            elif len(gate.qubits) == 1:
                self._transpiled_circuit.add(gate.on_qubits({gate.qubits[0]: self._qubit_map[gate.qubits[0]]}))
                self._circuit_position += 1
            else:
                index += 1
                if index == matched_gates + 1:
                    break
                self._transpiled_circuit.add(
                    gate.on_qubits(
                        {
                            gate.qubits[0]: self._qubit_map[gate.qubits[0]],
                            gate.qubits[1]: self._qubit_map[gate.qubits[1]],
                        }
                    )
                )
                self._circuit_position += 1

    def add_swaps(self, path, meeting_point):
        """Add swaps to the transpiled circuit to move qubits.

        Args:
            path (list): path to move qubits.
            meeting_point (int): qubit meeting point in the path.
        """
        forward = path[0 : meeting_point + 1]
        backward = list(reversed(path[meeting_point + 1 :]))
        if len(forward) > 1:
            for f1, f2 in pairwise(forward):
                gate = gates.SWAP(self._qubit_map[f1], self._qubit_map[f2])
                self._transpiled_circuit.add(gate)
                self._added_swaps_list.append(gate)

        if len(backward) > 1:
            for b1, b2 in pairwise(backward):
                gate = gates.SWAP(self._qubit_map[b1], self._qubit_map[b2])
                self._transpiled_circuit.add(gate)
                self._added_swaps_list.append(gate)

    def update_swap_map(self, swap: tuple):
        """Update the qubit swap map."""
        temp = self._swap_map[swap[0]]
        self._swap_map[swap[0]] = self._swap_map[swap[1]]
        self._swap_map[swap[1]] = temp

    def update_qubit_map(self):
        """Update the qubit mapping after adding swaps."""
        old_mapping = self._qubit_map.copy()
        for key, value in self._mapping.items():
            self._qubit_map[value] = old_mapping[key]

    @property
    def added_swaps(self):
        """Number of added swaps during transpiling."""
        return self._added_swaps

    def remap_circuit(self, qubit_map, original_circuit: Circuit):
        """Map logical to physical qubits in a circuit.

        Args:
            circuit (qibo.models.Circuit): qibo circuit to be remapped.
            qubit_map (np.array): new qubit mapping.

        Returns:
            new_circuit (qibo.models.Circuit): transpiled circuit mapped with initial qubit mapping.
        """
        new_circuit = Circuit(self._transpiled_circuit.nqubits)
        for gate in self._transpiled_circuit.queue:
            new_circuit.add(gate.on_qubits({q: qubit_map[q] for q in gate.qubits}))
            if gate in self._added_swaps_list:
                self.update_swap_map(tuple(qubit_map[gate.qubits[i]] for i in range(2)))
        return new_circuit


class CircuitMap:
    """Class to keep track of the circuit and physical-logical mapping during routing,
    this class also implements the initial two qubit blocks decomposition.

    Args:
        initial_layout (dict): initial logical-physical qubit mapping.
        circuit (Circuit): circuit to be routed.

    Attributes:
        circuit_blocks (CircuitBlocks): list of two qubit blocks of the circuit.
        _physical_logical (list): current logical to physical qubit mapping.
        _circuit_logical (list): initial circuit to current logical circuit mapping.
        _routed_blocks (CircuitBlocks): current routed circuit blocks.
        _swaps (int): number of added swaps.
    """

    def __init__(self, initial_layout: dict, circuit: Circuit):
        self.circuit_blocks = CircuitBlocks(circuit, index_names=True)
        self._circuit_logical = list(range(len(initial_layout)))
        self._physical_logical = list(initial_layout.values())
        self._routed_blocks = CircuitBlocks(Circuit(circuit.nqubits))
        self._swaps = 0

    def blocks_qubits_pairs(self):
        """Return a list containing the qubit pairs of each block."""
        return [block.qubits for block in self.circuit_blocks()]

    def execute_block(self, block: Block):
        """Execute a block by removing it from the circuit representation
        and adding it to the routed circuit.
        """
        self._routed_blocks.add_block(block.on_qubits(self.get_physical_qubits(block)))
        self.circuit_blocks.remove_block(block)

    def routed_circuit(self):
        """Return qibo circuit of the routed circuit."""
        return self._routed_blocks.circuit()

    def final_layout(self):
        """Return the final physical-circuit qubits mapping."""
        unsorted_dict = {"q" + str(self.circuit_to_physical(i)): i for i in range(len(self._circuit_logical))}
        return dict(sorted(unsorted_dict.items()))

    def update(self, swap: tuple):
        """Update the logical-physical qubit mapping after applying a SWAP
        and add the SWAP gate to the routed blocks, the swap is represented by a tuple containing
        the logical qubits to be swapped.
        """
        physical_swap = self.logical_to_physical(swap)
        self._routed_blocks.add_block(Block(qubits=physical_swap, gates=[gates.SWAP(*physical_swap)]))
        self._swaps += 1
        idx_0, idx_1 = self._circuit_logical.index(swap[0]), self._circuit_logical.index(swap[1])
        self._circuit_logical[idx_0], self._circuit_logical[idx_1] = swap[1], swap[0]

    def get_logical_qubits(self, block: Block):
        """Return the current logical qubits where a block is acting"""
        return self.circuit_to_logical(block.qubits)

    def get_physical_qubits(self, block: Block or int):
        """Return the physical qubits where a block is acting."""
        if isinstance(block, int):
            block = self.circuit_blocks.search_by_index(block)
        return self.logical_to_physical(self.get_logical_qubits(block))

    def logical_to_physical(self, logical_qubits: tuple):
        """Return the physical qubits associated to the logical qubits."""
        return tuple(self._physical_logical.index(logical_qubits[i]) for i in range(2))

    def circuit_to_logical(self, circuit_qubits: tuple):
        """Return the current logical qubits associated to the initial circuit qubits."""
        return tuple(self._circuit_logical[circuit_qubits[i]] for i in range(2))

    def circuit_to_physical(self, circuit_qubit: int):
        """Return the current physical qubit associated to an initial circuit qubit."""
        return self._physical_logical.index(self._circuit_logical[circuit_qubit])


MAX_ITER = 10000


class Sabre(Router):
    def __init__(self, connectivity: nx.Graph, lookahead: int = 2, decay: float = 0.6):
        """Routing algorithm proposed in
        https://doi.org/10.48550/arXiv.1809.02573

        Args:
            connectivity (dict): hardware chip connectivity.
            lookahead (int): lookahead factor, how many dag layers will be considered in computing the cost.
            decay (float): value in interval [0,1].
                How the weight of the distance in the dag layers decays in computing the cost.
        """
        self.connectivity = connectivity
        self.lookahead = lookahead
        self.decay = decay
        self._dist_matrix = None
        self._dag = None
        self._front_layer = None
        self.circuit = None
        self._memory_map = None

    def __call__(self, circuit, initial_layout):
        """Route the circuit.

        Args:
            circuit (qibo.models.Circuit): circuit to be routed.
            initial_layout (dict): initial physical to logical qubit mapping.

        Returns:
            (qibo.models.Circuit): routed circuit.
        """
        self.preprocessing(circuit=circuit, initial_layout=initial_layout)
        while self._dag.number_of_nodes() != 0:
            execute_block_list = self.check_execution()
            if execute_block_list is not None:
                self.execute_blocks(execute_block_list)
            else:
                self.find_new_mapping()
        return self.circuit.routed_circuit(), self.circuit.final_layout()

    def preprocessing(self, circuit: Circuit, initial_layout):
        """The following objects will be initialised:
        - circuit: class to represent circuit and to perform logical-physical qubit mapping.
        - _dist_matrix: matrix reporting the shortest path lengh between all node pairs.
        - _dag: direct acyclic graph of the circuit based on commutativity.
        - _memory_map: list to remember previous SWAP moves.
        - _front_layer: list containing the blocks to be executed.
        """
        self.circuit = CircuitMap(initial_layout, circuit)
        self._dist_matrix = nx.floyd_warshall_numpy(self.connectivity)
        self._dag = create_dag(self.circuit.blocks_qubits_pairs())
        self._memory_map = []
        self.update_dag_layers()
        self.update_front_layer()

    def update_dag_layers(self):
        for layer, nodes in enumerate(nx.topological_generations(self._dag)):
            for node in nodes:
                self._dag.nodes[node]["layer"] = layer

    def update_front_layer(self):
        """Update the front layer of the dag."""
        self._front_layer = self.get_dag_layer(0)

    def get_dag_layer(self, n_layer):
        """Return the n topological layer of the dag."""
        return [node[0] for node in self._dag.nodes(data="layer") if node[1] == n_layer]

    @property
    def added_swaps(self):
        """Number of SWAP gates added to the circuit during routing"""
        return self.circuit._swaps

    def find_new_mapping(self):
        """Find the new best mapping by adding one swap."""
        candidates_evaluation = {}
        self._memory_map.append(deepcopy(self.circuit._circuit_logical))
        for candidate in self.swap_candidates():
            candidates_evaluation[candidate] = self.compute_cost(candidate)
        best_candidate = min(candidates_evaluation, key=candidates_evaluation.get)
        self.circuit.update(best_candidate)

    def compute_cost(self, candidate):
        """Compute the cost associated to a possible SWAP candidate."""
        temporary_circuit = deepcopy(self.circuit)
        temporary_circuit.update(candidate)
        if not self.check_new_mapping(temporary_circuit._circuit_logical):
            return float("inf")
        tot_distance = 0.0
        weight = 1.0
        for layer in range(self.lookahead + 1):
            layer_gates = self.get_dag_layer(layer)
            avg_layer_distance = 0.0
            for gate in layer_gates:
                qubits = temporary_circuit.get_physical_qubits(gate)
                avg_layer_distance += (self._dist_matrix[qubits[0], qubits[1]] - 1.0) / len(layer_gates)
            tot_distance += weight * avg_layer_distance
            weight *= self.decay
        return tot_distance

    def check_new_mapping(self, map):
        """Check that the candidate will generate a new qubit mapping in order to avoid ending up in infinite cycles.
        If the mapping is not new the cost associated to that candidate will be infinite."""
        if map in self._memory_map:
            return False
        return True

    def swap_candidates(self):
        """Return a list of possible candidate SWAPs (to be applied on logical qubits directly).
        The possible candidates are the ones sharing at least one qubit with a block in the front layer.
        """
        candidates = []
        for block in self._front_layer:
            qubits = self.circuit.get_physical_qubits(block)
            for qubit in qubits:
                for connected in self.connectivity.neighbors(qubit):
                    candidate = tuple(
                        sorted((self.circuit._physical_logical[qubit], self.circuit._physical_logical[connected]))
                    )
                    if candidate not in candidates:
                        candidates.append(candidate)
        return candidates

    def check_execution(self):
        """Check if some gatesblocks in the front layer can be executed in the current configuration.

        Returns:
            list of executable blocks if there are, None otherwise.
        """
        executable_blocks = []
        for block in self._front_layer:
            qubits = self.circuit.get_physical_qubits(block)
            if qubits in self.connectivity.edges or not self.circuit.circuit_blocks.search_by_index(block).entangled:
                executable_blocks.append(block)
        if len(executable_blocks) == 0:
            return None
        return executable_blocks

    def execute_blocks(self, blocklist: list):
        """Execute a list of blocks:
        -Remove the correspondent nodes from the dag and circuit representation.
        -Add the executed blocks to the routed circuit.
        -Update the dag layers and front layer.
        -Reset the mapping memory.
        """
        for block_id in blocklist:
            block = self.circuit.circuit_blocks.search_by_index(block_id)
            self.circuit.execute_block(block)
            self._dag.remove_node(block_id)
        self.update_dag_layers()
        self.update_front_layer()
        self._memory_map = []


def draw_dag(dag: nx.DiGraph, filename=None):  # pragma: no cover
    """Draw a direct acyclic graph in topological order.

    Args:
        dag (nx.DiGraph): dag to be shown
        filename (str): name of the saved image, if None the image will be showed.
    """
    for layer, nodes in enumerate(nx.topological_generations(dag)):
        for node in nodes:
            dag.nodes[node]["layer"] = layer
    pos = nx.multipartite_layout(dag, subset_key="layer")
    fig, ax = plt.subplots()
    nx.draw_networkx(dag, pos=pos, ax=ax)
    ax.set_title("DAG layout in topological order")
    fig.tight_layout()
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)


def create_dag(gates_qubits_pairs):
    """Create direct acyclic graph (dag) of the circuit based on two qubit gates commutativity relations.

    Args:
        gates_qubits_pairs (list): list of qubits tuples where gates/blocks acts.

    Returns:
        (nx.DiGraph): dag of the circuit.
    """
    dag = nx.DiGraph()
    dag.add_nodes_from(range(len(gates_qubits_pairs)))
    # Find all successors
    connectivity_list = []
    for idx, gate in enumerate(gates_qubits_pairs):
        saturated_qubits = []
        for next_idx, next_gate in enumerate(gates_qubits_pairs[idx + 1 :]):
            for qubit in gate:
                if (qubit in next_gate) and (not qubit in saturated_qubits):
                    saturated_qubits.append(qubit)
                    connectivity_list.append((idx, next_idx + idx + 1))
            if len(saturated_qubits) >= 2:
                break
    dag.add_edges_from(connectivity_list)
    return remove_redundant_connections(dag)


def remove_redundant_connections(dag: nx.Graph):
    """Remove redundant connection from a DAG unsing transitive reduction."""
    new_dag = nx.DiGraph()
    new_dag.add_nodes_from(range(dag.number_of_nodes()))
    transitive_reduction = nx.transitive_reduction(dag)
    new_dag.add_edges_from(transitive_reduction.edges)
    return new_dag
