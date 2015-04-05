[![Build Status](https://travis-ci.org/samarjeet27/CSV-Mapper.svg?branch=master)](https://travis-ci.org/samarjeet27/CSV-Mapper)
[![PyPI Downloads](https://img.shields.io/pypi/dm/csvmapper.svg)](https://pypi.python.org/pypi/csvmapper)
CSV Mapper
===
Easily manipulate csv files with python. CSV Mapper is a python Module capable of parsing CSV files against a pre-defined mapper file, as well as converting between them.

Installation
---
CSV-Mapper can be installed using pip or easy_install

```sh

$ pip install csvmapper

```

Another way, which installs the latest updated version is 

```sh
$ git clone http://github.com/samarjeet27
$ cd CSV-Mapper
$ python setup.py install

```

Basic Usage
---

A quick snippet to parse files with mapper -

```python

import csvmapper

# can use csvmapper.JSONMapper, csvmapper.XMLMapper or custom mappers also
mapper = csvmapper.DictMapper([
	[ 
		{ 'name': 'firstName' } , 
		{ 'name' : 'lastName' }, 
		{ 'name': 'age', 'type':'int' }
	]
])

# data.csv
# ------
# John,Doe,39
# James,Bond,29
# Harry,Potter,28

parser = csvmapper.CSVParser('data.csv', mapper)
objects = parser.buildObject()
print '%s will be %d years old after 2 years' %(objects[0].firstName, (objects[0].age + 2))
```
if your file already as column headers and you don't worry about the type, you can use -

```python
csvmapper.CSVParser('data.csv', hasHeader=True)
```

Write CSV
---

```python
# create parser
parser = csvmapper.CSVParser()
dictionary = parser.buildDict() # manipulation works for dict only at the moment
# manipulate csv file
writer = csvmapper.CSVWriter(dictionary) # or CSVObject instance
writer.write('data.csv') # write(filename)
```

Convert CSV to JSON/XML

```python
import csvmapper
# using same vars as above
converter = csvmapper.JSONConverter(parser) # or XMLConverter
print converter.doConvert(pretty=True)
```

License
---
The MIT License
