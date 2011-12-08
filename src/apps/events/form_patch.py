from django.forms import forms
from django.forms.fields import Field, FileField

def real_data(self):
    if not self.form.is_bound:
        data = self.form.initial.get(self.name, self.field.initial)
        if callable(data):
            data = data()
    else:    
        if isinstance(self.field, FileField) and self.data is None:
            data = self.form.initial.get(self.name, self.field.initial)
        else:
            data = self.data
    return data

forms.BoundField.real_data=real_data