#!/usr/local/bin/python

import pymongo
from pymongo import Connection
import os

connection = Connection('76.181.68.191', 27017)
db = connection.test
collection = db.test_collection



path = 'OUT/'
listing = os.listdir(path)
for file in listing:
	if not file == 'log.txt':
		try:

			f = open(path + file)
			count = 0
                
			for line in file:
				count = count+1
				if count > 3:
					try: 
						cells = line.split("\t")
						id = cells[0]
						db.test.insert({id : map(lambda x:float(x), cells[1:])})

					except:
						log = open('upload_line_log.txt', 'a')
						log.write("this did not work for line " + count + " in " + file + "\n")
						log.close()
			f.close()
			os.remove(path + file)
		except:
			log = open('upload_log.txt', 'a')
			log.write("could not open and read " + file + "\n")
			log.close()


