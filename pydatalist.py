"""A list subclass for making working with datasets easier and more Pythonic.

Unlike an Ignition PyDataSet, this can be edited in place. It is a list with extras.
"""

import eztable
import system


class PyDataList(list):
	"""An extended list class with convenience methods and properties for use with datasets in Ignition.

	Can do anything list can do. isinstance() returns true for list. Plus more:
	The list of lists is in imitation of a pydataset. So, it should be rectangular and same number of
	columns and headers.

	pdsl = PyDataList(headers, list_of_lists)
	basic_dataset = pdsl.igds()
	pydataset = pdsl.pyds()
	number_of_columns = pdsl.cols() # from the current headers
	headers = pdsl.headers
	headers_as_ascii = pdsl.aheaders()
	"""

	def __init__(self, **kwargs):
		super(PyDataList, self).__init__(kwargs['data_list'])
		self.in_list = kwargs['data_list']
		self.headers = kwargs['headers']

	def __string__(self):
		return self.table()

	def pyds(self):
		"""Get a pydataset from the PyDataList."""

		std_ds = self.igds()
		return system.dataset.toPyDataSet(std_ds)

	def igds(self):
		"""Get a standard Ignition dataset from the PyDataList."""

		return system.dataset.toDataSet(self.headers, self.in_list)

	def cols(self):
		"""Get the number of columns."""

		return len(self.headers)

	def aheaders(self):
		"""Get the headers as ascii, not unicode."""

		return [x.encode('ascii', 'ignore') for x in self.headers]

	def headers(self):
		"""Get the headers property. So, both pylist.headers and pylist.headers() work."""

		return self.headers

	def table(self):
		"""Get the data as an EZ Table table."""

		return eztable.Table(self.headers, self.in_list)

	def findr(self, find_value, column=0, report_row_index=None, test_fn=None):
		"""Get the first row that has a matching value in the searched column. Default is leftmost column.

		Uses Shared.L.get_ds_row()
		"""

		return utils.get_ds_row(self.pyds(),
								find_value,
								column_to_search=column,
								report_row_index=report_row_index,
								test_fn=test_fn)
