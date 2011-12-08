def context_processor(request):
    if 'flash' in request.session:        
        flash = request.session['flash']
        del request.session['flash']
        return {'flash': flash}
    return {'flash': None}