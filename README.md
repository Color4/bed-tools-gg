bed-tools-gg
===

A few scripts to manage bed files, more details on the format are available [here](https://genome.ucsc.edu/FAQ/FAQformat.html#format1).

Cheers!

└[∵┌]└[ ∵ ]┘[┐∵]┘

## `./bed2matrix.sh`

```
 usage: ./bed2matrix.sh [-hn] [BEDFILEs]...

 Description:
  Merge bedfiles into a matrix. The score column is merged based on the positon
  given by the chr+start+end columns (default) or by the name column (-n option)

 Mandatory arguments:
  BEDFILEs  Bed file(s). Expected to be ordered per condition.

 Optional arguments:
  -h        Show this help page.
  -n        Merge bedfiles based on name instead of location.
```

## `./bed_add_name.sh`

```
 usage: ./bed_add_name.sh [-h][-p prefix] -b bedfile

 Description:
  Add the name column to the provided bedfile in the format prefix_i, where i
  is the index of the row.

 Mandatory arguments:
  -b bedfile  Path to the bed file.

 Optional arguments:
  -h    Show this help page.
  -p prefix Prefix to use for the name. Default: 'roi_'
```

## `./bed_add_rois.py`

```
usage: bed_add_rois.py [-h] [-u] [-m] [-l] regfile bedfile outfile

Assigns rows in a bed file to a given list of regions of interest (ROIs). The
ROIs can be overlapping. A new column is added to the end of the bed file,
with all the regions containing it, in the chr:start-end format, space-
separated.

positional arguments:
  regfile     Path to bedfile, containing regions to be assigne to.
  bedfile     Path to bedfile, containing rows to be assigned.
  outfile     Output file (not a bed).

optional arguments:
  -h, --help  show this help message and exit
  -u          Keep bedfile rows that do not match any region.
  -m          Keep bedfile rows that do match a region partially.
  -l          Keep bedfile rows that include a region.
```

## ` ./bed_mkbin.py`

```
usage: bed_mkbin.py [-h] [-c chr] [-i bsi] [-t bst] [-d DELIM] [-l] [-A]
                    chrlen

Bin chromosome(s) into a bed file.

positional arguments:
  chrlen                Path to file with chromosome lengths (chr, length) or
                        chromosome length.

optional arguments:
  -h, --help            show this help message and exit
  -c chr, --chr chr     The chromosome to bin. E.g., chr1.
                        Not needed if -A isused.
                        Default: chr1
  -i bsi, --binsize bsi
                        Bin size. Default: 1e6
  -t bst, --binstep bst
                        Bin step. Non-overlapping bins if equal to bin size.
                        Default: 1e5
  -d DELIM, --delim DELIM
                        Delim of chrlen file. Used also for output.
                        Default: TAB
  -l, --lastbin         Make additional last bin over the chromosome end to
                        avoid excluding the last portion.
  -A, --allchr          Run on every chromosome.
```

## `./bed_rep.sh`

```
 usage: ./bed_rep.sh [-h][-c colID][-d del] -b bedfile

 Description:
  Repeat a bedfile row as many times as specified in the score column.
  Following the bed format, the score column should be the 5th column.
  If not, specify the index of the column using the -c option.

 Mandatory arguments:
  -b bedfile  Bed file.

 Optional arguments:
  -h          Show this help page.
  -c colID    Column index (1-indexed). [Default: 5]
  -d del      Column delimiter. [Default: TAB]
```

## `./bed_shuffle.py`

Shuffle the reads (i.e., the score values) of the score column of a bed file. The score values are not merely shuffled but considered as read counts, then the reads are shuffled.

Saves the current random number generator seed status at the end of the script in `OUTDIR/.seed_state.pickle`. Subsequent runs of the script, with the same `OUTDIR`, will NOT re-load the seed status unless `-k` is used.

```
usage: bed_shuffle.py [-h] [-k] [-n nIter] [-p perc] [-o outDir] seed bedfile

Shuffle bed file read counts.

positional arguments:
  seed        Seed for random number generation.
  bedfile     Path to bedfile.

optional arguments:
  -h, --help  show this help message and exit
  -k          Reload previous seed state. Use on subsequent runs.
  -n nIter    Number of iterations.
  -p perc     Percentage of reads to shuffle.
  -o outDir   Output directory.
```

## `./beds_shuffle.sh`

Runs `bed_shuffle.R` on the given bedfile(s). The initial seed is consistently kept through the R script runs as it is saved and re-loaded.

```
 usage: ./beds_shuffle.sh [-h][-n nIter][-p perc][-o outDir]
                          -s seed [BEDFILE]...

 Description:
  Shuffle a certain percentage of reads in the given bed files.

 Mandatory arguments:
  -s seed   Seed for random number generation.
  BEDFILE   Bed file(s). In any order.

 Optional arguments:
  -h    Show this help page.
  -n nIter  Number of iterations. Default: 100
  -p perc   Percentage of reads to shuffle. Default: 10
  -o outDir Output directory. Default: ./shuffled/
  -t threads    Number of threads for parallelization. Default: 1
```
