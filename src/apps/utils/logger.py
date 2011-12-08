
import codecs
import datetime

class Logger():
    def __init__(self):
        import settings
        if hasattr(settings, 'LOG_PATH_NAME'):
#            self.f = codecs.open(os.path.join(settings.LOG_PATH, 'django.log'), 'awt', 'utf-8')
            self.f = codecs.open(settings.LOG_PATH_NAME, 'awt', 'utf-8')
        else:
            self.f=None
        
    def write(self, str):
        if hasattr(self, 'f'):
            self.f.write("%s: %s \n" % (datetime.datetime.today(),unicode(str)))            
            self.f.flush()
            
        
log = Logger()