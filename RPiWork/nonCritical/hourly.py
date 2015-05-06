#Send text message
#Make sure you're using the right 'email address' for your carrier

import smtplib
import pickle
from datetime import datetime

server = smtplib.SMTP( "smtp.gmail.com", 587 )
#server = smtp.lib.SMTP_SSL("smtp.gmail.com", 465)
server.ehlo()
server.starttls()
server.login( 'busert123@gmail.com', 'treehugger' )

lmp = pickle.load(open('today.p', 'rb'))
# LMP is in HE, so when we call datetime, we must increment, but then the array is
# zero-offset so we must decrement. Thus no offset is required (+1 + -1 = 0)
hour = datetime.now().hour

msg = 'The current LMP is now ' + str(lmp[hour])

server.sendmail('busert123@gmail.com', 'busert123@gmail.com', msg)
server.quit()
