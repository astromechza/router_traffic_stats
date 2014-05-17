import urllib2
import re
import config
from datetime import datetime, tzinfo, timedelta
import time
import json
import os
import os.path

url = 'http://' + config.router_host + '/traffic_meter.htm'
MB_to_bytes = 1024*1024




passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, config.router_host, config.router_user, config.router_pwd)
authhandler = urllib2.HTTPBasicAuthHandler(passman)

opener = urllib2.build_opener(authhandler)
response = opener.open(url)
stuff = response.read()
response.close()

regex = re.compile("^var report=(\[.*\]);", re.MULTILINE)
m = regex.search(stuff)

stats = eval(m.groups(1)[0])

today_s = stats[0][1:]
today_i = map(lambda s : float(s.split('/')[0])*MB_to_bytes, today_s)
now = datetime.now()
now = now.replace(microsecond=0, second=0)
now_i = time.mktime(now.timetuple())

data = [now_i, today_i]

fn = 'traffic'
fn_dir = os.path.expanduser(config.output_dir)
fn_dir = fn_dir if os.path.isabs(fn_dir) else os.path.abspath(fn_dir)
fn_js = os.path.join(fn_dir, fn+'.js')
fn_json = os.path.join(fn_dir, fn+'.json')

if not os.path.isdir(fn_dir):
    os.makedirs(fn_dir)

contents_o = []
try:
    with open(fn_json, 'r') as f:
        contents_j = f.read()
        contents_o = json.loads(contents_j)
except Exception, e:
    pass

contents_o += [data]

with open(fn_json, 'w') as f:
    contents_j = json.dumps(contents_o)
    f.write(contents_j)

with open(fn_js, 'w') as f:
    contents_j = json.dumps(contents_o)
    f.write('var traffic_data =' + contents_j + ';')
