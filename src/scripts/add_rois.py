#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# 
# Author: Gabriele Girelli
# Email: gigi.ga90@gmail.com
# Version: 1.0.1
# Description: 	Assigns rows in a bed file to a given list of regions of
# 				interest (ROIs). The ROIs can be overlapping. A new column is
# 				added to the end of the bed file, with all the regions
# 				containing it, in the chr:start-end format, space-separated.
# 
# ------------------------------------------------------------------------------



# DEPENDENCIES =================================================================

import argparse
import os
import pandas as pd
import sys

# Loaded local bed-tools-gg python library
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../lib/')
import bed_lib as bd

# Change pandas default options
pd.options.mode.chained_assignment = None  # default='warn'

# INPUT ========================================================================

# Add script description
parser = argparse.ArgumentParser(description = """
Assigns rows in a bed file to a given list of regions of interest (ROIs). ROIs
can be overlapping. A new column is added to the end of the bed file, with all
regions containing it, in the chr:start-end format, space-separated.
Output is NOT in bed format.
""")

# Add params
parser.add_argument('regfile', type = str, nargs = 1,
	help = 'Path to bedfile, containing regions to be assigned to.')
parser.add_argument('bedfile', type = str, nargs = 1,
	help = 'Path to bedfile, containing rows to be assigned.')

# Add flags
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
parser.add_argument('-N', '--usename',
	action = 'store_const', dest = 'use_name',
	const = True, default = False,
	help = 'Use ROI name instead of ROI coordinates.')

# Parse arguments
args = parser.parse_args()

# Retrieve arguments
regfile = args.regfile[0]
bedfile = args.bedfile[0]
keep_unassigned_rows = args.u
keep_marginal_overlaps = args.m
keep_including = args.l
use_name = args.use_name
outfile = args.o[0]

# Default variables
bedcolnames = ['chr', 'start', 'end', 'name', 'score']

# RUN ==========================================================================

# Read regions file
rois = pd.read_csv(regfile, '\t', names = bedcolnames)

# Read bed file
bed = pd.read_csv(bedfile, '\t', names = bedcolnames, skiprows = [0])

# Assign rois to bed rows
bed = bd.assign_to_rois(rois, bed, keep_unassigned_rows, keep_marginal_overlaps,
	keep_including, use_name)

# Output
if False == outfile:
	for i in range(bed.shape[0]):
		print('\t'.join(bed.iloc[i, :].astype('str').tolist()))
else:
	bed.to_csv(outfile, sep = '\t', header = False, index = False)

# END --------------------------------------------------------------------------

################################################################################
