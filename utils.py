"""Convenience functions and classes.

(This is one of the oldest bits of code here, so some of it shows its age in style, standards, and documentation.)

Contains mostly convenience functions.
-----------------------------------------
ptag							psuedo tag object class
gw(event)						Returns the parent window of an event.
typ(object)						Returns the name of the object type as a string.
rtag(tag)						Wrapper to read tags without having to wrap them in lists etc.
gct(tagConfiName, coaterNum)	Fetches a string representing a tag from the config file. See the ConfigModule for
more details.
get_recipes()					reads recipes csv and returns the info as a dataset with headers
get_csv_dataset(path)			reads the csv at the path and returns the info as a dataset with headers
gt(theKey) 						accepts a string key and returns the corresponding tag for that users screen

"""


def average_tag_history(tag_path, seconds=60, calculation="Average"):
	"""Updates the tag for the number of minutes of uptime this shift.
			
		:param tag_path: str, the path of the tag.
		:param seconds: int, the number of seconds back from current time to query.
		:param calculation: str, to specify a calculation mode other than time weighted average.
			
		:returns: float, the average value for the tag over the interval.
	"""

	import traceback
	from java.lang import Exception

	try:

		# if given a string, put it in a list
		if isinstance(tag_path, str):
			tag_path = [tag_path]

		# if it wasn't a string or list, can't use it
		elif not isinstance(tag_path, list):
			raise (TypeError("Tag must be a string or string in a list."))

		# set the start and end times
		endTime = system.date.now()
		startTime = system.date.addSeconds(endTime, -1 * seconds)

		calcs = [calculation]

		# returns a one row, two column dataset
		avg_ds = system.tag.queryTagCalculations(tag_path, calcs, startTime, endTime)

		return avg_ds.getValueAt(0, 1)

	except Exception:
		# we need to know about errors, not the operators
		lg = system.util.getLogger("average_tag_history shared script")
		lg.warn(traceback.format_exc())


def calc_tag_history(tag_path, calc='Average', interval_num=60, interval='s', end_time='now'):
	"""Get tag history calculation for a tag.
	
	if a string, end_time must be in 'yyyy-mm-dd HH:mm:ss' format
	"""

	startm = system.date.now()

	import traceback
	from java.lang import Exception

	try:  # I'm not the biggest fan of error handling like this,
		# but I need to know about errors, not the operators

		# if given a string, put it in a list
		if isinstance(tag_path, str):
			tag_path = [tag_path]
		# if it wasn't a string or list, can't use it
		elif not isinstance(tag_path, list):
			raise (TypeError("Tag must be a string or string in a list."))

		# set the start and end times
		if end_time == 'now':
			endTime = system.date.now()
		elif isinstance(end_time, str):
			endTime = system.date.parse(end_time)
		else:
			endTime = end_time

		if interval.lower() == 's':
			startTime = system.date.addSeconds(endTime, -1 * interval_num)
		elif interval.lower() == 'm':
			startTime = system.date.addMinutes(endTime, -1 * interval_num)
		elif interval.lower() == 'h':
			startTime = system.date.addHours(endTime, -1 * interval_num)
		elif interval.lower() == 'd':
			startTime = system.date.addDays(endTime, -1 * interval_num)

		calcs = [calc]

		# returns a one row, two column dataset
		avg_ds = system.tag.queryTagCalculations(tag_path, calcs, startTime, endTime)

		# to pydataset
		pds = system.dataset.toPyDataSet(avg_ds)

		# return just the value
		return pds[0][1]

	except Exception:
		lg = system.util.getLogger("average_tag_history shared script")
		lg.warn(traceback.format_exc())
		print("average_tag_history shared script", traceback.format_exc())


def colorFade(color, fade=100):
	"""Fades a color to transparency.

	Takes a java color object and a 0 to 100 fade 'percentage' (int) and applies the percentage to the alpha channel 
	then returns the new color.

	:param color: java.awt.Color
	:param fade: int, between 0 and 100 how opaque, compared to current, to make the color.

	:returns: java.awt.Color
	"""

	from traceback import format_exc as exc

	try:
		r, g, b, a = parseJavaColor(color)
		a = int(255 * fade / 100.0)
		newColor = "Color({r},{g},{b},{a})".format(r=r, g=g, b=b, a=a)
		return newColor
	except Exception:
		print(exc())
		return (color)


def dsget(dset, lookup, lookup_col_hdr, val_col_header):
	"""Get the value at the intersection of a found value's row and column by headers.

			:dset ignition dataset: the dataset to search
			:lookup any: generally a string or numeric, the value to find in the lookup column
			:lookup_col_hdr str: the header of the column to search for the value
			:val_col_header str: the header of the column to retriever the value from
			
			:returns any: the value found
			"""
	hdrs = system.dataset.getColumnHeaders(dset)
	val_index = hdrs.index(val_col_header)
	lookup_hdr = hdrs.index(lookup_col_hdr)
	row_pyds = Shared.L.getDSrow_asDS(dset, tcode, column_to_search=lookup_hdr)[0]
	return row_pyds[val_index]


def find_newest_file(files_path):
	"""Get the filepath of the mostrecently modified/created file, of files in a directory.
		Also returns a list of the older files.

		example:
		new, old_list = find_newest_file('C:\directory')
		print(new)
		print(old_list)
		>C:\today.txt
		>['C:\yesterday.txt', 'C:\last_week.txt']
	"""

	import scandir
	print('checking files')
	# dummy data to start
	latest_file = ['', system.date.parse("1970-01-01 00:00:00")]

	# find the newest file, delete the others
	delete_list = []

	# for each file in the directory
	for inv_file in scandir.scandir(files_path):
		# when was this file modified
		file_tstamp = get_mod_time(inv_file)

		# if it's the newest found, save it
		if latest_file[1] < file_tstamp:
			print('newer file', inv_file.path)
			delete_list.append(latest_file[0])
			latest_file = [inv_file.path, file_tstamp]
		else:
			delete_list.append(inv_file.path)
	return latest_file, delete_list


def get_ds_row(dataset, lookup, column_to_search=0, report_row_index=False, test_fn=None):
	"""Find the first row in a Py/Dataset/2d nested list where the column value is equal to the lookup value.

	 default lookup column is 0
	 if not found returns False.
	
	:param dataset: BasicDataset, PyDataSet, nested lists: the data to check
	:param lookup: any, the value to test in the column
	:param column_to_search: str or int, if a string is provided, it will be used to match a header and that column 
	will
		be searched, only Ignition dataset types. If an integer, that column index will be searched.
	:param report_row_index: bool, whether to return a tuple of ([[the],[row],[data]], the_row_index), default false
	:param test_fn: callable, a function that takes two values and returns a boolean, default lambda x,y: x == y

	:returns: DataSet
	"""

	from com.inductiveautomation.ignition.common.script.builtin.DatasetUtilities import PyDataSet
	from com.inductiveautomation.ignition.common import BasicDataset
	import system

	if isinstance(dataset, BasicDataset):
		ds_length = dataset.rowCount
		ds_headers = dataset.columnNames
		dataset = system.dataset.toPyDataSet(dataset)
	elif isinstance(dataset, PyDataSet):
		ds_length = dataset.rowCount
		ds_headers = dataset.columnNames
	elif isinstance(dataset, list):
		ds_length = len(dataset)

	# if given a header instead of a column index, find the index of that column header
	if isinstance(column_to_search, str):
		column_to_search = ds_headers.index(column_to_search)

	# default test function
	if test_fn is None:
		test_fn = lambda x, y: x == y

	# search for the lookup, return the first row that matches
	for row in range(0, ds_length, 1):
		if test_fn(dataset[row][column_to_search], lookup):
			return_row = [cl for cl in dataset[row]]
			if report_row_index:
				ret_value = return_row, row
			else:
				ret_value = return_row
			return ret_value
	return False


def getDSrow_number(dataset, lookup, column_to_search=0):
	"""Find the first row in a Py/Dataset/2d nested list where the column value is equal to the lookup value.

	 The default lookup column is 0
	 if not found returns -1

	:param dataset: BasicDataset, PyDataSet, nested lists: the data to check
	:param lookup: any, the value to test in the column
	:param column_to_search: str or int, if a string is provided, it will be used to match a header and that column 
	will
		be searched, only Ignition dataset types. If an integer, that column index will be searched.

	:returns: int, the row index or -1 if not found.

	 """

	from com.inductiveautomation.ignition.common.script.builtin.DatasetUtilities import PyDataSet
	from com.inductiveautomation.ignition.common import BasicDataset
	import system

	if isinstance(dataset, BasicDataset):
		ds_length = dataset.rowCount
		ds_headers = dataset.columnNames
		dataset = system.dataset.toPyDataSet(dataset)
	elif isinstance(dataset, PyDataSet):
		ds_length = dataset.rowCount
		ds_headers = dataset.columnNames
		ds_headers = dataset.columnNames
	elif isinstance(dataset, list):
		ds_length = len(dataset)

	# if given a header instead of a column index, find the index of that column header
	if isinstance(column_to_search, str):
		column_to_search = ds_headers.index(column_to_search)

	# search for the lookup, return the first row that matches
	for row in range(0, ds_length, 1):
		if dataset[row][column_to_search] == lookup:
			return row
	return -1


def getDSrow_asDS(dataset, lookup, column_to_search=0):
	"""Find the row where the leftmost column value is equal to the lookup value, if not found False."""

	import system
	dataset = system.dataset.toPyDataSet(dataset)
	for row_num in range(0, len(dataset), 1):
		row = dataset[row_num]
		#			print(type(row))
		if row[column_to_search] == lookup:
			headers = system.dataset.getColumnHeaders(dataset)
			py_list_row = [[x for x in row]]
			return_set = system.dataset.toPyDataSet(system.dataset.toDataSet(headers, py_list_row))
			return return_set
	return False


def getScope():
	"""Get the scope that the code is running under.

	:returns: int, scope: 0=Gateway, 1=Client, 2=Designer
		
	"""
	try:
		if system.util.getSystemFlags() & system.util.CLIENT_FLAG:
			location = 1
		elif system.util.getSystemFlags() & system.util.DESIGNER_FLAG:
			location = 2
	except AttributeError:
		# system.util.getSystemFlags() does not exist in gateway scope
		location = 0
	return location


def getScreenDims():
	"""Return the dimensions of the client screen.

	:returns: tuple, (int, int) dimensions of the screen.
	"""

	from java.awt import Toolkit

	scrn = Toolkit.getDefaultToolkit().getScreenSize()

	ht = scrn.getHeight()
	wt = scrn.getWidth()

	return ht, wt


def gt(theKey):
	"""Get the corresponding tag for a string key for that user's screen.

	example:
	myFinishingOperatorTag = Shared.L.gt('OperatorFinishing')
	print(myFinishingOperatorTag)
	print(myFinishingOperatorTag.value)
	>>>
	[Miller, Tim, Good, Fri Nov 22 11:26:57 EST 2019 (1574440017200)]
	Miller, Tim

	the [client]ClientGlobals/Tag_Key_Value_Dataset is populated from a csv file on the
	OEE server C:\NITTO\PIC\IndirectTagDataSet.csv	during client window startup script
	"""

	import system

	thedataset = system.dataset.toPyDataSet(system.tag.read("[client]ClientGlobals/Tag_Key_Value_Dataset").value)
	coaterID = system.tag.read('[client]ClientGlobals/CoaterIdentifier').value

	for i in range(0, thedataset.getRowCount()):
		thisKey = thedataset[i][0].encode('ascii', 'ignore')
		thisValue = thedataset[i][1]

		if thisKey == theKey:
			valueString = thisValue.encode('ascii', 'ignore').format(coaterNumber=coaterNumber)
			returnValue = system.tag.read(valueString)
			return returnValue


def gw(event):
	"""Returns the parent window of an event."""
	import system
	return system.gui.getParentWindow(event)


def gwbn(window_name):
	"""Returns the first open window with the string in its name. If none found returns False. Not case sensitive."""

	winNames = system.gui.getOpenedWindowNames()
	window = False
	for win in winNames:
		if window_name.lower() in win.lower():
			window = system.gui.getWindow(win)
	return window


def gwr(event):
	"""Returns the root container of the parent window of an event."""

	import system
	return system.gui.getParentWindow(event).getRootContainer()


def get_num_from_path(path):
	"""Return the first integer in the tag path (or any string). Useful for getting coater/lam number."""

	import re

	# gets the number from the tag (strips non-numeric using regex substitution and grabs the first number left over)
	return int(re.sub('[^0-9]', '', path)[0])


def gtts(tagpath):
	"""Get the timestamp of a tag at the path."""

	return rtag(tagpath).timestamp


def get_recipes():
	"""Reads recipes csv and returns the info as a dataset with headers."""

	import csv

	path = r"C:\...\recipes.csv"

	csvData = csv.reader(open(path))

	header = csvData.next()

	# Create a dataset with the header and the rest of our CSV.
	return system.dataset.toDataSet(header, list(csvData))


def get_csv_dataset(path):
	"""Reads the csv at the path and returns the info as a dataset with headers."""

	import csv

	csvData = csv.reader(open(path))
	header = csvData.next()

	# Create a dataset with the header and the rest of our CSV.
	return system.dataset.toDataSet(header, list(csvData))


def glog(name="Logger"):
	""" Returns a system logger with the name provided. """

	import system

	return system.util.getLogger(name)


def imageAutoscale(imageObject):
	"""
	This had been used for the image frame for the put ups before switching to the image canvas. It was adapted from 
	code from the link below.
	Originally (as link) it was to maintain image ratio, here it was attempting to resize the image to fit within the 
	frame. 
	
	from https://forum.inductiveautomation.com/t/autoscale-image-to-fill-bounds-but-maintain-aspect-ratio/19302/3
	"""

	from com.inductiveautomation.ignition.client.images import ImageLoader

	# Find Aspect Ratio of Component
	imgComponent = imageObject
	imgComponentW = imgComponent.getWidth()
	imgComponentH = imgComponent.getHeight()
	imgComponentRatio = float(imgComponentW) / float(imgComponentH)

	# Find Aspect Ratio of Original Image
	filename = imgComponent.getPath()
	img = ImageLoader.getInstance().loadImage(filename)
	imgW = img.getWidth()
	imgH = img.getHeight()
	imgRatio = float(imgW) / float(imgH)

	fillH = imgComponentH
	fillW = imgComponentW

	# Set Strech Mode to "Parameters"
	imgComponent.setStretchMode(1)

	# Set Component Image Bounds
	imgComponent.setStretchHeight(fillH)
	imgComponent.setStretchWidth(fillW)


def match_tabcode(does_this_tcode, match_this):
	"""Test if two tabcodes match, disregarding the presence of T's in either."""

	does_this_tcode, match_this = str(does_this_tcode), str(match_this)
	return does_this_tcode.upper().replace('T', '') in match_this


def minutesTimeToday(datetime):
	"""This function takes a datetime value and returns the minutes since midnight today."""

	import system.date
	now = system.date.now()
	month = system.date.getMonth(now)  # index 0: janurary is 0
	day = system.date.getDayOfMonth(now)
	year = system.date.getYear(now)
	today = system.date.getDate(year, month, day)
	return system.date.minutesBetween(today, datetime)


def osk():
	"""Opens the on screen keyboard."""

	keyb = ["C:\Windows\system32\osk.exe"]
	# keyb = ["C:\FreeVK.exe"]
	system.util.execute(keyb)


def parseJavaColor(colorObj):
	""" Accepts a java.awt.Color[] object and returns r,g,b,a scaled to 0 to 255.
	
	rbg are red green and blue values.
	a is the 'alpha channel' which is how opaque/transparent the color is.
	For a 255 is fully opaque and 0 is fully transparent (invisible).
	"""

	comps = colorObj.getComponents(None)
	r = int(comps[0] * 255)
	g = int(comps[1] * 255)
	b = int(comps[2] * 255)
	a = int(comps[3] * 255)
	return r, g, b, a


def resetButtons(container):
	"""Resets the template buttons in the container. Used for the stop reason popup on NH windows."""

	from Shared.CrawlDownFn import iterThru
	iterThru(container, "Enabled", True)


def sorc(event):
	"""Return the source component object from the event.
	 
	event.source will allow you to read values etc from a component, but not 
	change the values etc. An actual component object is needed for that. This
	function returns the the component object for the event.
	
	example of use:
	from Shared.L import src
	src_obj = src(event)
	src_obj.text = 'This is nice to have.'
	print(src_obj.text)
	>This is nice to have.
	"""

	return event.source.parent.getComponent(event.source.name)


def send_email(recipientList=[], subject='', body='', cc=[], bcc=[]):
	"""Sends an email using I.T.'s smtp relay.
	
	Example:
		send_email(["name@address.com"], "Did you get this email?", "Hello, let me know if you don't get this email.")
	
	
	for editing, example
		send_to = ['brian.lifeof@mail.com', 'blue.fjords@spam.com']
		subj = 'this is an email subject'
		body = 'this is the body of the email, it has some words'
		send_email(send_to, subj, body)
		
		This is only able to handle simple text emails. Attachments are not implemented.
		"""

	import smtplib
	from email.mime.text import MIMEText
	from traceback import format_exc

	sender = 'noreply@company.com'

	msg = MIMEText(body)
	msg['Subject'] = subject
	msg['From'] = sender

	to_lists = (('To', recipientList), ('Cc', cc), ('Bcc', bcc))
	for to_type, to_lst in to_lists:
		try:
			msg[to_type] = ", ".join(to_lst) if len(to_lst) > 1 else to_lst[0]
		except IndexError:
			pass  # regularly won't have all of the lists

	try:
		smtpObj = smtplib.SMTP('000.00.0.00')  # ip of smtp relay server
		smtpObj.sendmail(sender, recipientList + cc + bcc, msg=msg.as_string())
	except smtplib.SMTPException:
		logr = system.util.getLogger('Send email in {module}'.format(module=__name__))
		logr.error(format_exc())


def table_this(data_object, headers=None):
	"""Get an eztable.Table of an iterable like a dataset.
	
	data_object: a list of lists, Ignition DataSet or pyDataSet
	headers: iterable of strings to use as the headers for the table, can be ('header string', type) tuples
		for a typed table
	
	returns: eztable.Table
	"""

	from eztable import Table
	from com.inductiveautomation.ignition.common import BasicDataset
	from com.inductiveautomation.ignition.common.script.builtin.DatasetUtilities import PyDataSet
	from Shared.ds.PyDataList import PyDataList

	if isinstance(data_object, BasicDataset):
		data_object = system.dataset.toPyDataSet(data_object)
		headers = data_object.columnNames if headers is None else headers
	elif isinstance(data_object, PyDataSet):
		headers = data_object.columnNames if headers is None else headers
	elif isinstance(data_object, PyDataList):
		headers = data_object.headers if headers is None else headers
	else:
		headers = ['header{}'.format(num) for num in range(len(data_object[0]))] if headers is None else headers

	return Table(headers, data_object)


def who_called():
	"""Get the name of the function and module of that function, which called this function."""
	import inspect

	curframe = inspect.currentframe()
	ret_list = [x for x in inspect.getouterframes(curframe)][1:]
	return ret_list
