# coding: utf-8
from django import forms
from django.utils.safestring import mark_safe

class SelectGraphDate(forms.Widget):
    
    def render(self, name, value, attrs=None):
        if not value:
            value = ""
        return mark_safe(u"""
            <input type="text" id="%(name)s" name="%(name)s" value="%(value)s" readonly style="width: 80%%;">
            <input type="button" id="trigger%(name)s" value="..." style="width: 30px;">
            <script type="text/javascript">
              Calendar.setup(
                {
                  inputField  : "%(name)s",         // ID of the input field
                  ifFormat    : "%%Y-%%m-%%d",    // the date format
                  button      : "trigger%(name)s"       // ID of the button
                }
              );
            </script>
               """ % {'name': name, 'value': value})

class AdminDateTimeWidget(forms.widgets.SplitDateTimeWidget):
    
    def __init__(self, attrs=None):
        widgets = (forms.widgets.TextInput(attrs={'class': 'vDateField'}), 
                   forms.widgets.TextInput(attrs={'class': 'vTimeField'}))
        super(forms.widgets.SplitDateTimeWidget, self).__init__(widgets, attrs)
