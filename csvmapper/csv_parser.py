import csv
import mapper
import utils

class CSVParser(object):
	"""CSV Parser capable of parsing against a pre-defined mapper file"""
	def __init__(self, csvFile, fmapper):
		super(CSVParser, self).__init__()
		self.csvFile = csvFile
		self.fmapper = fmapper
		
	def getRecords(self):
		return self.fmapper.getRecords()

	# parses a CSV file
	def parseCSV(self):
		with open(self.csvFile, 'rb') as csvfile:
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

	# as dict instance
	def buildDict(self, onAppend=None):
		if hasattr(self, 'csvData') == False:
			self.parseCSV()
		recs = self.getRecords()
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
