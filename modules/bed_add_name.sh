#!/usr/bin/env bash

# ------------------------------------------------------------------------------
# 
# Author: Gabriele Girelli
# Email: gigi.ga90@gmail.com
# Version: 1.0.1
# Description: 	add name column.
# 
# ------------------------------------------------------------------------------



# ENV VAR ======================================================================

export LC_ALL=C

# DEPENDENCIES =================================================================

function join_by { local IFS="$1"; shift; echo "$*"; }

# INPUT ========================================================================

# Help string
helps="
 usage: ./bed_add_name.sh [-h][-p prefix] -b bedfile

 Description:
  Add the name column to the provided bedfile in the format prefix_i, where i
  is the index of the row.

 Mandatory arguments:
  -b bedfile	Path to the bed file.

 Optional arguments:
  -h		Show this help page.
  -p prefix	Prefix to use for the name. Default: 'roi_'
"

# Default options
prefix="roi_"

# Parse options
while getopts hp:b: opt "${bedfiles[@]}"; do
	case $opt in
		h)
			echo -e "$helps\n"
			exit 0
		;;
		p)
			prefix="$OPTARG"
		;;
		b)
			if [ -e $OPTARG ]; then
				bedfile=$OPTARG
			else
				msg="!!! Invalid bedfile (-b), file not found."
				msg=$msg"\n    File: $OPTARG"
				echo -e " $helps\n$msg"
				exit 1
			fi
		;;
	esac
done

# Check mandatory options
if [ -z "$bedfile" ]; then
	msg="!!! No bedfile (-b) provided."
	echo -e "$helps\n$msg"
	exit 1
fi

# TEST =========================================================================

# RUN ==========================================================================

awkprogram='{
	OFS=FS="\t";
	print $1 OFS $2 OFS $3 OFS prefix NR;
}'

awk -v prefix="$prefix" "$awkprogram" <(cat $bedfile)

# End --------------------------------------------------------------------------

################################################################################
