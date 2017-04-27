#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# 
# Author: Gabriele Girelli
# Email: gigi.ga90@gmail.com
# Version: 1.0.0
# Description: produce a bed with chromosome bins.
# ------------------------------------------------------------------------------



# DEPENDENCIES =================================================================

import argparse
import numpy as np
import os
import pandas as pd
import sys

# PARAMETERS ===================================================================

# Add script description
parser = argparse.ArgumentParser(
	description = 'Bin a chromosome into a bed file.'
)

# Add params
parser.add_argument('chrlen', metavar = 'chrlen', type = str, nargs = 1,
	help = 'Path to file with chromosome lengths (chr, length)' +
	' or chromosome length.')
parser.add_argument('chr', metavar = 'chr', type = str, nargs = 1,
	help = 'The chromosome to bin. E.g., chr1')

# Add flags
parser.add_argument('--binsize', metavar = 'bsi', type = int, nargs = 1,
	default = [1e6],
	help = 'Bin size. Default: 1e6')
parser.add_argument('--binstep', metavar = 'bst', type = int, nargs = 1,
	default = [1e6],
	help = 'Bin step. Non-overlapping bins if equal to bin size. Default: 1e5')

# Parse arguments
args = parser.parse_args()

# Retrieve arguments
chrfile = args.chrlen[0]
schr = args.chr[0]
size = int(args.binsize[0])
step = int(args.binstep[0])

if 0 == size:
	sys.exit('!!! ERROR !!! Cannot bin chromosome with bin size of 0.')

if step > size:
	sys.exit('!!! ERROR !!! Cannot bin chromosome with bin step > bin size.')

# FUNCTIONS ====================================================================

# RUN ==========================================================================

if os.path.isfile(chrfile):
	# Read chromosome length file
	lengths = pd.read_csv(chrfile, '\t', names = ['chr', 'len'])
	chrlen = lengths[lengths['chr'] == schr]['len']
else:
	try:
		# Convert string to chromosome length (integer)
		chrlen = int(chrfile)
	except ValueError:
		# Trigger exception
		sys.exit('!!! ERROR !!! The provided parameter is neither a file' +
			' nor an integer (chr length).')

# Calculate bin borders
starts = np.arange(0, int(chrlen) - size, step)
ends = starts + size

# Generate bin names
names = ['bin_' + str(i) for i in range(len(starts))]

# Produce output bedfile
out = pd.DataFrame(
	data = np.transpose([np.tile(schr, starts.shape[0]), starts, ends, names]),
	index = np.arange(starts.shape[0]),
	columns = ['chr', 'start', 'end', 'name']
)

# Print output bedfile
for i in range(out.shape[0]):
	print('\t'.join(out.iloc[i, :].astype('str').tolist()))

# END ==========================================================================

################################################################################