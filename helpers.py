import json
import copy
import os
import os.path

def load_json_object(filename, default):
    try:
        with open(filename, 'r') as f:
            contents_j = f.read()
            contents_o = json.loads(contents_j)
            return contents_o
    except Exception, e:
        return copy.deepcopy(default)

def dump_json_object(filename, obj):
    with open(filename, 'w') as f:
        contents_j = json.dumps(obj)
        f.write(contents_j)

def dump_json_object_in_js(filename, obj, varname):
    with open(filename, 'w') as f:
        contents_j = json.dumps(obj)
        f.write('var ' + varname + ' =' + contents_j + ';')

def get_json_js_filenames(folder, name):
    fn_dir = os.path.expanduser(folder)
    fn_dir = fn_dir if os.path.isabs(fn_dir) else os.path.abspath(fn_dir)
    fn_js = os.path.join(fn_dir, name+'.js')
    fn_json = os.path.join(fn_dir, name+'.json')

    if not os.path.isdir(fn_dir):
        os.makedirs(fn_dir)

    return fn_js, fn_json