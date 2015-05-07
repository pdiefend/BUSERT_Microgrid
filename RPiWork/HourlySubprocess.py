# Hourly Decision Subprocess
# Run on the hour

import pickle
import datetime
from WU import WU
import Island
import datetime
from Ecobee_13 import EcobeeThermostat


print('==================================================')
print('Hourly Subprocess')
print(str(datetime.datetime.now()))

# ================================================================
# These pickles are created by the DailyLookahead (which relies on no pickles)
# Worst case the system will cease operations until midnight

# Unload LMP
try:
    lmp = pickle.load(open('pickles/LMP.p', 'rb'))
except FileNotFoundError:
    print('ERROR: LMP pickle not found')
    print('No further actions will be taken')
    quit()

# Unload operationModes
try:
    hourModes = pickle.load(open('pickles/hourModes.p','rb'))
except FileNotFoundError:
    print('ERROR: hourModes pickle not found')
    print('No further actions will be taken')
    quit()
# ================================================================

# ================================================================
# These pickles are created Manually. If these fail something's very wrong

# Unload Downstairs
try:
    downstairs = pickle.load(open('pickles/downstairs.p', 'rb'))
except FileNotFoundError:
    print('ERROR: Downstairs pickle not found')
    print('No further actions will be taken')
    quit()

# Unload Upstairs
try:
    upstairs = pickle.load(open('pickles/upstairs.p','rb'))
except FileNotFoundError:
    print('ERROR: Upstairs pickle not found')
    print('No further actions will be taken')
    quit()
# ================================================================

# Unload current operation settings
try:
    current = pickle.load(open('pickles/current.p','rb'))
except FileNotFoundError:
    print('WARN: current settings pickle not found')
    print('Recovering lost data')
    # Restore settings from the Ecobee. Create a spot for outage, 
    # 5Min will set it properly in a few seconds
    current = {'conditions': 'ERROR', 'mode': 'ERROR', 'lmp': 'ERROR','DownNormHeat': 60, 'DownNormCool': 73, 'UpHeatCool': 60, 'UpNormCool': 73,'outage': False}

# Refresh values from the Thermostats in case user changed them
downstairs.refreshValues()
upstairs.refreshValue()

# If the last hour was running in normal mode, then update the hold temperatures
if(current['mode'] = 'Normal'):
    current['DownNormHeat'] = downstairs.heatHoldTemp
    current['DownNormCool'] = downstairs.coolHoldTemp
    current['UpHeatCool'] = upstairs.heatHoldTemp
    current['UpNormCool'] = upstairs.coolHoldTemp

hour = datetime.datetime.now().time().hour

currentLMP = lmp[hour]
currentMode = hourModes[hour]

weather = WU('Lewisburg')
weather.refresh()
conditions = weather.current_condition()

# ================================================================
# How should I accept the utility LM into the system?
utilityLM = False
if utilityLM:
    currentMode = 'LM'
# ================================================================

# If the last mode != current mode, change thermostat/ATS, else leave it be.

if(currentMode == 'Consumption'):
    # Consumption Mode Activate all consumption devices
    print('Consume')
    Island.GridTie()    

elif(currentMode == 'Pre-heat'):
    # Pre-heat the HVAC system
    print('Pre-heat')
    Island.GridTie()    

elif(currentMode == 'Pre-cool'):
    # Pre-cool the HVAC system
    print('Pre-cool')
    Island.GridTie()    

elif(currentMode == 'LM' or currentMode == 'Island'):
    # High PV forecast?
    if(conditions == 'Clear' or conditions == 'Partly Cloudy'):
        # Load Management Mode (a.k.a. grid-tied reduction)
        print('LM')
        currentMode = 'LM'
        Island.GridTie()
        # Reduce Managed Loads and set HVAC to conservation points

    else:
        # Island Mode (a.k.a. isolated reduction)
        print('Island')        
        currentMode = 'Island'
        # Run Island Subprocess
        Island.Island(False)
        # 5 min should handle LM if Islanded     

else: #(currentMode == 'Normal')
    # Normal Mode    
    print('Normal')    
    Island.GridTie()


# Update the current settings with our new operational points and store it
current['conditions'] = conditions
current['mode'] = currentMode
current['lmp'] = currentLMP
pickle.dump(current, open('pickles/current.p','wb'))


# Add preheat precool here, load pickle modify needed, and store back. Then look to get the HVAC setpt
#current = {'conditions': conditions, 'mode': currentMode, 'lmp': currentLMP, 'outage': False}
# ecobee options:
#    refresh: get data from server
#    change settings: send data to server
# That's it.


