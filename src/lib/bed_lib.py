#
#

import numpy as np
import pandas as pd

def test_lib():
	'''To test if the library was properly loaded.'''
	print('Library loaded and ready!')

def join_trim(l):
	'''Join nested array.'''
	return ' '.join(' '.join(l).split())

def assign_to_rois(
	rois, bed,
	keep_unassigned_rows,
	keep_marginal_overlaps,
	keep_including,
	use_name,
	collapse_method = None
):
	'''Assign rows from bed to regions in rois.

	Args:
		rois (pd.DataFrame): bed file with regions of interest.
		bed (pd.DataFrame): bed file with regions to be assigned to ROIs.
		keep_unassigned_rows (bool): keep rows that do not belong to any ROI.
		keep_marginal_overlaps (bool): assign to partial overlaps.
		keep_including (bool): assign to included ROIs.
		use_name (bool): also use ROIs name.
		collapse_method (string): collapse method, default: sum.

	Returns:
		pd.DataFrame: bed file with added rois column or collapsed.
	'''

	# Assign collapse method for np.ndarray
	collapse_methods = {
		'min' : lambda x: np.min(x),
		'mean' : lambda x: np.mean(x),
		'median' : lambda x: np.median(x),
		'max' : lambda x: np.max(x),
		'count' : lambda x: x.shape[0],
		'sum' : lambda x: np.sum(x)
	}
	if not type(None) == type(collapse_method):
		collapse = collapse_methods[collapse_method]

	# Add regions column
	bed['rois'] = pd.Series(np.array(['' for i in range(bed.shape[0])]),
		index = bed.index)

	# Assign reads to rows
	chr_set = set(bed['chr'])
	for chri in chr_set:
		# Select rois and rows
		chr_bed = bed.iloc[np.where(bed['chr'] == chri)[0], :]
		chr_roi = rois.iloc[np.where(rois['chr'] == chri)[0], :]

		if 0 == chr_bed.shape[0] or 0 == chr_roi.shape[0]:
			continue

		# Prepare roi label
		chr_roi_labels = np.array(chr_roi['chr']).astype('str').tolist()
		chr_roi_labels = np.core.defchararray.add(chr_roi_labels, ':')
		chr_roi_labels = np.core.defchararray.add(chr_roi_labels,
			np.array(chr_roi['start']).astype('str').tolist())
		chr_roi_labels = np.core.defchararray.add(chr_roi_labels, '-')
		chr_roi_labels = np.core.defchararray.add(chr_roi_labels,
			np.array(chr_roi['end']).astype('str').tolist())
		if use_name:
			chr_roi_labels = np.core.defchararray.add(chr_roi_labels, ':')
			chr_roi_labels = np.core.defchararray.add(chr_roi_labels,
				np.array(chr_roi['name']).astype('str').tolist())

		# Build matrix ---------------------------------------------------------
		bed_hash_start = [hash(i) for i in chr_bed['start']]
		bed_hash_end = [hash(i) for i in chr_bed['end']]
		roi_hash_start = [hash(i) for i in chr_roi['start']]
		roi_hash_end = [hash(i) for i in chr_roi['end']]

		# Start should be higher than the region start
		condition_start = np.greater_equal.outer(bed_hash_start, roi_hash_start)

		# End should be lower than the region end
		condition_end = np.logical_not(
			np.greater.outer(bed_hash_end, roi_hash_end))

		# Perfectly contained (in)
		condition_in = np.logical_and(condition_start, condition_end)

		if keep_marginal_overlaps or keep_including:
			# Start should be lower than the region start
			condition_left_start = np.logical_not(condition_start)

			# End should be higher than the region end
			condition_right_end = np.logical_not(condition_end)

		if keep_marginal_overlaps:
			# End should be lower than the region end and higher than its start
			condition_left_end = np.logical_and(condition_end,
				np.greater_equal.outer(bed_hash_end, roi_hash_start))

			# Start should be higher than the region start
			# and lower than its end
			condition_right_start = np.logical_and(condition_start,
				np.logical_not(np.greater.outer(bed_hash_start, roi_hash_end)))

			# Partial overlap on left margin
			condition_left = np.logical_and(
				condition_left_start, condition_left_end)

			# Partial overlap on right margin
			condition_right = np.logical_and(
				condition_right_start, condition_right_end)

			# Partial overla on a margin
			condition_margins = np.logical_or(condition_left, condition_right)

			# Partial overlap or inside
			condition_in = np.logical_or(condition_in, condition_margins)

		if keep_including:
			# Rows that include the region
			condition_larger = np.logical_and(
				condition_left_start, condition_right_end)

			# Included (inside) or including
			condition_in = np.logical_or(condition_in, condition_larger)

		if 0 == condition_in.sum():
			continue

		if not type(None) == type(collapse_method):
			# Collapse row's score to ROIs
			rois['score'][chr_roi.index.values] = [
				collapse(chr_bed['score'][condition_in[:, coli]])
				for coli in range(condition_in.shape[1])]
		else:
			# Add rois per row
			labels = np.tile(chr_roi_labels, (condition_in.shape[0], 1))
			labels[np.logical_not(condition_in)] = ''
			bed['rois'][chr_bed.index.values] = [join_trim(labels[rowi, :])
				for rowi in range(labels.shape[0])]
	
	# Return collapsed ROI list
	if not type(None) == type(collapse_method):
		rois['score'][np.where(np.isnan(rois['score']))[0]] = 0
		rois['score'] = rois['score'].astype('int')
		return(rois)

	# Remove rows without regions
	if not keep_unassigned_rows:
		bed = bed[bed['rois'] != '']

	# Return bed with assigned ROIs (not bed anymore)
	return(bed)

def bin_chr(schr, chrlen, size, step, last_bin):
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
