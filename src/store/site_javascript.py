import json
import copy
import os
import os.path

class SiteJavascript(object):

    def __init__(self, directory=None):
        super(SiteJavascript, self).__init__()

        if directory:
            directory = os.path.expanduser(directory)
            self.directory = folder if os.path.isabs(folder) else os.path.abspath(folder)
        else:
            thisdir = os.path.dirname(__file__)
            self.directory = os.path.abspath(os.path.join(thisdir, '..', '..', 'site'))

        # create missing dirs
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)

    def write(self, variable_name, obj):
        filename = os.path.join(self.directory, variable_name + '.js')
        with open(filename, 'w') as f:
            contents_j = json.dumps(obj)
            f.write("var %s=%s;" % (variable_name, contents_j))
