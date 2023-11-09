from setuptools import setup, find_packages

setup(
    name="my_module",
    version="1.0.3",
    packages=find_packages(include=["my_module", "my_module.*"]),
    install_requires=[],
    # Add other metadata like author, email, etc.
)