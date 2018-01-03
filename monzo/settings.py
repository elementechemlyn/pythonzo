import json
import os

settings_file = None
for loc in os.curdir, os.path.expanduser("~"), "/etc/monzoapi", os.environ.get("MONZOAPI_CONF"):
    if loc:
        fname = os.path.join(loc,"monzosettings.json")
        if os.path.isfile(fname):
            settings_file = fname

if settings_file==None:
    raise IOError("Settings file not found")

def load_settings():
    f = open(settings_file)
    settings = json.loads(f.read())
    f.close()
    return settings

settings = load_settings()

def save_settings(settings=settings):
    f = open(settings_file,"w")
    f.write(json.dumps(settings,indent=1))
    f.close()
    

