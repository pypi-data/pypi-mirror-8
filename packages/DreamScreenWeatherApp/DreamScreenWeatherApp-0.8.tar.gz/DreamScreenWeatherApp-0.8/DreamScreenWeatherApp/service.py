import os
import socket
import sys
import time
import json
import re
import requests
from flask import Flask, render_template, request, redirect, url_for, abort, session
from subprocess import call
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)s:%(message)s', level=logging.DEBUG)
logging.info('DreamScreen Weather App service startup')

_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_data(path):
    return os.path.join(_ROOT, path)

logging.debug(_ROOT)
# global section
app = Flask(__name__, instance_relative_config=False)
app.debug=True
app.config.from_pyfile('instance/weatherservice-config.py')
logging.debug(app.config)
#app.config.from_envvar('WEATHERSERVICE-CONFIG', silent=True)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# map of icons to weather string
with open(get_data('etc/weather_map.json'), 'r') as map_data:
    icon = json.load(map_data)
 
# global weather data response holder 
wdata = {}

# url end-point handlers
@app.route('/old_getLiveWeatherRSS.aspx', methods=['POST','GET'])
def old_getLiveWeatherRSS():
    global wdata
    mode='live'
    wdata = getWeatherData(app.config['QUERY_URL'])
    obs=wdata['current_observation']
    date=obs['date']
    if date['hour'] > 12:
        hr=date['hour']-12
    else:
        hr=date['hour']    
    iconKey = obs['icon']
    icon.setdefault(iconKey,  10)
    iconLive = icon [ iconKey ]
    logging.debug('%s = %s' % (iconKey,  iconLive))
    writeLog(mode)
    return render_template('getLiveWeatherRSS.html', obs = obs, date = date, hr = hr, iconLive = iconLive,  weburl = app.config['QUERY_URL'])

@app.route('/getLiveWeatherRSS.aspx', methods=['POST','GET'])
def getLiveWeatherRSS():
#    global wdata
    mode='live'
    source_url = app.config['API_URL'] + app.config['API_KEY'] + app.config['API_CONDITIONS'] + 'pws:' + app.config['PWS'] + '.' +app.config['FORMAT']
    r = requests.get(source_url)
    logging.debug(r)
    data = r.json()
    logging.debug(data)
    obs=data['current_observation']
    iconKey = obs['icon']
    icon.setdefault(iconKey,  10)
    iconLive = icon [ iconKey ]
    logging.debug('%s = %s' % (iconKey,  iconLive))
    writeLog(mode)
    return render_template('getLiveWeatherApi.html', obs = obs, iconLive = iconLive,  weburl = source_url)

# forecast is called After liveWeather so we will reuse the wdata variable.
@app.route('/old_getForecastRSS.aspx', methods=['POST','GET'])
def old_getForecastRSS():
    global wdata
    forecasts = []
    mode='forecast'
    loc=wdata['response']['location']
    for i in range(0, 5):
        fc=wdata['forecast']['days'][i]
        if fc['summary']['pop'] > 0:
            short_prediction = '%s%% %s' % (fc['summary']['pop'],fc['summary']['condition'])
        else:
            short_prediction = fc['summary']['condition']  
        fc['summary']['short_prediction'] = short_prediction            
        iconKey = fc['summary']['icon']
        icon.setdefault(iconKey,  10)
        forecasts.append(fc)    
            
    now=datetime.now().strftime("%m/%d/%y %H:%M:%S %p")
    writeLog(mode)
    return render_template('getForecastRSS.html', loc = loc, forecasts = forecasts, icon = icon, now = now)

@app.route('/getForecastRSS.aspx', methods=['POST','GET'])
def getForecastRSS():
    logging.info('Getting weather data via API')
    find_key = 'forecast'
    source_url = app.config['API_URL'] + app.config['API_KEY'] + app.config['API_FORECAST']+ 'pws:' + app.config['PWS'] + '.' +app.config['FORMAT']
#    logging.debug(source_url)
    r = requests.get(source_url)
#    logging.debug(r)
    data = r.json()
    forecasts=[]
#    logging.debug(data)
    mode='forecast'
    loc=data['response']['features']
    logging.debug(loc)
    for i in range(0, 5):
        fc=data[mode]['simpleforecast']['forecastday'][i]
 #       logging.debug(fc)
        # pop is probability of precipitation
        if fc['pop'] > 0:
            short_prediction = '%s%% %s' % (fc['pop'], fc['conditions'])
        else:
            short_prediction = fc['conditions']  
 #       logging.debug(short_prediction)
        fc['short_prediction'] = short_prediction            
        iconKey = fc['icon']
        icon.setdefault(iconKey,  10)
        forecasts.append(fc)    
     
#    logging.debug(forecasts)
    now=datetime.now().strftime("%m/%d/%y %H:%M:%S %p")
    writeLog(mode)
    return render_template('getForecastApi.html', loc = loc, forecasts = forecasts, icon = icon, now = now)

@app.route('/getLocationsXML.aspx', methods=['POST','GET'])
def getLocationsXML():
    mode='locations'
    key = request.args.get('SearchString')
    obj = { 'primary_city' : app.config['CITY'], 'state' : app.config['STATE'], 'country': app.config['COUNTRY'], 'zip': app.config['ZIPCODE'] }
    writeLog(key)
    return render_template('getLocationsXML.html', loc = obj)

@app.route('/verify', methods=['POST','GET'])
def verify():
    global wdata
    logging.info('verifying setup')
    mode='verify'
    wdata = getWeatherData(app.config['QUERY_URL'])
    loc=wdata['response']['location']
    obs=wdata['current_observation']
    date=obs['date']
    writeLog(mode)
    return render_template('verify.html', obs = obs, date = date, loc = loc)

# returns a json data object
def getWeatherData(source_url):
    logging.info('Getting weather data')
#    find_key = 'wui\.bootstrapped\.API'
#    find_key = 'wui\.bootstrapped\.pwsdashboard'
    find_key = 'wui\.api_data'
    r = requests.get(source_url)
    soup = BeautifulSoup(r.text)
    script = soup.find('script', text=re.compile(find_key))
    logging.debug(script)
    json_text = re.search(r'^\s*' + find_key + '\s*=\s*({.*?})\s*;\s*$', script.string, flags=re.DOTALL | re.MULTILINE).group(1)
    json_text = re.sub('[|]', '', json_text)
    #logging.debug(json_text)
    data = json.loads(json_text)
    logging.debug(data)
    assert data['response']['version'] == '2.0'
    return data
	
def writeRequestParams(mode):
    with open(app.instance_path + '/../static/' + mode + "." + session['id'] + '.params','w') as f:
        for p in request.args:
            f.write('%s = %s\n' % (p, request.args.get(p))) 

def writeLog(mode):
    now = time.strftime("%Y-%m-%d-%H:%M:%S")
    with open(app.instance_path + '/../logs/webservice.log', 'a') as f:
        f.write('%s %s\n' % (now,  mode))

if __name__ == '__main__':
    if socket.gethostname() == 'ubuntu':
        app.run(host='0.0.0.0',  port=8080)
    else:
        app.run(host='0.0.0.0', port=80)

