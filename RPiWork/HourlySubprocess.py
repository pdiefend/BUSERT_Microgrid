# Hourly Decision Subprocess
# Run on the hour

import pickle
import datetime
from WU import WU
import Island
import datetime


print('==================================================')
print('Hourly Subprocess')
print(str(datetime.datetime.now()))


# Unload LMP
lmp = pickle.load(open('pickles/LMP.p', 'rb'))

# Unload operationModes
hourModes = pickle.load(open('pickles/hourModes.p','rb'))

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

# Add preheat precool here, load pickle modify needed, and store back. Then look to get the HVAC setpt
current = {'conditions': conditions, 'mode': currentMode, 'lmp': currentLMP, 'outage': False}
pickle.dump(current, open('pickles/current.p','wb'))

# ================================================================
# Waiting on Ecobee for Pre-heat/cool, and managed load reduction
# Need to install and test WeMo for managed load reduction
# ================================================================


