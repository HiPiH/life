import time, os, sys, commands
import settings
from django.utils.daemonize import become_daemon
import threading

def write_log(str):
    f = open(os.path.join(settings.PROJECT_ROOT, "log.log"), "a")
    out = "%s     %s\n" % (time.time(),str)
    print out
    f.write(out)
    f.close()
    

class RestartThread(threading.Thread):
    
    def __init__(self, restart_file):
        super(RestartThread, self).__init__()
        self.restart_file = restart_file

    def run(self):
        try:
            time.sleep(1) # wait output
            become_daemon(our_home_dir=settings.PROJECT_ROOT)
            ret = commands.getoutput(self.restart_file)
            write_log("command return '%s'" % ret)
        except Exception, e:
            write_log("Exception: %s" % e)
        sys.exit(0)
    

def restart():
    if 'runserver' in sys.argv:
        print "Use console for reload"
        return
    
    restart_file = os.path.join(settings.PROJECT_ROOT, "restart.sh")
    if os.path.isfile(restart_file):
        m = RestartThread(restart_file)
        m.start()
    else:
        print "-----------------------------------------------------"
        print "|  restart.sh not found in '%s'" % settings.PROJECT_ROOT
        print "|  Please restart server"
        print "-----------------------------------------------------"
