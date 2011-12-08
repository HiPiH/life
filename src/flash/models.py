class Flash(dict):
    # make two commonly used flashes available as attributes
    error = property(lambda s: s.get('error', ""), lambda s, v: s.update({'error': v}))
    notice = property(lambda s: s.get('notice', ""), lambda s, v: s.update({'notice': v}))
    
    # if used as a string, return the first message found
    def __str__(self):        
        if len(self) > 0:
            return self.values()[0]
        return ""
    
    # allow {% for msg in flash %}{{ msg.type }}: {{ msg.msg }}{% endfor %}
    # this may not be necessary in newer versions of django where you should be
    # able to do: {% for key, value in flash %}{{ key }}: {{ value }}{% endfor %}
    def __iter__(self):
        for item in self.keys():
            yield {'type': item, 'msg': self[item]}
    
    # evaluate to True if there is at least one non-empty message
    def __nonzero__(self):
        return len(str(self)) > 0
