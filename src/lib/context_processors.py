from django.conf import settings


def cp_admin(request):
    return {    
        'site_name': settings.SITE_NAME,
        'site_admin_name': settings.SITE_ADMIN_NAME,
    }