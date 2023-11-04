from setuptools import setup, find_packages

setup(
    name="phrenktest",
    version="0.1.2",
    description="testest",
    author="test",
    packages=find_packages(),
    include_package_data=True,  # Include package data such as non-.py files
    data_files=[("", ["requirements.txt"])],
)