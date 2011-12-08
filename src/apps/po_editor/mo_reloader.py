import os, sys
from django.utils import autoreload

old_code_changed = autoreload.code_changed

_gettext_mo_list = None
#_mtimes = {}

def get_all_mo_files(path):
    ret={}
    for item in os.listdir(path):
        name = os.path.join(path, item)
        if os.path.isdir(name):
          ret.update(get_all_mo_files(name))
        if os.path.isfile(name):
            if name.endswith(".mo"):
                stat = os.stat(name)
                ret[name] = stat.st_mtime
    return ret  

def my_code_changed():
    if old_code_changed():
        return True

    global _gettext_mo_list
    if not _gettext_mo_list:
        import settings
        _gettext_mo_list = get_all_mo_files(settings.PROJECT_ROOT)
        #Load all po files for list
        
    for filename in _gettext_mo_list:
        try:
            stat = os.stat(filename)
        except:
            _gettext_mo_list = None
            return True
        if stat.st_mtime!=_gettext_mo_list[filename]:
            _gettext_mo_list = None
            return True            
    return False
    

autoreload.code_changed = my_code_changed
#print "reloader"