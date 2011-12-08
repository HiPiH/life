from django.forms import forms


def my_add_prefix(self, field_name):
    """
    Returns the field name with a prefix appended, if this Form has a
    prefix set.

    Subclasses may wish to override.
    """
    return self.prefix and ('%s_%s' % (self.prefix, field_name)) or field_name

forms.BaseForm.add_prefix = my_add_prefix



from django.forms import models

def my_construct_form(self, i, **kwargs):
    if self.is_bound and i < self.initial_form_count():
        pk_key = "%s_%s" % (self.add_prefix(i), self.model._meta.pk.name)
        pk = self.data[pk_key]
        pk_field = self.model._meta.pk
        pk = pk_field.get_db_prep_lookup('exact', pk)
        if isinstance(pk, list):
            pk = pk[0]
        kwargs['instance'] = self._existing_object(pk)
    if i < self.initial_form_count() and not kwargs.get('instance'):
        kwargs['instance'] = self.get_queryset()[i]
    return super(models.BaseModelFormSet, self)._construct_form(i, **kwargs)


models.BaseModelFormSet._construct_form = my_construct_form