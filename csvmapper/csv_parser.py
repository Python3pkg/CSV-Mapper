import csv
from . import mapper
from . import utils

class CSVParser(object):
	"""CSV Parser capable of parsing against a pre-defined mapper file"""
	def __init__(self, csvFile, fmapper=None, hasHeader=False):
		super(CSVParser, self).__init__()
		# the csv file
		self.csvFile = csvFile
		# the mapper object
		self.fmapper = fmapper
		# whether the csv file contains columns in the first row
		self.hasHeader = hasHeader

	# get records from mapper file
	def getRecords(self):
		if self.fmapper == None:
			if self.hasHeader == False:
				raise Exception('No mapper specified, set hasHeader=True if csv file contains headers')
			else:
				self.fmapper = mapper.FieldMapper(self.csvData[0]) # first row of csv
		return self.fmapper.getRecords()

	# parses a CSV file
	def parseCSV(self):
		with open(self.csvFile, 'rU') as csvfile:
			rdr = csv.reader(csvfile, delimiter='\t', quotechar='|')
			x = []
			for row in rdr:
				x.append(row[0].split(','))
			self.csvData = x

	# convert type
	def convertType(self,to,val):
		if to == '':
			return val
		i = ''
		exec('i = %s(%s)' %(to,val))
		return i

	# convert csv data to record
	def toDict(self, cdat, rec):
		d = {}
		i = 0
		for j in rec:
			a = cdat[i]
			if 'type' in j:
				a = self.convertType(j['type'], a)
			d[j['name']] = a
			i= i+1
		return d

	def getIndex(self, x, l):
		if x > (l-1):
			return x%l
		return x

	# csv against mapper as dict instance
	def buildDict(self, onAppend=None,popHeader=True):
		if hasattr(self, 'csvData') == False:
			self.parseCSV()

		recs = self.getRecords()
		if self.hasHeader and popHeader:
			self.csvData.pop(0) # remove the header line

		l = len(recs)
		dicts = []
		for x in range(0, len(self.csvData)):
			i = self.getIndex(x, l)
			dic = self.toDict(self.csvData[x], recs[i])
			if onAppend == None:
				dicts.append(dic)
			else:
				dicts.append(onAppend(dic))
		return dicts

	# as object instance
	def buildObject(self):
		return self.buildDict(utils.CSVObject)


# Parser instance to CSV
class CSVWriter():
	"""Generate CSV Output"""
	def __init__(self, dic):
		self.dic = dic

	# write to csv file
	def write(self, fileName):
		isDict = type(self.dic[0]) == dict
		with open(fileName, 'w') as fs:
			headings = None
			if isDict:
				headings = list(self.dic[0].keys())
			else:
				headings = self.dic[0].attribs()

			w = csv.DictWriter(fs, headings)
			w.writeheader()
			if isDict:
				for row in self.dic:
					w.writerow(row)
			else:
				for row in self.dic:
					w.writerow(row.__dict__)
