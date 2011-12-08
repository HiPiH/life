from django.utils.translation   import ugettext_lazy as _

translations = (    _('po_editor'), _('Po_editor'), )

import settings
if hasattr(settings, 'MO_RELOADER'):
    if settings.MO_RELOADER:
        import mo_reloader