"""A pseudo-tag class to make interacting with tags easier, more concise, and readable."""

from Shared.pd import pydl

import utils


class Ptag(object):
	"""A convenience class for reading and writing tag values.
	
	A "psuedo tag" so: ptag
	a class which holds the path provided at creation (or set later) and has methods which read and
	write the value of the tag
		
	creating an instance:
		speedTag = Ptag("[default]NH1/NH1 Line Speed")

	read and write like so:
		speedTag.val = 9001
		print(speedTag.val)
		>9001
		
	or like so:
		speedTag.write(100)
		currentSpeed = speedTag.read()
		print(currentSpeed)
		>100.0

		
	change which tag it references by reassigning speedTag as creating an instance above or:
		speedTag.retag("[default]NH1/NH1 Material Length")
	or
		speedTag.path = "[default]NH1/NH1 Material Width"
		
	check the tag path/name:
		print(speedTag.path)
		print(speedTag.name)
	"""

	def __init__(self, path, conversion=None):
		self._tag_path = path
		self.name = self._tag_path
		self.conversion = conversion

	def read(self):
		""" Get the tag's value. 
		
		the same as:
			system.tag.readBlocking([self._tag_path])[0].value
		"""

		tag_value = system.tag.readBlocking([self._tag_path])[0].value

		if self.conversion == 'json':
			import json

			return json.loads(tag_value)
		elif self.conversion == 'pydl':
			return pydl(tag_value)
		elif self.conversion is None:
			return tag_value
		else:
			raise ValueError('{} is not a supported conversion!'.format(self.conversion))

	def value(self):
		"""Get the value of the tag.
		
		Calls .read()
		"""

		return self.read()

	def write(self, value):
		""" Write a new value to the tag."""

		import system

		if self.conversion == 'json':
			import json

			value = json.dumps(value)
		elif self.conversion == 'pydl':
			value = value.igds()
		elif self.conversion is None:
			value = value
		else:
			raise ValueError('{} is not a supported conversion!'.format(self.conversion))

		return system.tag.writeBlocking([self._tag_path], [value])

	def retag(self, newTag):
		""" changes the psuedo tags internal identity values """

		self._tag_path = newTag
		self.name = newTag

	def timestamp(self):
		""" returns the last time the tag was changed """

		return system.tag.readBlocking([self._tag_path])[0].timestamp

	def history(self, *args, **kwargs):
		"""Returns a queryTagHistory dataset for the tag.
		
		Accepts arguments and keyword arguments as system.tag.queryTagHistory
		"""

		data = system.tag.queryTagHistory([self._tag_path], *args, **kwargs)
		return data

	def tagpath(self):
		return self._tag_path

	@property
	def val(self):
		"""Property method to get or set the tag value.
		
		using
			ptag.val
		Calls self.read()
		
		using
			ptag.val = 3
		Calls self.write(3)
		"""

		return self.read()

	@val.setter
	def val(self, new_value):
		"""Property method to set the tag value.
		
		Calls self.write(new_value)
		"""

		self.write(new_value)

	@property
	def path(self):
		"""The tag path the Ptag is referencing."""
		return self.tagpath()

	@path.setter
	def _set_path(new_path):
		self.retag(new_path)

	@property
	def mean(self):
		"""Get the average value over the last 60 seconds."""

		return self.average()

	def average(self, start_time=None, end_time=None):
		"""Get the average tag value between two times.

		:param start_time: datetime
		:param end_time: datetime
		"""

		# if there is a start time but no end time, do until now
		if start_time is not None and end_time is None:
			seconds = system.date.secondsBetween(start_time, system.date.now())

		# if we have both, the time between
		elif not any(time_param is None for time_param in (start_time, end_time)):
			seconds = system.date.secondsBetween(start_time, end_time)
		else:
			seconds = 60

		print('seconds', seconds)

		return utils.average_tag_history(self.path, seconds, calculation="Average")

	@property
	def tstamp(self):
		"""Property method to get the current tag timestamp."""

		return self.timestamp()

	@property
	def ql(self):
		"""The current tag quality."""

		return system.tag.readBlocking([self._tag_path])[0].quality

	@property
	def qv(self):
		"""Get the Ignition qualified value for the current tag state."""

		return system.tag.readBlocking([self._tag_path])[0]

	@property
	def qvl(self):
		"""Get the qualified value as a tuple(value, quality, timestamp)."""

		tqv = system.tag.readBlocking([self._tag_path])[0]
		return tqv.value, tqv.quality, tqv.timestamp

	@property
	def pydl(self):
		"""Get a dataset tag value as a PyDataList."""

		return Shared.ds.PyDS.pydl(self.read())
