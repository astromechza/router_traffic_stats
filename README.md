# Router Traffic Monitor

I have a NETGEAR DGN2200v3 router at home and needed a method of graphing the daily network traffic volume over time. The DGN2200 has a handy taffic meter that logs the amount of traffic used in the day/month. This program scrapes that page and uses it to keep a running graph of the usage. Device connections or disconnections are added as tags above the graph and a ping test is performed to a local and a remote IP to measure latency.

## How it works:
Every 5 minutes cronjobs run update_traffic.py, update_devices.py, and update_pings.py. These scripts generate the javascript files that are loaded by the site and also store the dataset as a json object so that new data can be appended easily.
