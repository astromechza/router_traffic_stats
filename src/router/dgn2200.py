import urllib2
import re

class DGN2200(object):
    def __init__(self, host, user, password):
        super(DGN2200, self).__init__()
        self.host = host
        self.user = user
        self.password = password

    def _make_url(self, asset):
        return "http://%s/%s" % (self.host, asset)

    def _get(self, asset):
        url = self._make_url(asset)

        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, self.host, self.user, self.password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)

        opener = urllib2.build_opener(authhandler)
        response = opener.open(url)
        content = response.read()
        response.close()

        return content

    def get_connected_devices(self, wired=True, wireless=True):
        # get html from router
        devices_html = self._get('setup.cgi?todo=nbtscan&next_file=DEV_devices.htm')

        # compile some regex
        re_wired_devices_region = re.compile('Wired Devices[\s\S]*?<table([\s\S]*?)</table', re.IGNORECASE|re.MULTILINE)
        re_wireless_devices_region = re.compile('Wireless Devices[\s\S]*?<table([\s\S]*?)</table', re.IGNORECASE|re.MULTILINE)
        re_device = re.compile('<tr>[\s\S]*?<b>(.*?)</b>[\s\S]*?<b>(.*?)</b>[\s\S]*?<b>(.*?)</b></td></tr>')

        # output object
        devices = {}
        if wired:
            devices['wired'] = []
            # get wired table region
            wired_match = re_wired_devices_region.findall(devices_html)
            if len(wired_match) > 0:
                # get the devices
                devices['wired'] = re_device.findall(wired_match[0])

        if wireless:
            devices['wireless'] = []
            # get wireless table region
            wireless_match = re_wireless_devices_region.findall(devices_html)
            if len(wireless_match) > 0:
                # get the devices
                devices['wireless'] = re_device.findall(wireless_match[0])

        # return this object
        return devices

    def get_traffic_usage(self):

        # get html from router
        traffic_html = self._get('traffic_meter.htm')

        # compile regex
        re_report = re.compile("^var report=(\[.*?\]);", re.MULTILINE)

        # scan for traffic report variables
        report = eval(re_report.findall(traffic_html)[0])

        this_day = map(lambda s : float(s.split('/')[0])*1024*1024, report[0][1:])
        this_month = map(lambda s : float(s.split('/')[0])*1024*1024, report[3][1:])

        return {
            'day': {
                'upload': this_day[0],
                'download': this_day[1],
                'total': this_day[2]
            },
            'month': {
                'upload': this_month[0],
                'download': this_month[1],
                'total': this_month[2]
            }
        }


if __name__ == '__main__':
# ==============================
# A set of basic test methods
# ==============================

    def test_can_construct():
        d = DGN2200('127.0.0.1', 'admin', 'hunter2')
        assert d

    def test__make_url():
        d = DGN2200('127.0.0.1', 'admin', 'hunter2')
        assert d._make_url('dir/asset.htm?var1=2&var3') == 'http://127.0.0.1/dir/asset.htm?var1=2&var3'

    test_can_construct()
    test__make_url()

    print "tests passed"

