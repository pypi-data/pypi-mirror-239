import qiskit
import numpy as np
import treelib
from scipy import sparse


class HTreeQST:
    def __init__(self, circuit, sampler, use_matrix_path=True):
        """Perform a QST for real valued state vector
        This needs only N additional circuits but require some posprocesing

        Args:
            circuit (QuantumCircuit): the base circuit we want to evaluate
            sampler (Sampler): A sampler primitive
        """
        # store the roots/leaves of each level for faster processing
        self.root = []
        self.leaf = []

        # circuit and size
        self.circuit = circuit
        self.num_qubits = circuit.num_qubits
        self.size = 2**self.num_qubits

        # get the full connection tree
        self.tree = self.get_tree()

        # get all the paths
        self.path_to_node = self.get_path()
        if use_matrix_path:
            self.path_matrix = self.get_path_sparse_matrix()
            self.idx_path_matrix = np.insert(
                np.cumsum(self.path_matrix.getnnz(axis=1)), 0, 0
            )
        else:
            self.path_matrix = None
            self.idx_path_matrix = None

        # sampler and circuits
        self.sampler = sampler
        self.list_circuits = self.get_circuits()
        self.ncircuits = len(self.list_circuits)

    def get_tree(self):
        """Compute the tree"""

        def init_tree():
            """_summary_

            Returns:
                _type_: _description_
            """
            trees = []
            level_root, level_leaf = [], []
            for i in range(int(self.size / 2)):
                tree = treelib.Tree()
                a, b = 2 * (i), 2 * (i) + 1
                tree.create_node(a, a, data=1)
                tree.create_node(b, b, parent=a)
                trees.append(tree)

                level_leaf.append(b)
                level_root.append(a)
            return trees, level_root, level_leaf

        def link_trees(trees):
            """_summary_

            Args:
                trees (_type_): _description_
            """
            ntree = len(trees)
            level_root, level_leaf = [], []
            for iter_ in range(1, self.num_qubits):
                root, leaf = [], []
                for iroot in range(0, int(ntree), 2**iter_):
                    new_root = trees[iroot].root
                    new_leaf = iroot + 2 ** (iter_ - 1)
                    trees[iroot].paste(new_root, trees[new_leaf])

                    root.append(trees[iroot].root)
                    leaf.append(trees[new_leaf].root)

                level_root.append(root)
                level_leaf.append(leaf)
            return trees[0], level_root, level_leaf

        tree_list, root, leaf = init_tree()
        self.root.append(root)
        self.leaf.append(leaf)
        tree, root, leaf = link_trees(tree_list)
        self.root += root
        self.leaf += leaf

        return tree

    def get_path(self):
        """_summary_"""
        paths = []
        for inode in range(self.size):
            paths.append(list(self.tree.rsearch(inode)))
        return paths

    def get_path_sparse_matrix(self):
        """transforms the path into a sparse matrix

        Returns:
            _type_: _description_
        """
        row_idx, col_idx, vals = [], [], []
        for ip, path in enumerate(self.path_to_node):
            num_nodes = len(path)
            row_idx += [ip] * num_nodes
            col_idx += path
            vals += [1] * num_nodes
        return sparse.coo_matrix(
            (vals, (row_idx, col_idx)), shape=(self.size, self.size)
        )

    def get_circuits(self):
        """_summary_

        Args:
            circuits (_type_): _description_
        """
        list_circuits = [self.circuit.measure_all(inplace=False)]

        for iq in range(self.num_qubits):
            qc = qiskit.QuantumCircuit(self.num_qubits)
            qc.append(self.circuit, range(self.num_qubits))
            qc.h(iq)
            list_circuits.append(qc.measure_all(inplace=False))
        return list_circuits

    def get_samples(self, parameters):
        """_summary_

        Args:
            sampler (_type_): _description_
        """
        results = (
            self.sampler.run(self.list_circuits, [parameters] * self.ncircuits)
            .result()
            .quasi_dists
        )
        samples = []
        for res in results:
            proba = np.zeros(2**self.num_qubits)
            for k, v in res.items():
                proba[k] = v
            samples.append(proba)
        return samples

    def get_weight(self, samples):
        """_summary_

        Args:
            samples (_type_): _description_
        """
        # root
        weights = np.zeros_like(samples[0])
        weights[0] = 1

        # link the weights
        for iter_ in range(0, self.num_qubits):
            roots = self.root[iter_]
            leafs = self.leaf[iter_]
            signs = np.sign(
                2 * samples[iter_ + 1][roots] - samples[0][roots] - samples[0][leafs]
            )
            weights[leafs] = signs

        return weights

    def get_signs(self, weights):
        """Agregate the signs of the statevector

        Args:
            weights (np.array):
        """

        # if the path is not known
        if self.path_matrix is None:
            signs = np.zeros_like(weights)
            for ip, path in enumerate(self.path_to_node):
                signs[ip] = weights[path].prod()
            return signs

        # otherwise use the path
        mat = self.path_matrix.multiply(weights)
        return np.multiply.reduceat(mat.data, self.idx_path_matrix[:-1])

    def get_relative_amplitude_sign(self, parameters):
        """_summary_

        Args:
            parameters (_type_): _description_
        """
        samples = self.get_samples(parameters)
        weights = self.get_weight(samples)
        return self.get_signs(weights)

    def get_statevector(self, parameters):
        """_summary_

        Args:
            parameters (_type_): _description_
        """
        samples = self.get_samples(parameters)
        amplitudes = np.sqrt(samples[0])
        weights = self.get_weight(samples)
        signs = self.get_signs(weights)
        return amplitudes * signs
