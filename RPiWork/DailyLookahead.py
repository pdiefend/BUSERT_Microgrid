# Daily-Lookahead Subprocess

# Run at 11:30 p.m.

from WU import WU
from D_LMP_Downloader import LMP_Downloader
import pickle
import datetime


print('==================================================')
print('Daily Lookahead')
print(str(datetime.datetime.now()))

# User parameters
LM_Threshold = 60 # arbitrarily set for now
CM_Threshold = 0
Gen_Threshold = 170

HVAC_Setpoint = 70 # will need to be checked against the Ecobee


# Download the Weather Data
weather = WU('Lewisburg')
weather.refresh()
hourlyForecast = weather.hourly_forecast()

# Download Tomorrow's LMP Data
lmpDL = LMP_Downloader('PPL')
lmp = lmpDL.DL_LMP()

# ======================================================================
# Place testing arrays here
#lmp = [25, 24, 24, 24, 200, 28, 50, 48, 49, 38, 47, 57,
# 58, 60, 90, 120, 160, 250, 260, 220, 190, 20, 0, -10]

#hourlyForecast = [{'daylight': False, 'hour': '0',  'temp': '36', 'condition': 'Clear'},
#                  {'daylight': False, 'hour': '1',  'temp': '34', 'condition': 'Clear'},
#                  {'daylight': False, 'hour': '2',  'temp': '33', 'condition': 'Clear'},
#                  {'daylight': False, 'hour': '3',  'temp': '32', 'condition': 'Clear'},
#                  {'daylight': False, 'hour': '4',  'temp': '31', 'condition': 'Clear'},
#                  {'daylight': False, 'hour': '5',  'temp': '30', 'condition': 'Clear'},
#                  {'daylight': False, 'hour': '6',  'temp': '30', 'condition': 'Clear'},
#                  {'daylight': True,  'hour': '7',  'temp': '32', 'condition': 'Clear'}, 
#                  {'daylight': True,  'hour': '8',  'temp': '36', 'condition': 'Clear'}, 
#                  {'daylight': True,  'hour': '9',  'temp': '41', 'condition': 'Clear'}, 
#                  {'daylight': True,  'hour': '10', 'temp': '45', 'condition': 'Clear'}, 
#                  {'daylight': True,  'hour': '11', 'temp': '49', 'condition': 'Clear'}, 
#                  {'daylight': True,  'hour': '12', 'temp': '53', 'condition': 'Clear'}, 
#                  {'daylight': True,  'hour': '13', 'temp': '56', 'condition': 'Partly Cloudy'}, 
#                  {'daylight': True,  'hour': '14', 'temp': '58', 'condition': 'Partly Cloudy'}, 
#                  {'daylight': True,  'hour': '15', 'temp': '59', 'condition': 'Partly Cloudy'}, 
#                  {'daylight': True,  'hour': '16', 'temp': '59', 'condition': 'Partly Cloudy'}, 
#                  {'daylight': True,  'hour': '17', 'temp': '59', 'condition': 'Partly Cloudy'}, 
#                  {'daylight': True,  'hour': '18', 'temp': '58', 'condition': 'Partly Cloudy'}, 
#                  {'daylight': False, 'hour': '19', 'temp': '56', 'condition': 'Mostly Cloudy'},
#                  {'daylight': False, 'hour': '20', 'temp': '52', 'condition': 'Mostly Cloudy'}, 
#                  {'daylight': False, 'hour': '21', 'temp': '50', 'condition': 'Mostly Cloudy'}, 
#                  {'daylight': False, 'hour': '22', 'temp': '47', 'condition': 'Overcast'}, 
#                  {'daylight': False, 'hour': '23', 'temp': '45', 'condition': 'Overcast'}]
#
# ======================================================================

pickle.dump(lmp, open('pickles/LMP.p','wb'))
hourModes = []

# Iterate through all hours to plan the day
for hour in range(0, 24):
    if(lmp[hour] > LM_Threshold):
        # If high PV output expected:
        if(((hourlyForecast[hour]['condition'] == 'Clear') or (hourlyForecast[hour]['condition'] == 'Partly Cloudy')) and hourlyForecast[hour]['daylight']):
            hourModes.append('LM')
        else:
            if (lmp[hour] > Gen_Threshold):
                hourModes.append('Island')
            else:
                hourModes.append('LM')
    elif (lmp[hour] < CM_Threshold):
        hourModes.append('Consume')
    else:
        hourModes.append('Normal')


# This does not make use of most opportune times to pre-heat/pre-cool

prepHours = 4

# If needed, pre-heat or pre-cool
for hour in range(2, 24):
    #print(hourModes[hour])
    # First compare setpoint against forecast to determine if 
    #you can pre-heat/cool and which you should do 
    if((hourModes[hour] == 'LM' or hourModes[hour] == 'Island') and ((HVAC_Setpoint+0) < int(hourlyForecast[hour]['temp']))):
        # Pre-cooling the previous 3 hours
        for i in range(1,(prepHours+1)):
            if((hourModes[hour-i] == 'Normal' or hourModes[hour-i] == 'Consume') and (hour-i) >= 0):
                hourModes[hour-i] = 'Pre-cool'
   
    elif((hourModes[hour] == 'LM' or hourModes[hour] == 'Island')  and ((HVAC_Setpoint-0) > int(hourlyForecast[hour]['temp']))):
        # Pre-heating the previous 3 hours
        for i in range(1,(prepHours+1)):
            if((hourModes[hour-i] == 'Normal' or hourModes[hour-i] == 'Consume') and (hour-i) >= 0):
                hourModes[hour-i] = 'Pre-heat'

print('\noutput\n')
for hour in hourModes:
    print(hour)

# Store Hour Modes in a pickle
pickle.dump(hourModes, open('pickles/hourModes.p','wb'))

# all hour Modes == Normal, Pre-heat, Pre-cool, Consumption, LM, Island and Outage

