import urllib.request
import os
import sys
import smtplib
import passwords

username = passwords.IMP_USER
password = passwords.IMP_PASS
ATS_base = passwords.IMP_ATS_BASE
Raux_base = passwords.IMP_RAUX_BASE
Gmail_User = passwords.GMAIL_USER
Gmail_Pass = passwords.GMAIL_PASS
recpients = passwords.GMAIL_RECP

# pull pin 9 high to remote island, pull pin 9 low to return to auto
island_url =  'http://agent.electricimp.com/'+ATS_base+'?username='+username+'&password='+password+'&led=1'
gridTie_url = 'http://agent.electricimp.com/'+ATS_base+'?username='+username+'&password='+password+'&led=0'
status_url =  'http://agent.electricimp.com/'+ATS_base+'?username='+username+'&password='+password+'&status'

# pull pin 9 high to disable breaker, low to turn back on
raux_off_url = 'http://agent.electricimp.com/'+Raux_base+'?username='+username+'&password='+password+'&led=1'
raux_on_url =  'http://agent.electricimp.com/'+Raux_base+'?username='+username+'&password='+password+'&led=0'

# Island from the power grid
def Island(outage):
    # Disable Raux2    
    #urllib.request.urlretrieve(raux_off_url, 'impStat.txt') # <==================================

    #server = smtplib.SMTP( "smtp.gmail.com", 587 )
    #server.ehlo()
    #server.starttls()
    #server.login( Gmail_User, Gmail_Pass )

    if outage:
        # Notify User that outage occured, ATS Islanded automatically
        print("notifying user that a utility outage occured")
        #server.sendmail(Gmail_User, recpients, 'A Utility Outage Occured')
        #server.quit()
    else:
        # Notify User that we will island Manually
        print("notifying user that the system will Island itself")
        #server.sendmail(Gmail_User, recpients, 'Microgrid will now Island itself')
        #server.quit()
        # Island the Microgrid
        #urllib.request.urlretrieve(island_url, 'impStat.txt') # <==================================

# Reconnect to the Power grid and re-enable Raux2
# If we are islanded due to an outage condition, we will remain on the
# generator. This essentially returns the ATS to "auto"
def GridTie():
    print('ATS set to AUTO')
    urllib.request.urlretrieve(gridTie_url, 'impStat.txt')
    #urllib.request.urlretrieve(raux_on_url, 'impStat.txt') # <==================================

# Check status of the ATS, does not change island status
def IsIslanded():
    print('Checking ATS status')
    urllib.request.urlretrieve(status_url, 'impStat.txt')
    f = open('impStat.txt', 'r')
    stat = f.read()
    if 'OK Status: Islanded=true' in stat:
        print('Islanded')
        return True
    elif 'OK Status: Islanded=false' in stat:    
        print('Grid-Tied')
        return False
    else:
        print('An Error Occured')
        return 'ERROR'
 
