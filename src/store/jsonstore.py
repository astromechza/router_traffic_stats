import json
import copy
import os
import os.path

class JSONStore(object):

    def __init__(self, folder):
        super(JSONStore, self).__init__()

        # format folder path
        folder = os.path.expanduser(folder)
        self.directory = folder if os.path.isabs(folder) else os.path.abspath(folder)

        # create missing dirs
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)

    def read(self, name, default=[]):
        filename = os.path.join(self.directory, name + '.json')
        try:
            with open(filename, 'r') as f:
                contents_j = f.read()
                contents_o = json.loads(contents_j)
                return contents_o
        except Exception, e:
            return copy.deepcopy(default)

    def write(self, name, obj):
        filename = os.path.join(self.directory, name + '.json')
        with open(filename, 'w') as f:
            contents_j = json.dumps(obj)
            f.write(contents_j)
