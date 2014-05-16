import re
import subprocess
import config
from datetime import datetime, tzinfo, timedelta
import time
import json
import os
import os.path

def pingcheck(remote):
    count = 5
    try:
        ping = subprocess.Popen(["ping", "-n", "-c " + str(count), remote], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error = ping.communicate()
        if out:
            try:
                lost_perc = float(re.findall(r'received, (.*)\% p', out)[0])
                lost = int(round(count * lost_perc / 100.0))
                stats_s = re.findall(r'mdev = (.*) ms', out)[0]
                stats_s_parts = stats_s.split('/')
                minimum = float(stats_s_parts[0])
                average = float(stats_s_parts[1])
                maximum = float(stats_s_parts[2])
                return [minimum, average, maximum, lost]
            except Exception as e:
                print e
                return None
        else:
            return None
    except subprocess.CalledProcessError:
        return None



now = datetime.now()
now_i = time.mktime(now.timetuple())

ping_local = pingcheck(config.ping_local)
ping_remote = pingcheck(config.ping_remote)

data = {'time': now_i}
if ping_local:
    data['local'] = ping_local
if ping_remote:
    data['remote'] = ping_remote

fn = 'pings'
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

if len(data.keys()) > 1:
    contents_o += [data]

    with open(fn_json, 'w') as f:
        contents_j = json.dumps(contents_o)
        f.write(contents_j)

    with open(fn_js, 'w') as f:
        contents_j = json.dumps(contents_o)
        f.write('var ping_data =' + contents_j + ';')
