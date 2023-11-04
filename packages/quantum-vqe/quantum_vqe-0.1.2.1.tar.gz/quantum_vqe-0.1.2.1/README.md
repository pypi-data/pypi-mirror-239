# Quantum VQE Package

The Quantum VQE (Variational Quantum Eigensolver) package is a Python library for simulating the VQE algorithm on quantum computers. It utilizes the Qiskit framework to create and optimize quantum circuits that estimate the ground state energy of a given Hamiltonian.

# Features

- Implementation of the VQE algorithm using Qiskit.
- Functions to create variational ansatzes for quantum circuits.
- Optimization routines to find the minimum eigenvalue of the Hamiltonian.
- Utilities for validating input Hamiltonians.

# Installation

Before installing the Quantum VQE package, ensure that you have Python 3.7 or higher and pip installed.

To install the Quantum VQE package, run the following command in your terminal:
```
pip install git+https://github.com/SweatyCrayfish/quantum_vqe.git
```
Alternatively, you can clone the repository and install the package locally:
```bash
git clone https://github.com/SweatyCrayfish/quantum_vqe.git
cd quantum_vqe
pip install .
```
# Usage

Here is a simple example of how to use the Quantum VQE package to find the ground state energy of a Hamiltonian:
```python
from qiskit.opflow import X, Z, I
from quantum_vqe.vqe import create_vqe_ansatz, optimize_vqe
from qiskit import Aer
```
Define your Hamiltonian. For example, for a simple 2-qubit system:
```python
hamiltonian = (X ^ X) + (Z ^ I)
Define the quantum backend
backend = Aer.get_backend('statevector_simulator')
circuit, parameters = create_vqe_ansatz(num_qubits=2)
Optimize the circuit parameters
result = optimize_vqe(circuit, hamiltonian, backend)
print(f"Ground state energy: {result.fun}")
```
For more detailed examples, please refer to the examples/ directory in the repository.

# Development

To contribute to the Quantum VQE package, you can clone the repository and set up a development environment:
```bash
git clone https://github.com/SweatyCrayfish/quantum_vqe.git
cd quantum_vqe
pip install -e .
```
# Testing

To run the tests for the Quantum VQE package, navigate to the package root and execute:
```
python -m unittest discover tests
```
# License

This project is licensed under the MIT License - see the LICENSE file for details.

# Authors

- Viktor Veselov - Initial work

# Acknowledgments

- The Qiskit community for providing the framework to build upon.

# Citation

If you use this package in your research, please cite it as follows:

@misc{quantum_vqe,
  author = {Viktor Veselov},
  title = {Quantum VQE: A Variational Quantum Eigensolver Package},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {url{https://github.com/SweatyCrayfish/quantum_vqe}}
}