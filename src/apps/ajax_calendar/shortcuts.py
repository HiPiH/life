

##template for context_processor
#def context_processor(req, processor_type):
#    def func(req):
#        return {'ajax_calendar': processor_type(req)}
#    return func
#
##template for view
#def view(processor_type):
#    def func(req, cur_date, ):
#        out={}
#        calendar = processor_type(req, cur_date)
#        out['ajax_calendar'] = calendar
#    return func

