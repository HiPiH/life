import datetime
def cp_admin(req):
    from django.conf import settings    
    return {    
                'site_name': settings.SITE_NAME,
                'site_admin_name': settings.SITE_ADMIN_NAME,
                'cur_date': datetime.date.today()
            }