import time
import os.path
from datetime import date, timedelta
import pickle
import csv

f = open('test.CSV', 'r')
reader = csv.DictReader(f)
tmp = {}
for row in reader:
	tmp = row

pickle.dump(tmp, open('meter.p', 'wb'))

print(tmp['Time'])


f.close()

