from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.12"
]

setup (
    name="physics-gabri432",
    version="0.2.1",
    description="A package containing Physics formulas and constants for various calculations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Gabri432/python-physics",
    author="Gabriele Gatti",
    author_email="gabrielegatti432@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="physics, library, lib, relativity, thermodynamics, classical, gravity, electromagnetism, fluids",
    packages=find_packages(),
    install_requires=[""]

)