import re
import subprocess
import config
from datetime import datetime, tzinfo, timedelta
import time
import json
import os
import os.path

import helpers

# ping method for unix
def pingcheck(remote):
    count = 5
    try:
        # spawn subprocess with pipes
        ping = subprocess.Popen(["ping", "-n", "-c " + str(count), remote], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error = ping.communicate()
        # if there was output
        if out:
            try:
                # read fields using regex!
                lost_perc = float(re.findall(r'received, (.*)\% p', out)[0])
                lost = int(round(count * lost_perc / 100.0))
                stats_s = re.findall(r'mdev = (.*) ms', out)[0]
                stats_s_parts = stats_s.split('/')
                minimum = float(stats_s_parts[0])
                average = float(stats_s_parts[1])
                maximum = float(stats_s_parts[2])
                # return stats
                return [minimum, average, maximum, lost]
            except Exception as e:
                print e
                return None
        else:
            return None
    except subprocess.CalledProcessError:
        return None


# construct now time object
now = datetime.now()
now = now.replace(microsecond=0, second=0)
now_i = time.mktime(now.timetuple())

# get pings
ping_local = pingcheck(config.ping_local)
ping_remote = pingcheck(config.ping_remote)

# construct output object
data = {'time': now_i}
if ping_local:
    data['local'] = ping_local
if ping_remote:
    data['remote'] = ping_remote

# build filenames
fn_js, fn_json = helpers.get_json_js_filenames(config.output_dir, 'pings')

# load existing data
contents_o = helpers.load_json_object(fn_json, [])

# if pings were successful
if len(data.keys()) > 1:
    # append
    contents_o += [data]

    #write out
    helpers.dump_json_object(fn_json, contents_o)
    helpers.dump_json_object_in_js(fn_js, contents_o, 'ping_data')
