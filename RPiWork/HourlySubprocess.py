# Hourly Decision Subprocess
# Run on the hour

import pickle
import datetime
from WU import WU
import Island
import datetime
from Ecobee_13 import EcobeeThermostat
import uGrid_Params


preCoolDelta = uGrid_Params.PRE_COOL_DELTA # amount setpoint is varied during precooling
preHeatDelta = uGrid_Params.PRE_COOL_DELTA # amount setpoint is varied during preheating

LMCoolDelta = uGrid_Params.LM_COOL_DELTA # amount setpoint is varied during Load Management Mode
LMHeatDelta = uGrid_Params.LM_HEAT_DELTA # amount setpoint is varied during Load Management Mode

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
    current = {'conditions': 'ERROR', 'mode': 'ERROR', 'lmp': 'ERROR','DownNormHeat': 60, 'DownNormCool': 73, 'UpNormHeat': 60, 'UpNormCool': 73,'outage': False}

# Refresh values from the Thermostats in case user changed them
downstairs.refreshValues()
upstairs.refreshValues()

# If the last hour was running in normal mode, then update the hold temperatures
if(current['mode'] == 'Normal'):
    current['DownNormHeat'] = downstairs.heatHoldTemp
    current['DownNormCool'] = downstairs.coolHoldTemp
    current['UpNormHeat'] = upstairs.heatHoldTemp
    current['UpNormCool'] = upstairs.coolHoldTemp
upFan = upstairs.fan
downFan = downstairs.fan
upMode = upstairs.hvacMode
downMode = downstairs.hvacMode


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

# Daily Lookahead Override (Takes Utility LM into account as well)
if(currentMode == 'LM' or currentMode == 'Island'):
    # High PV forecast?
    if(conditions == 'Clear' or conditions == 'Partly Cloudy'):
        currentMode = 'LM'
    else:
        # Check to see if we are over the Generator LMP
        if currentLMP > uGrid_Params.GEN_LMP_THRESHOLD:
            # If so, Island the microgird            
            currentMode = 'Island'
        else:
            # If current LMP < Generator LMP, then it is not worth running.
            currentMode = 'LM'
        
print(currentMode)

# If the last mode != current mode, change thermostat/ATS, else leave it be.
if (currentMode != current['mode']):
    print('Modes Changed since last hour')
    if(currentMode == 'Consumption'):
        # Consumption Mode Activate all consumption devices
        Island.GridTie()
        upstairs.changeSettings(current['UpNormHeat'] + preHeatDelta, current['UpNormCool'] -preCoolDelta, 'on', upMode)
        # delay?
        downstairs.changeSettings(current['DownNormHeat'] + preHeatDelta, current['DownNormCool'] -preCoolDelta, 'on', downMode)
    
    elif(currentMode == 'Pre-heat'):
        # Pre-heat the HVAC system
        Island.GridTie()
        upstairs.changeSettings(current['UpNormHeat'] + preHeatDelta, current['UpNormCool'], 'auto', upMode)
        # delay?
        downstairs.changeSettings(current['DownNormHeat']+ preHeatDelta, current['DownNormCool'], 'auto', downMode)    
    
    elif(currentMode == 'Pre-cool'):
        # Pre-cool the HVAC system
        Island.GridTie()
        upstairs.changeSettings(current['UpNormHeat'], current['UpNormCool'] - preCoolDelta, 'auto', upMode)
        # delay?
        downstairs.changeSettings(current['DownNormHeat'], current['DownNormCool'] - preCoolDelta, 'auto', downMode)    
    
    elif(currentMode == 'LM'):
        Island.GridTie()
        # Reduce Managed Loads and set HVAC to conservation points
        upstairs.changeSettings(current['UpNormHeat'] - LMHeatDelta, current['UpNormCool'] + LMCoolDelta, 'on', upMode)
        # delay?
        downstairs.changeSettings(current['DownNormHeat'] - LMHeatDelta, current['DownNormCool'] + LMCoolDelta, 'on', downMode)
    
    elif(currentMode == 'Island'):
        # Island Mode (a.k.a. isolated reduction)
        # Run Island Subprocess
        Island.Island(False)
        # 5 min should handle LM if Islanded
        upstairs.changeSettings(current['UpNormHeat'] - LMHeatDelta, current['UpNormCool'] + LMCoolDelta, 'on', upMode)
        # delay?
        downstairs.changeSettings(current['DownNormHeat'] - LMHeatDelta, current['DownNormCool'] + LMCoolDelta, 'on', downMode)
    
    else: #(currentMode == 'Normal')
        # Normal Mode    
        Island.GridTie()
        upstairs.changeSettings(current['UpNormHeat'], current['UpNormCool'], 'auto', upMode)
        # delay?
        upstairs.changeSettings(current['UpNormHeat'], current['UpNormCool'], 'auto', downMode)
else:
    print('Modes have not changed since last hour') 

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


