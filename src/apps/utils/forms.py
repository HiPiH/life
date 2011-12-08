from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


from django.forms.fields import EMPTY_VALUES, Field
from django.forms import ValidationError
import re
from django.utils.encoding import smart_unicode

__all__ = ('DynamicChoicesSelect', 'SelectGraphDate', 'DEFAULT_DATETIME_INPUT_FORMATS',
           'CustomForm', 'CustomModelForm', 'RU_PhoneNumberField','JSCal2Date',
           'CKEditor'
           )

"""
Author Kovalenko Pavel (pavel@kengine.com)
"""
class PreviewFileWidget(forms.FileInput):

    def render(self, name, value, attrs=None):
        out = ''
        if value and type(value)!=datastructures.FileDict:
            out = '<a href="http://%s%s%s" target="_blank">%s</a> <br/>' % (Site.objects.get(id=SITE_ID).domain, MEDIA_URL,value,value)
        out = out + super(PreviewFileWidget,self).render( name, value, attrs)
        return out
    
    def value_from_datadict(self, data, files, name):
        "File widgets take data from FILES, not POST"
        return files.get(name, None)

        
def as_table(self):
    top_errors = self.non_field_errors() # Errors that should be displayed above all fields.
    fields=[]        
    for name, field in self.fields.items():
        bf = forms.forms.BoundField(self, field, name)
        fields.append(bf)
    return render_to_string('utils/custom_form.html' ,{'fields': fields, 'top_errors':top_errors})
        
class CustomForm(forms.Form):
    as_table = as_table


class CustomModelForm(forms.ModelForm):
    as_table = as_table

"""
Author Kovalenko Pavel (ice.tegliaf@gmail.com)
"""
class DynamicChoicesSelect(forms.Select):
     
    def __init__(self, objects, titleName='title', required=True, attrs=None, empty_label=u"---"):
        super(DynamicChoicesSelect, self).__init__(attrs)
        self.objects=objects
        self.required=required
        self.titleName=titleName
        self.empty_label = empty_label
        
    def render(self, name, value, attrs=None, choices=()):
        self.choices=()
        if not self.required:
            self.choices += ((0,self.empty_label),)
        all=list(self.objects.filter())
        for p in all:
            self.choices += ((p.id,unicode(p)),)            
        return super(DynamicChoicesSelect,self).render( name, value, attrs)
    
    
#def form_view(out, object_type, form_class, redirect):
#    out['object'] = project = get_object_or_404(object_type, pk=id) if id else object_type()
#    if req.method == 'POST':
#        form = form_class(req.POST, instance = project, )
#        if form.is_valid():
#            form.save()
#            return HttpResponseRedirect(redirect)
#            #reverse('apps.plan.views.project', args=(project.id,))
#    else:
#        form = form_class(instance=project)
#    
#    out['form'] = form

DEFAULT_DATETIME_INPUT_FORMATS = (
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
    '%m/%d/%Y',              # '10/25/2006'
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
    '%m/%d/%y',              # '10/25/06'

    '%d.%m.%Y %H:%M',        # '10/25/2006 14:30'
)


class SelectGraphDate(forms.Widget):
    
    def __init__(self, calendar_args = {}):
        self.calendar_args = calendar_args
        super(SelectGraphDate, self).__init__()
    
    def render(self, name, value, attrs=None):
        if not value:
            value = ""
        self_args = {
                    'inputField':   "\"%(name)s\"" % {'name': name, },
                    'ifFormat':     "\"%Y-%m-%d\"",
                    'button':       "\"trigger%(name)s\"" % {'name': name, }
                    }
        
        self_args.update(self.calendar_args)
        
        str_args = ",\n".join(map(lambda e: "%s:%s" % (e, self_args[e]), self_args))
        out={'name': name, 'value': value, 'str_args':str_args}
        return render_to_string('utils/select_graph_date.html', out)
#        return mark_safe("""
#            <input type="text" id="%(name)s" name="%(name)s" value="%(value)s" readonly>
#            <input type="button" id="trigger%(name)s" value="...">
#            <script type="text/javascript">
#              Calendar.setup(
#                {
#                  %(str_args)s
#                }
#              );
#            </script>
#               """ % {'name': name, 'value': value, 'str_args':str_args})
#

#phone_digits_re = re.compile(r'^(?:1-?)?(\d{3})[-\.]?(\d{3})[-\.]?(\d{4})$')
#phone_digits_re = re.compile(r'^\+(\d{1,3})\(\d{3}\)(\d{3})-(\d{2})-(\d{2})$')

phone_digits_re=(
    re.compile(r'^\((\d{3})\)(\d{3})-(\d{2})-(\d{2})$'),
    re.compile(r'^\((\d{4})\)(\d{2})-(\d{2})-(\d{2})$'),
    re.compile(r'^\((\d{5})\)(\d{1})-(\d{2})-(\d{2})$'),
#    re.compile(r'^((\d{3}))$'),
#    re.compile(r'^\((\d{6})\)[\s]*(\d{2})-(\d{2})$'),
)

        
class RU_PhoneNumberField(Field):
    """Russian phone number field."""
    default_error_messages = {
        'invalid': _(u'Phone numbers must be in:\n(XXX) XXX-XX-XX,\n(XXXX) XX-XX-XX,\n(XXXXX) X-XX-XX   formats.'),
    }

    def clean(self, value):
        """Validate a phone number.
        """
#        print "-----------------|%s|------------------!!!" % value
        super(RU_PhoneNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        value = re.sub('(\s+)', '', smart_unicode(value))
#        print value
        for pd_re in phone_digits_re:
            m = pd_re.search(value)
            if m:
                value =  u'(%s) %s-%s-%s' % (m.group(1), m.group(2), m.group(3), m.group(4))
                return value
        raise ValidationError(self.error_messages['invalid'])


class JSCal2Date(forms.Widget):
    class Media:
        js = (
              'jscal2_1_7/js/jscal2.js',
              'jscal2_1_7/js/lang/ru.js',  #TODO: change for current lang
              )
        css = {"":
               ('jscal2_1_7/css/jscal2.css',
               'jscal2_1_7/css/border-radius.css',
               'jscal2_1_7/css/steel/steel.css',)
               }    
    
    def __init__(self, calendar_args = {}):
        self.calendar_args = calendar_args
        super(JSCal2Date, self).__init__()
    
    def render(self, name, value, attrs=None):
        if not value:
            value = ""
        self_args = {
                    'inputField':   "\"%(name)s\"" % {'name': name, },
                    'format':     "%Y-%m-%d",
                    'button':       "\"trigger%(name)s\"" % {'name': name, }
                    }
        
        self_args.update(self.calendar_args)
        
        str_args = ",\n".join(map(lambda e: "%s:%s" % (e, self_args[e]), self_args))
        return mark_safe("""
            <input id="id_%(name)s" name="%(name)s" value="%(value)s"/>
            <a href="#" id="btn%(name)s"><img src="/media/jscal2_1_7/ico-callendare.png" alt="ico"></a>

            <script type="text/javascript">
              var cal_%(name)s = Calendar.setup(
                  {
                      onSelect: function(cal_%(name)s) { cal_%(name)s.hide() }
                  }
              );
              cal_%(name)s.manageFields("btn%(name)s", "id_%(name)s", "%(format)s");
            </script>
               """ % {'name': name, 'value': value, 'str_args':str_args,'format':self_args['format']})


class CKEditor(forms.Widget):
    
    def render(self, name, value, attrs=None):
        if not value:
            value=""
        final_attrs = self.build_attrs(attrs, name=name, value=value)
        return mark_safe("""<textarea id="%(id)s" name="%(name)s">%(value)s</textarea>
<script type="text/javascript">
//<![CDATA[
    CKEDITOR.replace( "%(id)s" );
//]]>
</script>
    """ % final_attrs)
    
    class Media:
        js = ("ckeditor/ckeditor.js",
              "ckeditor/config.js"
              )