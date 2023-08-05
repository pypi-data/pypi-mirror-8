#!/usr/bin/env python
#
# BioLite - Tools for processing gene sequence data and automating workflows
# Copyright (c) 2012-2014 Brown University. All rights reserved.
# 
# This file is part of BioLite.
# 
# BioLite is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# BioLite is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with BioLite.  If not, see <http://www.gnu.org/licenses/>.

import glob
import os
import wget
import shutil
import subprocess
import sys

from collections import defaultdict
from Bio import Entrez
from lxml import etree

from biolite import utils
from biolite.catalog import CatalogRecord
from biolite.config import get_resource_default


Entrez.email = get_resource_default('email', None)


def check_email():
	"""
	Check if the `email` field, required for Entrez queries, has been set.
	"""
	if Entrez.email is None:
		utils.die("""to make an Entrez query, you must either:
 1) set the field 'Entrez.email' manually
 2) set the 'email' resource in your BioLite configuration file""")


def ftp_url(id):
	"""
	Returns the URL for downloading the data for accession `id` from SRA's
	FTP server.
	"""
	return 'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/{0}/{1}/{2}/{2}.sra'.format(id[:3], id[:6], id)


def all_ids(id):
	"""
	Queries SRA via Entrez and returns all accession IDs associated with the
	given accession `id`.
	"""
	check_email()
	handle = Entrez.esearch(db='sra', MaxRet=100, term=id)
	record = Entrez.read(handle)
	return record['IdList']


def download_xmls(ids):
	"""
	Returns a list of XML files for the given list of SRA accession `ids`.
	"""
	check_email()
	return [Entrez.efetch(db='sra', id=i) for i in ids]


def xml_metadata(xml):	
	"""
	Returns a dict populated with the metadata from an SRA EXPERIMENT_PACKAGE
	`xml` file location, with fields matching those of the BioLite catalog. The
	`paths` entry contains a list of run accessions that need to be converted
	to URLs for downloading.
	"""
	package = etree.parse(xml)
	base = '//EXPERIMENT_PACKAGE_SET/EXPERIMENT_PACKAGE'
	record = {}

	# Helper function for retrieving text values if they exist.
	def get_text(key, path):
		result = package.xpath(base+path)
		if len(result):
			record[key] = result[0].text

	# Parse the sample attributes first, in case a key is defined that
	# conflicts with a catalog field name.
	for attr in package.xpath(base+'/SAMPLE/SAMPLE_ATTRIBUTES/SAMPLE_ATTRIBUTE'):
		children = attr.getchildren()
		record[children[0].text] = children[1].text

	# These should always be present.
	record['id'] = package.xpath(base+'/EXPERIMENT/@accession')[0]
	run_ids = package.xpath(base+'/RUN_SET/RUN/@accession')
	record['paths'] = run_ids
	record['library_id'] = '|'.join(run_ids)

	# Find other fields for populating the BioLite catalog.
	get_text('species', '/SAMPLE/SAMPLE_NAME/SCIENTIFIC_NAME')
	get_text('ncbi_id', '/SAMPLE/SAMPLE_NAME/TAXON_ID')
	get_text('library_type', '/EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_SOURCE')
	get_text('sequencer', '/EXPERIMENT/PLATFORM/ILLUMINA/INSTRUMENT_MODEL')

	seq_center = package.xpath(base+'/EXPERIMENT/@center_name')
	if seq_center: record['seq_center'] = seq_center[0]

	get_text('note', '/SAMPLE/DESCRIPTION')
	if record.get('note', 'None') == 'None': record['note'] = None

	get_text('sample_prep', '/EXPERIMENT/DESIGN/DESIGN_DESCRIPTION')

	return record


# Test
if __name__ == '__main__':
	ids = all_ids('SRP008975')
	print ids
	for xml in download_xmls(ids):
		print xml_metadata(xml)

