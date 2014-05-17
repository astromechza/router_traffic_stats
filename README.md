# router_traffic_logger

I have a NETGEAR DGN2200v3 router at home and needed a method of graphing the daily network traffic volume over time.

Device connections or disconnections are added as tags above the graph.

May be updated to show current down/up speeds or any other router stats.

## How it works:
Every 5 minutes cronjobs run main.py, devices.py, and pingtest.py. These scripts generate the javascript files that are loaded by the site and also store the dataset as a json object so that new data can be appended easily.