from typing import Optional, List
from qiskit import QuantumCircuit
from qiskit.algorithms.exceptions import AlgorithmError
import numpy as np
import numpy.typing as npt


class BatchDirectHadammardTest:
    r"""Class that execute batches of Hadammard Test"""

    def __init__(self, hdmr_list: List):
        """Create a single container that computes many hadamard tests

        Args:
            hdrm_list (List): A list of DirectHadamardTest instances
        """
        self.hdmr_list = hdmr_list
        self.circuits = [hdmr.circuits for hdmr in hdmr_list]
        self.post_processing = hdmr_list[0].post_processing
        self.shots = hdmr_list[0].shots

    def get_values(self, sampler, parameter_sets: List, zne_strategy=None) -> List:
        """Compute the value of the test

        Args:
            sampler (Estimator): an sampler instance
            parameter_sets (List): The list of parameter values for the circuit

        Returns:
            List: values of the batched Hadammard Tests
        """

        ncircuits = len(self.circuits)

        try:
            if zne_strategy is None:
                job = sampler.run(
                    self.circuits,
                    [parameter_sets] * ncircuits,
                    shots=self.shots,
                )
            else:
                job = sampler.run(
                    self.circuits,
                    [parameter_sets] * ncircuits,
                    shots=self.shots,
                    zne_strategy=zne_strategy,
                )

            results = self.post_processing(job.result())
        except Exception as exc:
            raise AlgorithmError(
                "The primitive to evaluate the Hadammard Test failed!"
            ) from exc

        return results


class DirectHadamardTest:
    r"""Class to compute the direct measurement for Hadammard Test"""

    def __init__(
        self,
        operators: QuantumCircuit,
        apply_initial_state: Optional[QuantumCircuit] = None,
        shots: Optional[int] = 4000,
    ):
        r"""Create the quantum circuits required to compute the hadamard test:

        .. math::

            \\langle \\Psi | U | \\Psi \\rangle

        in case where U is a Pauli string and therefore we can use a deirect measurement

        Args:
            operators (QuantumCircuit): quantum circuit that represent the operator
            apply_initial_state (Optional[QuantumCircuit], optional): Quantum Circuit to create
                |Psi> from |0>. If None, assume that the qubits are alredy in Psi.
        """

        self.num_qubits = operators.num_qubits
        if apply_initial_state is not None:
            if apply_initial_state.num_qubits != operators.num_qubits:
                raise ValueError(
                    "The operator and the initial state circuits \
                        have different numbers of qubits"
                )

        # build the circuits
        self.circuits = self._build_circuit(
            operators,
            apply_initial_state,
        )

        # number of shots
        self.shots = shots

    def _build_circuit(
        self,
        operator: QuantumCircuit,
        apply_initial_state: Optional[QuantumCircuit] = None,
    ) -> QuantumCircuit:
        """build the quantum circuits

        Args:
            operators (List[QuantumCircuit]): quantum circuit or list of quantum circuits
                representing the U.
            use_barrier (bool): introduce barriers in the description of the circuits.
            apply_initial_state (Optional[QuantumCircuit], optional): Quantum Circuit to
                create |Psi> from |0>. If None, assume that the qubits are alredy in Psi.
                Defaults to None.


        Returns:
            QuantumCircuit: quamtum circuit required to compute the Hadammard Test.
        """
        if apply_initial_state is not None:
            circuit = apply_initial_state.compose(operator)
        else:
            circuit = QuantumCircuit(operator.num_qubits)
            circuit.append(operator, range(operator.num_qubits))
        circuit.measure_all()

        return circuit

    def post_processing(self, sampler_result) -> npt.NDArray[np.cdouble]:
        """Post process the sampled values of the circuits

        Args:
            sampler_result (results): Result of the sampler

        Returns:
            List: value of the overlap hadammard test
        """

        quasi_dist = sampler_result.quasi_dists
        val = []
        for qdist in quasi_dist:
            # add missing keys
            val.append(
                np.array(
                    [qdist[k] if k in qdist else 0 for k in range(2**self.num_qubits)]
                )
            )

        return np.array(val)

    def get_value(
        self, sampler, parameter_sets: List, zne_strategy=None
    ) -> npt.NDArray[np.cdouble]:
        """Compute the value of the test

        Args:
            sampler (sampler): a sampler instance
            parameter_sets (List): The list of parameter values for the circuit

        Returns:
            List: value of the test
        """

        try:
            if zne_strategy is None:
                job = sampler.run(
                    self.circuits,
                    parameter_sets,
                    shots=self.shots,
                )
            else:
                job = sampler.run(
                    self.circuits,
                    parameter_sets,
                    shots=self.shots,
                    zne_strategy=zne_strategy,
                )
            results = self.post_processing(job.result())

        except Exception as exc:
            raise AlgorithmError(
                "The primitive to evaluate the Hadammard Test failed!"
            ) from exc

        return results
