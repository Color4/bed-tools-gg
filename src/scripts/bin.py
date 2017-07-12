#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# 
# Author: Gabriele Girelli
# Email: gigi.ga90@gmail.com
# Version: 1.0.0
# Description: assign bed rows to regions and collapse rows.
# ------------------------------------------------------------------------------



# DEPENDENCIES =================================================================

import argparse
import numpy as np
import os
import pandas as pd
import sys

# Loaded local bed-tools-gg python library
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../lib/')
import bed_lib as bd

# Change pandas default options
pd.options.mode.chained_assignment = None  # default='warn'

# PARAMETERS ===================================================================

# Add script description
parser = argparse.ArgumentParser(description = '''
Assign bed rows to Region of Interest (ROIs) and collapse them.
Every row in the bedfile is assigned to a ROI from the regfile.
Then, the file is collapsed to have a single row per ROI.
Rows can be collapsed in different ways: sum, max, min, median, mean, count.
The output is in bed format.
''')

# Add params
parser.add_argument('regfile', type = str, nargs = 1,
	help = 'Path to bedfile, containing regions to be assigned to.')
parser.add_argument('bedfile', type = str, nargs = 1,
	help = 'Path to bedfile, containing rows to be assigned.')

# Add flags
parser.add_argument('-c', '--collapse', type = str, nargs = 1,
	choices = ['min', 'mean', 'median', 'max', 'count', 'sum'],
	help = '''Collapse method. Default: sum''',
	default = ['sum'])
parser.add_argument('-u',
	action = 'store_const', const = True, default = False,
	help = 'Keep bedfile rows that do not match any region.')
parser.add_argument('-m',
	action = 'store_const', const = True, default = False,
	help = 'Assign to bedfile rows that partially match a region.')
parser.add_argument('-l',
	action = 'store_const', const = True, default = False,
	help = 'Assign to bedfile rows that include a region.')
parser.add_argument('-o', metavar = 'outfile', type = str, nargs = 1,
	default = [False],
	help = 'Output file (not a bed). Output to stdout if not specified.')

# Parse arguments
args = parser.parse_args()

# Retrieve arguments
regfile = args.regfile[0]
bedfile = args.bedfile[0]
selected_collapse = args.collapse[0]
keep_unassigned_rows = args.u
keep_marginal_overlaps = args.m
keep_including = args.l
use_name = True
outfile = args.o[0]

# Default variables
bedcolnames = ['chr', 'start', 'end', 'name', 'score']

# RUN ==========================================================================

# Read regions file
rois = pd.read_csv(regfile, '\t', names = bedcolnames)

# Read bed file
bed = pd.read_csv(bedfile, '\t', names = bedcolnames, skiprows = [0])

# Assign rois to bed rows
rois = bd.assign_to_rois(rois, bed, keep_unassigned_rows,
	keep_marginal_overlaps, keep_including, use_name, selected_collapse)

# Output
if False == outfile:
	for i in range(rois.shape[0]):
		print('\t'.join(rois.iloc[i, :].astype('str').tolist()))
else:
	rois.to_csv(outfile, sep = '\t', header = False, index = False)

# END ==========================================================================

################################################################################