"""
author:Kovalenko Pavel (ice.tegliaf@gmail.com)
"""

from django.core.urlresolvers import *
from django.core import urlresolvers
  
def RegexURLPattern_resolve2(self, path):
    match = self.regex.search(path)
    if match:
        # If there are any named groups, use those as kwargs, ignoring
        # non-named groups. Otherwise, pass all non-named arguments as
        # positional arguments.
        kwargs = match.groupdict()
        if kwargs:
            args = ()
        else:
            args = match.groups()
        # In both cases, pass any extra_kwargs as **kwargs.
        kwargs.update(self.default_args)

        return self, args, kwargs

urlresolvers.RegexURLPattern.resolve2 = RegexURLPattern_resolve2

def RegexURLResolver_resolve2(self, path):
        tried = []
        match = self.regex.search(path)
        if match:
            new_path = path[match.end():]
            for pattern in self.url_patterns:
                try:
                    ret = pattern.resolve2(new_path)
                except Resolver404, e:
                    tried.extend([(pattern.regex.pattern + '   ' + t) for t in e.args[0]['tried']])
                else:
                    if ret:
                        return ret
                    tried.append(pattern.regex.pattern)
            raise Resolver404, {'tried': tried, 'path': new_path}
        
        
urlresolvers.RegexURLResolver.resolve2 = RegexURLResolver_resolve2

def resolve2(path, urlconf=None):
    return get_resolver(urlconf).resolve2(path)

urlresolvers.resolve2 = resolve2