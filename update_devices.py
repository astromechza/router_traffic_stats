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

devices = router.get_connected_devices(wireless=config.include_wireless)
devices = [d for t in devices.values() for d in t]

devices_by_mac = {}
for d in devices:
    devices_by_mac[d[2]] = d

# load current traffic data
devices_data = store.read('devices', {'connected': [], 'events': []})
last_devices = devices_data['connected']
last_devices_by_mac = {}
for d in last_devices:
    last_devices_by_mac[d[2]] = d

# calculate changes
disconnected_by_mac = set(last_devices_by_mac) - set(devices_by_mac)
connected_by_mac = set(devices_by_mac) - set(last_devices_by_mac)

disconnected = [last_devices_by_mac[d] for d in disconnected_by_mac]
connected = [devices_by_mac[d] for d in connected_by_mac]

event = {
    'time': now_i
}

if len(connected) > 0:
    event['connected'] = list(connected)

if len(disconnected) > 0:
    event['disconnected'] = list(disconnected)

if len(event.keys()) > 1:

    devices_data['connected'] = list(set(devices))
    devices_data['events'] += [event]

    print connected
    print event

    # write out
    store.write('devices', devices_data)

    # write out as a javascript object
    SiteJavascript().write('devices_data', devices_data)
