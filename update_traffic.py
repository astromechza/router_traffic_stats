import time
import config
import os.path
from datetime import datetime

from src.router.dgn2200 import DGN2200
from src.store.jsonstore import JSONStore
from src.store.site_javascript import SiteJavascript

store = JSONStore(os.path.join(os.path.dirname(__file__), 'data'))

router = DGN2200(config.router_host, config.router_user, config.router_pwd)

# get now time as seconds from epoch
now = datetime.now()
now = now.replace(microsecond=0, second=0)
now_i = int(time.mktime(now.timetuple())*1000)

# build data object
data = {
    'time': now_i,
    'data': router.get_traffic_usage()['day']
}

print data

# load current traffic data
traffic = store.read('traffic', [])

# append to current traffic data
traffic += [data]

# write out
store.write('traffic', traffic)

# write out as a javascript object
SiteJavascript().write('traffic_data', traffic)