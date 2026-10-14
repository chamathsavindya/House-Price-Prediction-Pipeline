from setuptools import find_packages,setup
from typing import List

"""
the setup.py is an essential part of packaging and distributing python projects. 
it is used by setuptools (or distutils in older python versions) to define 
the configuration of your project, such as its metadata , dependencies and more
"""


def get_requirements()->List[str]:
    requirements_list:List[str] = []
    try:
        with open("requirements.txt","r") as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement != "e .":
                    requirements_list.append(requirement)
        
    except FileNotFoundError:
        return "requirements.txt file is not fount"

    return requirements_list


setup (
    name = "housepriceprediction",
    version = "0.0.1",
    author = "chamathsavindya",
    author_email = "chamathsavinda10@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)