
from mongoengine import *
import os

DBNAME = 'test'
HOST = '76.181.68.191'
PORT = 27017
connect(DBNAME, host = HOST, port = PORT)


class Line(Document):
        varid = StringField()
        cell = ListField(FloatField())

def upLoadStudy(gsid):
	
	
	path = 'OUT/'
	listing = os.listdir(path)
	for FILENAME in listing:
		if not FILENAME == 'log.txt':
			try:
				file = open(path + FILENAME)
				count = 0
	      			for line in file:
					count += 1
					if count > 3:
						try:
							
							stuff = line.split("\t")
							
							post = Line(varname = stuff[0], cell = map(lambda x:float(x), stuff[1:]))
							post.save()
						except:
							log = open('upload_log.txt',"a")
							log.write("this did not work for line " +count + " in " + FILENAME)
							log.close()
				file.close()
				os.remove(path + FILENAME)
			except:
                                log = open('upload.txt',"w")

                                log.write("this did not work")
                                log.close
