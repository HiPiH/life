from flash.models import Flash

class Middleware:
    def process_response(self, request, response):        
        try:
            # make sure we never override an existing flash with an empty one.
            # otherwise non-pageview requests (like views.static.serve) will
            # override a previously set flash with the empty object created in
            # process_request(). Note that we use len(), so it is still possible
            # to clear a flash by setting the dict-item to ""
            if len(request.flash):
                request.session['flash'] = request.flash            
        except:
            pass
        return response
    
    def process_request(self, request):
        # Initialize a Flash dict that can be used in views      
        request.flash = Flash()