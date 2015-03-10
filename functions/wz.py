#Weather from wunderground
import requests
import json

api_key = "" #An API key is required for this to work.


def wstring(zcode, metric):  #Use this - faster
 r = requests.get('http://api.wunderground.com/api/'+api_key+'/conditions/q/'+zcode+'.json')
 jso = json.loads(r.text)
 if metric == 1:
  lostr = jso['current_observation']['display_location']['full'] 
  cond = jso['current_observation']['weather']
  temp = str(jso['current_observation']['temp_c'])
  atm = str(jso['current_observation']['pressure_mb'])
  winddir = jso['current_observation']['wind_dir']
  winddeg = str(jso['current_observation']['wind_degrees'])
  windsp = str(jso['current_observation']['wind_kph'])
  humid = str(jso['current_observation']['relative_humidity'])
  return '<u>'+lostr+'</u> | Condition: '+cond+' | Temperature: '+temp+' C | Humidity: '+humid+' | Pressure: '+atm+' mb | Wind: '+winddir+'('+winddeg+') at '+windsp+' km/h'
 else:
  lostr = jso['current_observation']['display_location']['full'] 
  cond = jso['current_observation']['weather']
  temp = str(jso['current_observation']['temp_f'])
  atm = str(jso['current_observation']['pressure_in'])
  winddir = jso['current_observation']['wind_dir']
  winddeg = str(jso['current_observation']['wind_degrees'])
  windsp = str(jso['current_observation']['wind_mph'])
  humid = str(jso['current_observation']['relative_humidity'])
  return '<u>'+lostr+'</u> | Condition: '+cond+' | Temperature: '+temp+' F | Humidity: '+humid+' | Pressure: '+atm+' inHg | Wind: '+winddir+'('+winddeg+') at '+windsp+' MPH'
