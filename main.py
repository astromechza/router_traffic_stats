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
url = 'http://' + config.router_host + '/traffic_meter.htm'
MB_to_bytes = 1024*1024

# get file from router
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, config.router_host, config.router_user, config.router_pwd)
authhandler = urllib2.HTTPBasicAuthHandler(passman)

opener = urllib2.build_opener(authhandler)
response = opener.open(url)
stuff = response.read()
response.close()

# scan for traffic report variables
regex = re.compile("^var report=(\[.*\]);", re.MULTILINE)
m = regex.search(stuff)

# get as python object
stats = eval(m.groups(1)[0])

# get todays totals so far
today_s = stats[0][1:]
today_i = map(lambda s : float(s.split('/')[0])*MB_to_bytes, today_s)

# get now time as seconds from epoch
now = datetime.now()
now = now.replace(microsecond=0, second=0)
now_i = time.mktime(now.timetuple())

# build data object
data = [now_i, today_i]

# build output filenames
fn_js, fn_json = helpers.get_json_js_filenames(config.output_dir, 'traffic')

# load current traffic data
contents_o = helpers.load_json_object(fn_json, [])

# append to current traffic data
contents_o += [data]

# write out object and corrosponding js
helpers.dump_json_object(fn_json, contents_o)
helpers.dump_json_object_in_js(fn_js, contents_o, 'traffic_data')
