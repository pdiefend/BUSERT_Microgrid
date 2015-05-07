import threading
import tornado.ioloop
import tornado.web
import tornado.httputil
import tornado.httpserver
import time
import os.path
from datetime import date, timedelta
import pickle
import csv


class AcuRevServer():
	def __init__(self):
		self.t = threading.Thread(name='httpDaemon', target=self.http_server)
		self.t.start()
		self.data = {}
		self.request = {}
	def http_server(self):
		http_server = tornado.httpserver.HTTPServer(self.handle_request)
		http_server.listen(8080)
		tornado.ioloop.IOLoop.instance().start()	
	def handle_request(self, request):
		#print("Got one!")
		self.data = request.arguments
		self.request = request
		request.connection.write_headers(tornado.httputil.ResponseStartLine('HTTP/1.1', 200, 'OK'),tornado.httputil.HTTPHeaders({"Content-Length":str(0)}))
		request.connection.finish()
		#print(self.data)
		#pickle.dump(request, open( "data.p", "wb" )) # This is a bad way to pickle things...
		self.writeCSV()
	def stop_server(self):
		tornado.ioloop.IOLoop.instance().stop()
		tornado.ioloop.IOLoop.instance().close()
		self.t.join()
	
	def writeCSV(self):
		###Create file if nesscesary, and add headers
		state = os.path.isfile(self.filename())
		if state == False:
			f = open(self.filename(), 'wb')
			f.write(self.request.files[u'file'][0][u'body'])
			f.close()
		else:
			##If not just write stuff
			f = open(self.filename(), 'ab')
			substring = self.request.files[u'file'][0][u'body'].decode('utf-8')
			idx = substring.index('\r')
			f.write(bytes(substring[idx:], 'utf-8'))
			f.close()
		
		# ^Why are the above accesses in UTF-8, but the operational one is in bytes?
		# is it because the meter sends the data in bytes? I think so...

		# Store the most recent data in a pickle for the control system
		# open the file where the meter data is stored and create a CSV Dict Reader
		datFile = open(self.filename(), 'r')
		reader = csv.DictReader(datFile)
		
		# create a temporary empty Dict, this is where the data will go
		tmp = {}
		
		# iterate through the CSV to get the last row, aka the one we just wrote
		for row in reader:
			tmp = row
		
		# Dump the last row of the CSV as a Dict to a pickle that can be accessed by the
		# control system when it is needed. I should trigger the control system to run one minute
		# after the data is received or find a way that is not dependent on the meter's timing
		
		pickle.dump(tmp, open('/home/pi/BUSERT_Microgrid/RPiWork/pickles/meter.p', 'wb')) # this MUST be in bytes
		#print(tmp['Time'])
		
		# Clean up and move on
		datFile.close()
		return

	def yesterday_filename(self):
		year = str((date.today()-timedelta(1)).year)
		month = (date.today()-timedelta(1)).month
		day= (date.today()-timedelta(1)).day
		if month < 10:
			month = "0"+ str(month)
		else:
			month = str(month)
		if day <10:
			day = "0" + str(day)
		else:
			day = str(day)
	
		return month + day + year + ".CSV"
		
	def filename(self):
		year = str(date.today().year)
		month = date.today().month
		day= date.today().day
		if month < 10:
			month = "0"+ str(month)
		else:
			month = str(month)
		if day <10:
			day = "0" + str(day)
		else:
			day = str(day)
	
		return month + day + year + ".CSV"


# this goes in init
test = AcuRevServer()
