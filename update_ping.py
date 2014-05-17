import time
import config
import os.path
from datetime import datetime

from src.commands.ping import ping
from src.store.jsonstore import JSONStore
from src.store.site_javascript import SiteJavascript

store = JSONStore(os.path.join(os.path.dirname(__file__), 'data'))

# construct now time object
now = datetime.now()
now = now.replace(microsecond=0, second=0)
now_i = int(time.mktime(now.timetuple())*1000)

# get pings
ping_local = ping(config.ping_local)
ping_remote = ping(config.ping_remote)

# construct output object
data = {'time': now_i}
if ping_local:
    data['local'] = ping_local
if ping_remote:
    data['remote'] = ping_remote

if len(data.keys()) > 1:
    print data

    # load current traffic data
    pings = store.read('pings', [])

    # append to current traffic data
    pings += [data]

    # write out
    store.write('pings', pings)

    # write out as a javascript object
    SiteJavascript().write('ping_data', pings)
