# Changes in V3: Made all operations happen through a class, for easier access
# Changes in V4: Made the class functions better suited for the control system.  Cleaned up code better.

#Important Note: If both the access key and refresh key expire due to an incidental action, the application must be re-authicated with the authorize function.
#Data can only be posted every 15 seconds (or 30... need to verify) otherwise an error will occur.

#Note: thermostat time is in GMT: Four hour offset between UTC and thermostatTime.
#Thermostat Time = UTC - 4hr.
     
import pickle
import requests
import time
import json

#Access Credentials
API_Key = '1gquZ74nIEaz6B2z9tUqjqQCr0c7wnUy'
Scope = 'smartWrite'
payload = {'response_type':'ecobeePin', 'client_id':API_Key, 'scope':Scope}


class EcobeeThermostat:
    
    # Intializes the instance variables.
    def __init__(self):
        #Instantiates an object of type thermostat
        self.coolHoldTemp = None
        self.heatHoldTemp = None
        self.fan = None
        self.thermostatID = None
        self.needsAuthetication = False
        self.nameString = ""
        self.hvacMode = None
        self.actualTemp = None  #Note: This is only accurate immidiately following a refreshValues() call
        return
        
    def changeSettings(self, heatTemp, coolTemp, fanMode, hvacMode):
        #This is the main function to change the climate.  The pickle is automatically saved at the end of function.
        #INPUTS: coolTemp, heatTemp - These integers are the fahrenheit temperatures, times 10.  E.G. 64 deg F needs to be input as 640
        #        fanMode - A string that is either "on" or "auto" to control the fan mode
        #        hvacMode - A string that is either "auto", "auxHeatOnly", "cool", "heat", or "off"
        #OUTPUTS: Boolean Status Value.  True is returned if posted sucessfully.
        
   #Changes the hvac mode in the object before it is posted
        if (hvacMode != "auto" or hvacMode != "auxHeatOnly" or hvacMode != "cool" or hvacMode != "heat" or hvacMode != "off"):
           print("Wrong hvacMode input.")
           return
        else:
            self.hvacMode = hvacMode

   #Changes the Fan mode in the object before updating
        if fanMode != 'on' and fanMode != 'auto':
            print("The fan options are 'on' or 'auto', nothing else")
            return
        else:
            self.fan = fanMode

   #Changes the cool and heat hold temperatures before updating.
        if coolTemp < 400 or coolTemp > 1000:
            print("The input cool temperature is not within accepted range.")
            return
        else:
            self.coolHoldTemp = coolTemp

        if heatTemp < 400 or heatTemp > 1000:
            print("The input heat temperature is not within accepted range.")
            return
        else:
            self.heatHoldTemp = heatTemp

    #Posting occurs
        result = self.postToDevice()

    #Updates the pickle with what the thermostat was set to and returns appropriate boolean with appropriate status
        if result == True:
            self.postToPickle()
            return True
        else:
            return False




    def refreshValues(self):
    #This function polls ecobee for the states of the two thermostats and updates their pickles accordingly
    #INPUTS: None
    #OUTPUTS: None, though it does change the pickles
        
    #Setup headers for a query
        self.refreshToken()
        Headers()
        url_1 = 'https://api.ecobee.com/1/thermostat?json='\
                '{'\
                    "selection"':'\
                    '{'\
                        '"selectionType":"thermostats",'\
                        '"selectionMatch":"'
        identifier = str(self.thermostatID)
        url_2 = '","includeAlerts":"true",'\
                        '"selectionType":"registered",'\
                        '"selectionMatch":";'

        url_3 ='",'\
                        '"includeEvents":"true",'\
                        '"includeSettings":"true",'\
                        '"includeRuntime":"true"'\
                      '}'\
                  '}'
        url_t = url_1 + identifier + url_2 + url_3
        s = requests.get(url_t, headers = url_Headers)

    #JSON operations to make the json parsable.
        #PrintResponse(s)
        data = json.loads(s.text)

    #The simplification below will hold so long as there are only 2 thermostats in the system
        if int(data["thermostatList"][0]["identifier"]) == self.thermostatID:
            index = 0
        else:
            index = 1
            print("else")

        
        
    #Look for the the various parameters and save them
        print("fanMode")
        print(data["thermostatList"][index]["runtime"]["desiredFanMode"])

        print("heatHold")
        print(data["thermostatList"][index]["runtime"]["desiredHeat"])

        print("coolHold")
        print(data["thermostatList"][index]["runtime"]["desiredCool"])
        
        print("hvacMode")
        print(data["thermostatList"][index]["settings"]["hvacMode"])

        print("actualTemp")
        print(data["thermostatList"][index]["runtime"]["actualTemperature"])

        self.coolHoldTemp = int(data["thermostatList"][index]["runtime"]["desiredCool"])
        self.heatHoldTemp = int(data["thermostatList"][index]["runtime"]["desiredHeat"])
        self.fan = data["thermostatList"][index]["runtime"]["desiredFanMode"]
        self.hvacMode = data["thermostatList"][index]["settings"]["hvacMode"]
        self.actualTemp = int(data["thermostatList"][index]["runtime"]["actualTemperature"])

    #Stores the values into the thermostat object pickle
        self.postToPickle()

        return

######################################################################################################################################
### All functions below are helper functions, and can largely be ignored.
######################################################################################################################################

    def postToDevice(self):
        #This device is a wrapper to do the actual posting
        self.refreshToken()
        Headers()
        post_body = 'https://api.ecobee.com/1/thermostat?format=json&body='
        post_body_end = '}'
        # If you want a hold that only runs until a certain time, holdtype 
        #     becomes datetime, the number 4 changes to 6, and endtime and enddate parameters are needed
        url = post_body + Post_selection('thermostats', ""+str(self.thermostatID)+"", self.hvacMode) \
         + Post_function(4, 'setHold', 'fan', self.fan, 'heatHoldTemp', self.heatHoldTemp, 'coolHoldTemp',
         self.coolHoldTemp, 'holdType', 'indefinite') + post_body_end
        print(url)
        post = requests.post(url, headers = url_Headers)
        if post.status_code == 200:
            return True
        else:
            return False

    # Helper function to procure the refresh token.
    def refreshToken(self):
        file = open("Refresh.txt","r+")
        refresh_Token = file.read(49)
        file.close()    
        payload2 = {'grant_type': 'refresh_token','code':refresh_Token, 'client_id':API_Key}
        url_refresh = 'https://api.ecobee.com/token'
        p = requests.post(url_refresh, params = payload2)
       # PrintResponse(p)
        Refresh_json = p.json()
        Refresh_json_string = str(Refresh_json)
        
        Access_beg_string = Refresh_json_string.index('access_token', 0, len(Refresh_json_string))
        Access_temp_string = Refresh_json_string[Access_beg_string: Access_beg_string + 48]
        Access_Code = Access_temp_string[16:48]
        global Access_Token
        Access_Token = str(Access_Code)
        Refresh_beg_string = Refresh_json_string.index('refresh_token', 0, len(Refresh_json_string))
        Refresh_temp_string = Refresh_json_string[Refresh_beg_string: Refresh_beg_string + 49]
        Refresh_Code = Refresh_temp_string[17:49]
        Token = str(Refresh_Code)
        file = open("Refresh.txt", "r+")
        file.write(Token)
        file.close()
        return

    # Saves this instance in a similarly named pickle.
    def postToPickle(self):
        file = self.nameString + '.p'
        pickle.dump(self,open(file,'wb'))
        return
    
    
        
    
def Post_function(number_params, function_type, parameter_1, value_1, parameter_2 = 0 , value_2 = 0 , parameter_3 = 0, value_3 = 0, parameter_4 = 0, value_4 = 0, parameter_5 = 0, value_5 = 0,\
              parameter_6 = 0, value_6 = 0, parameter_7 = 0, value_7 = 0, parameter_8 = 0, value_8 = 0, parameter_9  = 0, value_9 = 0):
    '''Helper function.'''        
    parameter_list = [parameter_1, parameter_2, parameter_3, parameter_4, parameter_5, parameter_6, parameter_7, parameter_8, parameter_9]
    value_list = [value_1, value_2, value_3, value_4, value_5, value_6, value_7, value_8, value_9]
    parameter_string = [""] * (number_params)
    value_string = [""] * (number_params)
    function_body = '"functions":['\
                        '{"type":"'
    f_type = function_type
    function_type_string = str(f_type)
    function_body_params = '",'\
                        '"params":{'\
                        '"'
    for x in range(0,number_params):
        parameter_string[x] = str(parameter_list[x])
        x = x + 1
        
    for x in range(0,number_params):
        value_string[x] = str(value_list[x])
        x = x + 1
        
    function_body_break = '":"'
    function_body_comma = '", "'
    function_body_end = '"}}]'

    
    url_fn = function_body + function_type_string + function_body_params

    for x in range (0,number_params):
        fn = parameter_string[x] + function_body_break + value_string[x] + function_body_comma
        url_fn += fn
        
    url_function = url_fn[0:len(url_fn) - 4]
    url_function =  url_function + function_body_end
    
    print(url_function)
    print(parameter_string)
    print(value_string)
                   
    
    if (function_type == 0):
        return(0)
    else:
        return(url_function)
    
# Creates the nescessary headers.
def Headers():
    A = 'content_type'
    B = 'application/json;charset=UTF-8'
    C = 'authorization'
    T = Access_Token
    Access = str(T)
    D = 'Bearer '
    Token = D + Access
    global url_Headers
    url_Headers = {A: B,C: Token}
    #url_Headers = {'content_type': 'application/json;charset=UTF-8','authorization': 'Bearer lOyymgBi9X6ltSKVJ8oGfsu9NBxcoTwT'}


# This function is a helper function to print the various components of a request object.
#    Input is any request object.
def PrintResponse(x):
    print(x.headers)
    print()
    print(x.request.headers)
    print()
    print(x.json)
    print()
    print(x.text)
    print()
    print(x.url)
    print()
    print(x.status_code)
    print()

# Helper function.
def Post_selection(selection_type, selection_match, HVACMode):
    selection_body_A = '{"selection": {'\
                            '"selectionType":"'
    selection_type_string = str(selection_type)
    selection_body_B ='",'\
                        '"selectionMatch":"'
    selection_match_string = selection_match
    selection_body_C = '"},'
    url_selection = selection_body_A + selection_type_string + selection_body_B + selection_match_string + selection_body_C + '"thermostat": {' +'"settings":{' + '"hvacMode":"' + str(HVACMode) + '"}},'
    return(url_selection)

# A step by step process for authorizing a thermostat.  Bear in mind that this process
#    need only happen once a year, assuming the user does not mess the authorization up.
#    Inputs for this function are an object of class EcobeeThermostat 
#    (the thermostat for which to authorize)
def Authorize():
    print('Welcome to Authorization!')
    print()
    option = input('Press enter to begin, or type exit and enter to quit')
    if option != '':
        return
    print()
    #Setting Authorization Pin
    url_auth = 'https://api.ecobee.com/authorize'
    r = requests.get(url_auth, params = payload)
    PrintResponse(r)
    print("Locate the four digit key to the right of ecobeePin.  Go to ecobee.com, login, go the the settings tab \
open the apps tab on the left side of the screen, enter the four digit key, and return to idle")
    time.sleep(5)
    print()
    print()
    input("Once you have put this key into ecobee.com, hit enter in idle to contine with the authorization process")
    file = open("Refresh.txt","r+")
    refresh_Token = file.read(49)
    file.close()
    print()
    print()
    code = str(input("In the output of the shell, there should be a code that looks like 'MiDabdFefxh9SCDta6CjNa64caJeTLTE', copy the one that you got on this line (but without any quotes!!!!!), and press enter"))
    payload_auth = {'grant_type': 'ecobeePin','code':code, 'client_id':API_Key}
    url_refresh = 'https://api.ecobee.com/token'
    p = requests.post(url_refresh, params = payload_auth)
    PrintResponse(p)
    Refresh_json = p.json()
    Refresh_json_string = str(Refresh_json)
    Access_beg_string = Refresh_json_string.index('access_token', 0, len(Refresh_json_string))
    Access_temp_string = Refresh_json_string[Access_beg_string: Access_beg_string + 48]
    Access_Code = Access_temp_string[16:48]
    global Access_Token
    Access_Token = str(Access_Code)
    Refresh_beg_string = Refresh_json_string.index('refresh_token', 0, len(Refresh_json_string))
    Refresh_temp_string = Refresh_json_string[Refresh_beg_string: Refresh_beg_string + 49]
    Refresh_Code = Refresh_temp_string[17:49]
    Token = str(Refresh_Code)
    file = open("Refresh.txt", "r+")
    file.write(Token)
    file.close()
    ##Implement a check to look for the number 200, the sucess status code, towards the end of the file
    if r.status_code == 200:
        print()
        print()
        print("Authorization Complete!")
    else:
        Print(p)
        print()
        print()
        print("Your authorization may be not have suceeded.  See the above output to see if there was an error.")
    

downstairs = pickle.load(open("downstairs.p",'rb'))
upstairs = pickle.load(open("upstairs.p",'rb'))

##Authorize()
