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
"""Functions relating to UniProt and its API"""


import logging
import urllib.parse
import urllib.request

from urllib.error import HTTPError

from tqdm import tqdm

from saintBioutils.misc import get_chunks_list


def get_uniprot_accessions(genbank_dict, args):
    """Retrieve UniProt accessions for the GenBank accessions from UniProt REST API.
    
    UniProt requests batch queries of no larger than 20,000, athough queries longer than 500
    often raise HTTP 400 Error codes, especially in busy server times.

    :param genbank_dict: dict, keyed by GenBank accessions and valued by local CAZyme db record id (int)
    :param args: cmd-line args parser

    Return dict of {uniprot_accession: {'gbk_acc': str, 'db_id': int}}
    """
    logger = logging.getLogger(__name__)
    uniprot_url = 'https://www.uniprot.org/uploadlists/'

    genbank_accessions = list(genbank_dict.keys())

    uniprot_rest_queries = get_chunks_list(genbank_accessions, args.uniprot_batch_size)

    uniprot_gbk_dict = {}  # {uniprot_accession: {'gbk_acc': str, 'db_id': int}}
    failed_queries = {}  # {query: tries}

    for query_chunk in tqdm(
        uniprot_rest_queries,
        desc='Batch retrieving UniProt IDs',
    ):
        if type(query_chunk) != str:
            # convert the set of gbk accessions into str format
            query = ' '.join(query_chunk)

        params = {
            'from': 'EMBL',
            'to': 'ACC',
            'format': 'tab',
            'query': query
        }

        # submit query data
        data = urllib.parse.urlencode(params)
        data = data.encode('utf-8')
        req = urllib.request.Request(uniprot_url, data)

        # retrieve UniProt response
        try:
            with urllib.request.urlopen(req) as f:
                response = f.read()
        except HTTPError:
            try:
                failed_queries[query] += 1
            except KeyError:
                failed_queries[query] = 1
            if failed_queries[query] > args.retries:
                del failed_queries[query]
            else:
                uniprot_rest_queries.append(query)

        uniprot_batch_response = response.decode('utf-8')

        uniprot_batch_response = uniprot_batch_response.split('\n')

        for line in tqdm(uniprot_batch_response[1:], "Parsing retrieved UniProt query"):  # the first line includes the titles, last line is an empty str
            if line == '':  # add check incase last line is not an empty str 
                continue
            uniprot_accession = line.split('\t')[1]
            genbank_accession = line.split('\t')[0]
            db_id = genbank_dict[genbank_accession]
            uniprot_gbk_dict[uniprot_accession] = {'gbk_acc': genbank_accession, 'db_id': db_id}

    logger.info(
        f"Retrieved {len(genbank_accessions)} gbk accessions from the local db\n"
        f"{len(list(uniprot_gbk_dict.keys()))} were assoicated with records in UniProt"
    )

    return uniprot_gbk_dict
 
