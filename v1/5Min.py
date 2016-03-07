# 5 Minute Subprocess
# Run every 5 minutes 1 minute behind (i.e. 2:01, 2:06, 5:31, 10:56)

import Island
import pickle
import datetime
import uGrid_Params

print('==================================================')
print('5Min Subprocess')
print(str(datetime.datetime.now()))

def performLM():
    print('Managing Loads')
    
    # Unload Meter Data
    try:
        meter = pickle.load(open('pickles/meter.p', 'rb'))
    except FileNotFoundError:
        print('ERROR: Meter pickle not found')
        print('No further actions will be taken')
        quit()

    # Unload Last Meter Data
    try:
        meterLast = pickle.load(open('pickles/meterLast.p', 'rb'))
    except FileNotFoundError:
        print('ERROR: Meter Last pickle not found')
        print('No further actions will be taken')
        quit()
    
    # Check current power consumption
    Gen_output = meter['P01_kW'] + meter['P02_kW'] + meter['P04_kW'] + meter['P05_kW']
    PV_output = meter['P03_kW'] + meter['P06_kW']
    PV_outputLast = meterLast'P03_kW'] + meterLast['P06_kW']

    if (PV_output < 0):
        # PV is on 
        if (Gen_output < 1.5):
            # increase load otherwise leave it be for now.
    elif (PV_outputLast < 0):
        # PV was on and we probably just killed it, so turn on some WeMos, Heaters?
    else:
        # PV is off, turn off all WeMos
        

# To make my life easier I'm just going to tell the system what the WeMos are called
# and thier nominal load in uGrid params as dict objects


# Load current status of system
try:
    current = pickle.load(open('pickles/current.p','rb'))
except FileNotFoundError:
    print('ERROR: Current Settings pickle not found')
    print('No further actions will be taken')
    quit()

# check to see if we are islanded on the ATS
islanded = Island.IsIslanded()

# Check to see if islanded and we know it
if (islanded and ((current['mode'] == 'Island') or current['outage'])):
    # then perfrom LM tasks
    print('Islanded Operation')
    performLM()

# if islanded but we didn't know
elif islanded:
    print('Utility Outage Island')
    # Update our current status
    current['outage'] = True
    Island.Island(True)
    # perform LM tasks
    performLM()

elif current['leveling']:
    print('Leveling Load')
    # Unload Meter Data
    try:
        meter = pickle.load(open('pickles/meter.p', 'rb'))
    except FileNotFoundError:
        print('ERROR: Meter pickle not found')
        print('No further actions will be taken')
        quit()
    # Unload Last Meter Data
    try:
        meterLast = pickle.load(open('pickles/meterLast.p', 'rb'))
    except FileNotFoundError:
        print('ERROR: Meter Last pickle not found')
        print('No further actions will be taken')
        quit()

    Grid = meter['P01_kW'] + meter['P02_kW'] + meter['P04_kW'] + meter['P05_kW']
    GridLast = meterLast['P01_kW'] + meterLast['P02_kW'] + meterLast['P04_kW'] + meterLast['P05_kW']
    PV_output = meter['P03_kW'] + meter['P06_kW']
    PV_outputLast = meterLast'P03_kW'] + meterLast['P06_kW']

    # check status of WeMos, we know what they are, see above
    Heat1['on'] = False # Something gained from server...
    Heat2['on'] = False # Something gained from server...
    Volt['on'] = False # Something gained from server...

    # compare last consumption to current consumption and make decisions
    PVdiff = PV_output - PV_outputLast
    if (PVdiff > 0.5): # check if it's worth leveling
        # More PV now than earlier so increase load
        if (PVdiff > 3.5):
            # Turn everthing on
        elif (PVdiff > 2.2):
            # Turn on Heat 1 and 2 if not already on
        elif (PVdiff > 1.5):
            # Turn on Heat 1 Volt if not already on
        elif (PVdiff > 1):
            # Turn on Heat 1 if not already on
        else:
            # Turn on Volt if not already on
    
    elif (PVdiff < -0.5): 
        # Less PV now than earlier so drop load
        if (PVdiff < -3.5):
            # Turn everthing off
        elif (PVdiff < -2.2):
            # Turn off Heat 1 and 2 if not already off
        elif (PVdiff < -1.5):
            # Turn off Heat 1 Volt if not already off
        elif (PVdiff < -1):
            # Turn off Heat 1 if not already off
        else:
            # Turn off Volt if not already off

# Wrap above into a new function that can be tested offline.


# otherwise we are not islanded nor are we attempting to level the load
else:
    print('Normal Operation')
    # Update our current status
    current['outage'] = False
    # we are done, no short-term LM necessary

pickle.dump(meter, open('pickles/meterLast.p', 'wb'))    
pickle.dump(current, open('pickles/current.p', 'wb'))



