from setuptools import setup, find_packages

setup(
    name="quantum_vqe",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["qiskit", "numpy", "scipy"],
    author="Viktor Veselov",
    description="A quantum VQE package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SweatyCrayfish/quantum_vqe",
)
