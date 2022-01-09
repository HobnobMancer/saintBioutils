#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) University of St Andrews 2020-2021
# (c) University of Strathclyde 2020-2021
# (c) James Hutton Institute 2020-2021
#
# Author:
# Emma E. M. Hobbs
#
# Contact
# eemh1@st-andrews.ac.uk
#
# Emma E. M. Hobbs,
# Biomolecular Sciences Building,
# University of St Andrews,
# North Haugh Campus,
# St Andrews,
# KY16 9ST
# Scotland,
# UK
#
# The MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Script containing functions to retrieve paths to files and directories"""


from pathlib import Path


def get_file_paths(directory, prefixes=None, suffixes=None):
    """Retrieve paths to all files in input dir.

    :param directory: Path, path to directory from which files are to be retrieved
    :param prefixes: List of Str, prefixes of the file names to be retrieved
    :param suffixes: List of Str, suffixes of the file names to be retrieved

    Returns list of paths to fasta files.
    """
    # create empty list to store the file entries, to allow checking if no files returned
    file_paths = []

    # retrieve all files from input directory
    files_in_entries = (entry for entry in Path(directory).iterdir() if entry.is_file())

    if prefixes is None and suffixes is None:
        for item in files_in_entries:
            file_paths.append(item)
    
    elif prefixes is not None and suffixes is None:
        for item in files_in_entries:
            for prefix in prefixes:
                if item.name.startswith(prefix):
                    file_paths.append(item)
    
    elif prefixes is None and suffixes is not None:
        for item in files_in_entries:
            for suffix in suffixes:
                if item.name.endswith(suffix):
                    file_paths.append(item)

    else:
        for item in files_in_entries:
            for suffix in suffixes:
                for prefix in prefixes:
                    if item.name.startswith(prefix) and item.name.endswith(suffix):
                        file_paths.append(item)

    return file_paths


def get_dir_paths(directory, prefixes=None, suffixes=None):
    """Retrieve paths to all directories in input dir.

    :param directory: Path, path to directory from which files are to be retrieved
    :param prefixes: List of Str, prefixes of the file names to be retrieved
    :param suffixes: List of Str, suffixes of the file names to be retrieved

    Returns list of paths to fasta files.
    """
    # create empty list to store the file entries, to allow checking if no files returned
    dir_paths = []

    # retrieve all files from input directory
    files_in_entries = (entry for entry in Path(directory).iterdir() if entry.is_dir())

    if prefixes is None and suffixes is None:
        for item in files_in_entries:
            dir_paths.append(item)
    
    elif prefixes is not None and suffixes is None:
        for item in files_in_entries:
            for prefix in prefixes:
                if item.name.startswith(prefix):
                    dir_paths.append(item)
    
    elif prefixes is None and suffixes is not None:
        for item in files_in_entries:
            for suffix in suffixes:
                if item.name.endswith(suffix):
                    dir_paths.append(item)

    else:
        for item in files_in_entries:
            for suffix in suffixes:
                for prefix in prefixes:
                    if item.name.startswith(prefix) and item.name.endswith(suffix):
                        dir_paths.append(item)

    return dir_paths
