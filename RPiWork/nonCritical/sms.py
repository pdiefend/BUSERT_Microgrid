#Send text message
#Make sure you're using the right 'email address' for your carrier

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import poplib
from email import parser

#server = smtplib.SMTP( "smtp.gmail.com", 587 )
#server.starttls()
#server.login( 'busert123@gmail.com', 'treehugger' )

#server.sendmail('Griffin', '2064658911@mms.att.net', 'Testing 1 2 3')

# recp '<number@service>' ex: xxxxxxxxxx@vtext.com
# subj '<Subject>'
# body '<string>'
def sendMsg(recp, subj, body):
    msg = MIMEMultipart(body)
    msg['From'] = 'busert123@gmail.com'
    msg['To'] = recp
    msg['Subject'] = subj 
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP( 'smtp.gmail.com:587' )
    server.ehlo()
    server.starttls()
    server.login( 'busert123@gmail.com', 'treehugger' )
    server.sendmail('busert123@gmail.com', recp, msg.as_string())
    server.quit()

def checkMsgs():
    pop_conn = poplib.POP3_SSL('pop.gmail.com')
    pop_conn.user('busert123@gmail.com')
    pop_conn.pass_('treehugger')
    #Get messages from server:
    messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
    # Concat message pieces:
    messages = ["\n".join(mssg[1]) for mssg in messages]
    #Parse message intom an email object:
    messages = [parser.Parser().parsestr(mssg) for mssg in messages]
    for message in messages:
        print (message['subject'])
    pop_conn.quit()


sendMsg('5704010227@vtext.com', 'Automated Message', 'Are you still there?')
#checkMsgs()
