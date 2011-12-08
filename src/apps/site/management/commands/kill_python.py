from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
import os, re, commands

class Command(BaseCommand):
    
    ps_split = re.compile("[\n\r]+")
    ps_pid = re.compile(r"^\s*(\d+)")
   
    def handle(self, *args, **options):
        verbosity = int(options['verbosity'])
        if verbosity==1:
            print "Kill FCGI..."
            
        if not args:
            raise CommandError('Not arguments found')
        
        patterns=[]
        for arg in args:
            patterns.append( re.compile(r"%s" % arg) )
        
        ps_out = commands.getoutput("ps ax | grep python | grep -v kill_python")
        for line in self.ps_split.split(ps_out):
            for pattern in patterns:
                if  pattern.search(line):
                    try:
                        pid = self.ps_pid.match(line).group()                    
                        os.kill(int(pid), 9)
                        print "Kill process: %s" % line
                    except Exceptoin, e:
                        print "Exception:", e
