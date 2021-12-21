"""Contains a convenience wrapper functions for creating nested Python lists out of an Ignition dataset."""

from pydatalist import PyDataList


def pydl(pyds):
	"""From a py/dataset, create an extended-functionality python list.
	
	Can do anything list can do. isinstance() returns true for list. Plus more:
	The extended list has an additional attribute, a list which contains the headers.
	
	from Shared.ds.PyDS import pydl
	ext_list = pydl(dataset)
	
	pprint.pprint(pydl)
		[[Tue Mar 10 16:21:38 EDT 2020, 2069L, 10.073052635990704, None],
		[Tue Mar 10 16:22:37 EDT 2020, 2069L, 10.066964396434487, None],
		[Tue Mar 10 16:23:37 EDT 2020, 2114L, 10.060876156878273, None]]
	
	# convenience methods and properties
	# get this = using this
	basic_dataset = pydl.igds()
	pydataset = pydl.pyds()
	number_of_columns = pydl.cols() # from the current headers
	headers = pydl.headers()
	headers_as_ascii = pydl.aheaders()	# as they're frequently unicode, ignores non-ascii characters
	
	"""

	return_list, headers = ds_pl(pyds, headers=True)

	# return extended list object
	return PyDataList(data_list=return_list, headers=headers)


def ds_pl(dataset, headers=False):
	"""Get a nested Python list of lists from an Ignition DataSet or PyDataSet.

	:param dataset: any, the data object to convert
	:param headers: bool, whether to return a tuple of (the lists, the headers)
	:returns: list or tuple, (list, list) of the nested lists and headers
	"""

	from com.inductiveautomation.ignition.common.script.builtin.DatasetUtilities import PyDataSet
	from com.inductiveautomation.ignition.common import BasicDataset
	import system

	# ensure the dataset is in a PyDataSet
	if isinstance(dataset, BasicDataset):
		ds_headers = list(dataset.columnNames)
		dataset = system.dataset.toPyDataSet(dataset)
	elif isinstance(dataset, PyDataSet):
		ds_headers = list(dataset.columnNames)
	else:
		dataset = system.dataset.toPyDataSet(dataset)
		ds_headers = list(dataset.columnNames)

	# convert to nested lists
	try:
		nested_list = [[col for col in row] for row in dataset]
	except TypeError:
		nested_list = []
		for row in dataset:
			row_data = []
			for col in row:
				row_data += [col]
			nested_list += [row_data]

	if headers:
		return_this = nested_list, ds_headers
	else:
		return_this = nested_list

	return return_this
