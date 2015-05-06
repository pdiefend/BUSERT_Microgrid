# 5 Minute Subprocess
# Run every 5 minutes 1 minute behind (i.e. 2:01, 2:06, 5:31, 10:56)

import Island
import pickle

def performLM():
    print('Managing Loads')
    # ================================================================
    # Waiting on Ecobee for Pre-heat/cool, and managed load reduction
    # Need to install and test WeMo for managed load reduction
    # ================================================================

# Load current status of system
current = pickle.load(open('pickles/current.p','rb'))

# check to see if we are islanded on the ATS
islanded = Island.IsIslanded()

# Check to see if islanded and we know it
if (islanded and ((current['mode'] == 'Island') or current['outage'])):
    # then perfrom LM tasks
    performLM()

# if islanded but we didn't know
elif islanded:
    # Update our current status
    current['outage'] = True
    Island.Island(True)
    # perform LM tasks
    performLM()

# otherwise we are not islanded
else:
    # Update our current status
    current['outage'] = False
    # we are done, no short-term LM necessary
    
pickle.dump(current, open('pickles/current.p', 'wb'))



