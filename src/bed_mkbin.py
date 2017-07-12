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
	description = 'Bin chromosome(s) into a bed file.'
)

# Add params
parser.add_argument('chrlen', metavar = 'chrlen', type = str, nargs = 1,
	help = 'Path to file with chromosome lengths (chr, length)' +
	' or chromosome length.')

# Add flags
parser.add_argument('-c', '--chr', metavar = 'chr', type = str, nargs = 1,
	help = '''The chromosome to bin. E.g., chr1.
	Not needed if -A is used. Default: chr1''',
	default = ["chr1"])
parser.add_argument('-i', '--binsize', metavar = 'bsi', type = int, nargs = 1,
	default = [1e6],
	help = 'Bin size. Default: 1e6')
parser.add_argument('-t', '--binstep', metavar = 'bst', type = int, nargs = 1,
	help = '''Bin step. Non-overlapping bins if equal to bin size.
	Default: 1e5''', default = [1e6])
parser.add_argument('-d', '--delim', type = str, nargs = 1,
	help = 'Delim of chrlen file. Used also for output. Default: TAB',
	default = ['\t'])
parser.add_argument('-l', '--lastbin',
	dest = 'last_bin', action = 'store_const',
	const = True, default = False,
	help = '''Make additional last bin over the chromosome end to avoid
	excluding the last portion.''')
parser.add_argument('-A', '--allchr',
	dest = 'all_chr', action = 'store_const',
	const = True, default = False,
	help = 'Run on every chromosome.')

# Parse arguments
args = parser.parse_args()

# Retrieve arguments
chrfile = args.chrlen[0]
schr = args.chr[0]
size = int(args.binsize[0])
step = int(args.binstep[0])
delim = args.delim[0]
last_bin = args.last_bin
all_chr = args.all_chr

if 0 == len(schr) and not all_chr:
	sys.exit('!!! ERROR !!! Chromosome needed if -A is not used.')

if 0 == size:
	sys.exit('!!! ERROR !!! Cannot bin chromosome with bin size of 0.')

if step > size:
	sys.exit('!!! ERROR !!! Cannot bin chromosome with bin step > bin size.')

# FUNCTIONS ====================================================================

def bin_chr(chrlen, size, step, last_bin):
	'''Generate bins covering a chromosome.

	Args:
		chrlen (int): chromosome length.
		size (int): bin size.
		step (int): bin step. Use step == size for not overlapping bins.
		last_bin (bool): whether to add extra final bin.

	Returns:
		pd.Dataframe: a chr-start-end-name table.
	'''

	# Calculate bin borders
	starts = np.arange(0, int(chrlen) - size, step)
	ends = starts + size - 1

	if last_bin:
		# Add last bin
		starts = starts.tolist()
		starts.append(starts[-1] + size)
		starts = np.array(starts)
		ends = ends.tolist()
		ends.append(ends[-1] + size)
		ends = np.array(ends)

	# Generate bin names
	names = ['bin_' + str(i + 1) for i in range(len(starts))]

	# Produce output bedfile
	out = pd.DataFrame(
		data = np.transpose([np.tile(schr, starts.shape[0]),
			starts, ends, names]),
		index = np.arange(starts.shape[0]),
		columns = ['chr', 'start', 'end', 'name']
	)

	# Output
	return(out)

# RUN ==========================================================================

if os.path.isfile(chrfile):
	# Read chromosome length file
	lengths = pd.read_csv(chrfile, delim, names = ['chr', 'len'])
	chrlen = lengths[lengths['chr'] == schr]['len']
else:
	try:
		# Convert string to chromosome length (integer)
		chrlen = int(chrfile)
	except ValueError:
		# Trigger exception
		sys.exit('!!! ERROR !!! The provided parameter is neither a file' +
			' nor an integer (chr length).')

if all_chr:
	# Bin every chromosome
	# Prepare empty dataframe list
	out = []

	# Run per chromosome
	for schr in lengths['chr']:
		chrlen = lengths[lengths['chr'] == schr]['len']
		out.append(bin_chr(chrlen, size, step, last_bin))

	# Concatenate dataframes
	out = pd.concat(out)

	# Update bin names
	out['name'] = out['chr'] + '_' + out['name']
else:
	# Bin specified chromosome
	out = bin_chr(chrlen, size, step, last_bin)

# Print output bedfile
for i in range(out.shape[0]):
	print(delim.join(out.iloc[i, :].astype('str').tolist()))

# END ==========================================================================

################################################################################