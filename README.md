# saintBioutils

[![DOI](https://zenodo.org/badge/423782407.svg)](https://zenodo.org/badge/latestdoi/423782407)

Repository containing utility and miscellaneous scripts and functions for use in bioinformatic pipelines, primarily written in Python3.

The name is derived from the primary host organisation (University of St Andrews) when the repo was firsted established.

## Table of contents
<!-- TOC -->
- [Installation](#installation)
- [Directories](#directories)
- [Copyright and License](#copyright-and-license)
<!-- /TOC -->

## Installation

### Quick and Easy

The easiest way to install `saintBioutils` and include the (sub)modules and functions is to install the package via `pip`, using the following command:  
```bash
pip3 install saintBioutils
```
This ensures all dependencies are installed

### From Source

To install from source, clone the repository:
```bash
git clone https://github.com/HobnobMancer/saintBioutils.git
```
Then install the package, which ensures all dependencies are also installed:  
```bash
python3 <path to the setup.py file>
```

## Directories

- `genbank` - Scripts for downloading and parsing genomic assemblies from NCBI GenBank
- `uniprot` - Scripts and functions related to calling to, retrieving from and parsing data from UniProt and its API
- `utilities` - Script and functions for utility functions for script/program utility operations

## Copyright and License

MIT License

Copyright (c) 2020-2021 University of St Andrews  
Copyright (c) 2020-2021 University of Strathclyde  
Copyright (c) 2020-2021 UJames Hutton Institute  
