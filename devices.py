import urllib2
import re
import config
from datetime import datetime, tzinfo, timedelta
import time
import json
import os
import os.path

url = 'http://' + config.router_host + '/DEV_devices.htm'

passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, config.router_host, config.router_user, config.router_pwd)
authhandler = urllib2.HTTPBasicAuthHandler(passman)

opener = urllib2.build_opener(authhandler)
response = opener.open(url)
stuff = response.read()
response.close()

hostnames_regex = re.compile("<b>192\.[\s\S]*?<b>(.*?)</b>", re.MULTILINE)
wired_only_regex = re.compile("Wired Devices([\s\S]*?)Wireless Devices", re.MULTILINE)

devices = hostnames_regex.findall(stuff)

if not config.include_wireless:
    wiredregion = wired_only_regex.findall(stuff)[0]
    devices = hostnames_regex.findall(wiredregion)

now = datetime.now()
now_i = time.mktime(now.timetuple())

fn = 'devices'
fn_dir = os.path.expanduser(config.output_dir)
fn_dir = fn_dir if os.path.isabs(fn_dir) else os.path.abspath(fn_dir)
fn_js = os.path.join(fn_dir, fn+'.js')
fn_json = os.path.join(fn_dir, fn+'.json')

if not os.path.isdir(fn_dir):
    os.makedirs(fn_dir)

contents_o = {'devices': [], 'events': []}
try:
    with open(fn_json, 'r') as f:
        contents_j = f.read()
        contents_o = json.loads(contents_j)
except Exception, e:
    pass

disconnected = set(contents_o['devices']) - set(devices)
connected = set(devices) - set(contents_o['devices'])

event = ''
if len(connected) > 0:
    event += 'Connected ' + ', '.join(list(connected)) + ' '

if len(disconnected) > 0:
    event += 'Disconnected ' + ', '.join(list(disconnected)) + ' '

if event:

    contents_o['devices'] = list(set(devices))

    data = [now_i, event]

    contents_o['events'] += [data]

    with open(fn_json, 'w') as f:
        contents_j = json.dumps(contents_o)
        f.write(contents_j)

    with open(fn_js, 'w') as f:
        contents_j = json.dumps(contents_o)
        f.write('var device_data =' + contents_j + ';')