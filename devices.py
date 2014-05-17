import urllib2
import re
import config
from datetime import datetime, tzinfo, timedelta
import time
import json
import os
import os.path

import helpers

# variables
url = 'http://' + config.router_host + '/setup.cgi?todo=nbtscan_refresh&this_file=DEV_devices.htm&next_file=DEV_devices.htm&SID='

# get devices html from router
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, config.router_host, config.router_user, config.router_pwd)
authhandler = urllib2.HTTPBasicAuthHandler(passman)

opener = urllib2.build_opener(authhandler)
response = opener.open(url)
stuff = response.read()
response.close()

# compile regex
hostnames_regex = re.compile("<b>192\.[\s\S]*?<b>(.*?)</b>", re.MULTILINE)
wired_only_regex = re.compile("Wired Devices([\s\S]*?)Wireless Devices", re.MULTILINE)

# get connected devices
devices = hostnames_regex.findall(stuff)

# ignore wireless devices if needs be
if not config.include_wireless:
    wiredregion = wired_only_regex.findall(stuff)[0]
    devices = hostnames_regex.findall(wiredregion)

print devices

# build now time object
now = datetime.now()
now = now.replace(microsecond=0, second=0)
now_i = time.mktime(now.timetuple())

# build filenames
fn_js, fn_json = helpers.get_json_js_filenames(config.output_dir, 'devices')

# load existing devices events
contents_o = helpers.load_json_object(fn_json, {'devices': [], 'events': []})

# calculate changes
disconnected = set(contents_o['devices']) - set(devices)
connected = set(devices) - set(contents_o['devices'])

# create event string
event = ''
if len(connected) > 0:
    event += 'Connected ' + ', '.join(list(connected)) + ' '

if len(disconnected) > 0:
    event += 'Disconnected ' + ', '.join(list(disconnected)) + ' '

print event

# if the event is worth mentioning
if event:
    # update current devices
    contents_o['devices'] = list(set(devices))

    # create data obj
    data = [now_i, event]

    # append new data
    contents_o['events'] += [data]

    # write out to js and json
    helpers.dump_json_object(fn_json, contents_o)
    helpers.dump_json_object_in_js(fn_js, contents_o, 'device_data')
