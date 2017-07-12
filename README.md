bed-tools-gg
===

A few scripts to manage bed files, more details on the format are available [here](https://genome.ucsc.edu/FAQ/FAQformat.html#format1).

Cheers!

└[∵┌]└[ ∵ ]┘[┐∵]┘

## @TODO

* Convert non-Python scripts to Python.
* Move scripts code to modules.
* Implement main script.

## Folder:

* **Lib** contains function libraries, shared by modules and scripts.
* **Mods** contains modules, used by the main script.
* **Scripts** contains single scripts.

## Single scripts

### `2matrix.sh`

```
 usage: ./bed2matrix.sh [-hn] [BEDFILEs]...

 Description:
  Merge bedfiles into a matrix. The score column is merged based on the positon
  given by the chr+start+end columns (default) or by the name column (-n option)

 Notes:
  Output is NOT in bed format.

 Mandatory arguments:
  BEDFILEs  Bed file(s). Expected to be ordered per condition.

 Optional arguments:
  -h    Show this help page.
  -n    Merge bedfiles based on name instead of location.
```

### `add_name.sh`

```
 usage: ./bed_add_name.sh [-h][-p prefix] -b bedfile

 Description:
  Add the name column to the provided bedfile in the format prefix_i, where i
  is the index of the row. The output is in bed format.

 Mandatory arguments:
  -b bedfile  Path to the bed file.

 Optional arguments:
  -h    Show this help page.
  -p prefix Prefix to use for the name. Default: 'roi_'
```

### `add_rois.py`

```
 usage: add_rois.py [-h] [-u] [-m] [-l] [-o outfile] [-N] regfile bedfile
 
 Assigns rows in a bed file to a given list of regions of interest (ROIs). ROIs
 can be overlapping. A new column is added to the end of the bed file, with all
 regions containing it, in the chr:start-end format, space-separated. Output is
 NOT in bed format.
 
 positional arguments:
   regfile        Path to bedfile, containing regions to be assigned to.
   bedfile        Path to bedfile, containing rows to be assigned.
 
 optional arguments:
   -h, --help     show this help message and exit
   -u             Keep bedfile rows that do not match any region.
   -m             Assign to bedfile rows that partially match a region.
   -l             Assign to bedfile rows that include a region.
   -o outfile     Output file (not a bed). Output to stdout if not specified.
   -N, --usename  Use ROI name instead of ROI coordinates.
```

### `bin.py`

```
 usage: bin.py [-h] [-c {min,mean,median,max,count,sum}] [-u] [-m] [-l]
               [-o outfile]
               regfile bedfile
 
 Assign bed rows to Region of Interest (ROIs) and collapse them. Every row in
 the bedfile is assigned to a ROI from the regfile. Then, the file is collapsed
 to have a single row per ROI. Rows can be collapsed in different ways: sum,
 max, min, median, mean, count. The output is in bed format.
 
 positional arguments:
   regfile               Path to bedfile, containing regions to be assigned to.
   bedfile               Path to bedfile, containing rows to be assigned.
 
 optional arguments:
   -h, --help            show this help message and exit
   -c {min,mean,median,max,count,sum}, --collapse {min,mean,median,max,count,sum}
                         Collapse method. Default: sum
   -u                    Keep bedfile rows that do not match any region.
   -m                    Assign to bedfile rows that partially match a region.
   -l                    Assign to bedfile rows that include a region.
   -o outfile            Output file (not a bed). Output to stdout if not
                         specified.
```

### `gen_bin.py`

```
 usage: gen_bin.py [-h] [-c chr] [-i bsi] [-t bst] [-d DELIM] [-l] [-A]
                   [-o outfile]
                   chrlen
 
 Generate bin bed file. Bin a single chromosome by specifying the chromosome
 with -c, either its length as chrlen, or a file containing it. Bin the whole
 genome using the -A option. Add an additional final bin, which extends over
 the end of a chromosome, to avoid excluding the final portion when the
 chromosome length is not divisible by the bin size. The output is in bed
 format.
 
 positional arguments:
   chrlen                Path to file with chromosome lengths (chr, length) or
                         chromosome length.
 
 optional arguments:
   -h, --help            show this help message and exit
   -c chr, --chr chr     The chromosome to bin. E.g., chr1. Not needed if -A is
                         used. Default: chr1
   -i bsi, --binsize bsi
                         Bin size. Default: 1e6
   -t bst, --binstep bst
                         Bin step. Non-overlapping bins if equal to bin size.
                         Default: 1e5
   -d DELIM, --delim DELIM
                         Delim of chrlen file. Used also for output. Default:
                         TAB
   -l, --lastbin         Make additional last bin over the chromosome end to
                         avoid excluding the last portion.
   -A, --allchr          Run on every chromosome.
   -o outfile            Output file (not a bed). Output to stdout if not
                         specified.
```

### `rep.sh`

```
 usage: ./bed_rep.sh [-h][-c colID][-d del] -b bedfile

 Description:
  Repeat a bedfile row as many times as specified in the score column.
  Following the bed format, the score column should be the 5th column.
  If not, specify the index of the column using the -c option.
  The output is in bed format.

 Mandatory arguments:
  -b bedfile  Bed file.

 Optional arguments:
  -h    Show this help page.
  -c colID  Column index (1-indexed). [Default: 5]
  -d del  Column delimiter. [Default: TAB]
```

### `shuffle.py`

```
 usage: shuffle.py [-h] [-k] [-n nIter] [-p perc] [-o outDir] seed bedfile
 
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

### `shuffle_multiple.sh`

```
 usage: ./beds_shuffle.sh [-h][-n nIter][-p perc][-o outDir] -s seed [BEDFILE]...

 Description:
  Shuffle a certain percentage of reads in the given bed files.

 Mandatory arguments:
  -s seed Seed for random number generation.
  BEDFILE Bed file(s). In any order.

 Optional arguments:
  -h  Show this help page.
  -n nIter  Number of iterations. Default: 100
  -p perc Percentage of reads to shuffle. Default: 10
  -o outDir Output directory. Default: ./shuffled/
```
