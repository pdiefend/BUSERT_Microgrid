#Send text message
#Make sure you're using the right 'email address' for your carrier

import smtplib

server = smtplib.SMTP( "smtp.gmail.com", 587 )
#server = smtp.lib.SMTP_SSL("smtp.gmail.com", 465)
server.ehlo()
server.starttls()
server.login( 'busert123@gmail.com', 'treehugger' )

server.sendmail('busert123@gmail.com', '5704010227@vtext.com', 'Testing 1 2 3')
server.quit()
