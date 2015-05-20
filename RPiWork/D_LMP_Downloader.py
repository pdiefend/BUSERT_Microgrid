import urllib.request
import csv
import os
import sys
#import time
from datetime import date, timedelta
import pickle

class LMP_Downloader:

    def __init__(self, Location):
        self.Location = Location        

    def tomorrowLMPfilename(self):
        year = str((date.today()+timedelta(0)).year)
        month = (date.today()+timedelta(0)).month
        day= (date.today()+timedelta(0)).day
        if month < 10:
               month = "0"+ str(month)
        else:
            month = str(month)
        if day <10:
            day = "0" + str(day)
        else:
            day = str(day)
    
        return year + month + day + '-da.csv'

    #Searches file for PPL's data and saves it to a file
    def parseFile(self, loc, lmpFile):
        #print ('Parsing file...')
        file1 = open(lmpFile, 'rt')
        lmp = []
        
        for row in csv.reader(file1):
            if str(row).find(loc) > 0 :
                count = 7
                while count < 77 :
                    #print(str(row[count]) + " ")
                    lmp.append(float(row[count]))
                    count = count + 3
                #file2.write('\n')
                break
        file1.close()
        #print ('Parsing complete.')
        
        # pickle.dump(lmp,open('tomorrow.p','wb'))
        # Reopen pickle
        #lmp = pickle.load(open('tomorrow.p', 'rb'))
        return lmp
    
    # dailyRun should be ran everyday after the Day-Ahead LMP has been posted, later than 17:00
    def DL_LMP(self):
        lmpFile = 'lmp.csv'
        # First download the daily DA-LMP file
        # print('http://www.pjm.com//pub/account/lmpda/'+tomorrowLMPfilename())
        urllib.request.urlretrieve('http://www.pjm.com//pub/account/lmpda/'+self.tomorrowLMPfilename(), lmpFile)
        # Then parse the data we are interested in and dump it to a pickle called 'today.p'
        return self.parseFile(self.Location, lmpFile)


#Save data to array
#Save array in pickle
#Open pickle in control system as needed

#def LMP_filename():
#    year = str(date.today().year)
#    month = date.today().month
#    day= date.today().day
#    if month < 10:
#        month = "0"+ str(month)
#    else:
#        month = str(month)
#    if day <10:
#        day = "0" + str(day)
#    else:
#        day = str(day)
#
#    return year + month + day + '-da.csv'

#def filename():
#    year = str(date.today().year)
#    month = date.today().month
#    day= date.today().day
#    if month < 10:
#        month = "0"+ str(month)
#    else:
#        month = str(month)
#    if day <10:
#        day = "0" + str(day)
#    else:
#        day = str(day)
#
#    return year + month + day + 'LMP.CSV'


