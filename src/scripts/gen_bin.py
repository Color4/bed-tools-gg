#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# 
# Author: Gabriele Girelli
# Email: gigi.ga90@gmail.com
# Version: 1.0.0
# Description: generate a bed with chromosome bins.
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
Generate bin bed file.
Bin a single chromosome by specifying the chromosome with -c, either its length
as chrlen, or a file containing it. Bin the whole genome using the -A option.
Add an additional final bin, which extends over the end of a chromosome,
to avoid excluding the final portion when the chromosome length is not
divisible by the bin size.  The output is in bed format.
''')

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
parser.add_argument('-o', metavar = 'outfile', type = str, nargs = 1,
	default = [False],
	help = 'Output file (not a bed). Output to stdout if not specified.')

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
outfile = args.o[0]

if 0 == len(schr) and not all_chr:
	sys.exit('!!! ERROR !!! Chromosome needed if -A is not used.')

if 0 == size:
	sys.exit('!!! ERROR !!! Cannot bin chromosome with bin size of 0.')

if step > size:
	sys.exit('!!! ERROR !!! Cannot bin chromosome with bin step > bin size.')

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
		out.append(bd.bin_chr(chrlen, size, step, last_bin))

	# Concatenate dataframes
	out = pd.concat(out)

	# Update bin names
	out['name'] = out['chr'] + '_' + out['name']
else:
	# Bin specified chromosome
	out = bd.bin_chr(chrlen, size, step, last_bin)

# Output
if False == outfile:
	for i in range(out.shape[0]):
		print(delim.join(out.iloc[i, :].astype('str').tolist()))
else:
	out.to_csv(outfile, sep = delim, header = False, index = False)

# END ==========================================================================

################################################################################