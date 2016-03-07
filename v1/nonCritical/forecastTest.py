import urllib.request
import json
import pickle
from datetime import date, timedelta

key = '950e016d8128e849'
city = 'Lewisburg'


# Download tomorrow's weather forecast

#f = urllib.request.urlopen('http://api.wunderground.com/api/'+key+'/conditions/forecast/hourly/astronomy/q/PA/'+city+'.json')
#json_string = f.read()
#data = json.loads(json_string.decode("utf-8"))
#pickle.dump(data, open('forecast.p', 'wb'))

# ---- above or below, not both ----

data = pickle.load(open('forecast.p', 'rb'))

#print(data['hourly_forecast'][0]['FCTTIME']['mday'])

forecast=[]
sunrise = int(data['sun_phase']['sunrise']['hour'])
sunset =  int(data['sun_phase']['sunset']['hour'])

for hour in data['hourly_forecast']:
    if(int(hour['FCTTIME']['mday']) == (date.today()+timedelta(1)).day):
        d = {}
        d['hour'] = hour['FCTTIME']['hour']
        d['temp'] = hour['temp']['english']
        d['condition'] = hour['condition']
        if((int(d['hour']) > sunrise) and (int(d['hour']) < sunset)):
            d['daylight'] = True
        else:
            d['daylight'] = False
        forecast.append(d)




