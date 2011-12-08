from django                         import forms
from django.utils.translation       import ugettext as _
from django.contrib.auth.models     import User
from django.forms.widgets           import PasswordInput
from models                         import UsersAvatars
from apps.utils.forms import SelectGraphDate, CustomForm

# ФОРМА РЕГИСТРАЦИИ
class FormUserReg(forms.ModelForm):
    username = forms.RegexField(label=_('Nic'), regex=u'^([a-zA-Z0-9-_]+)$', required = True, help_text=_("Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters"))
    last_name = forms.CharField(label=_('last name'), required = True)
    password1 = forms.CharField(label=_('Your password'), required = True, widget=PasswordInput)
    password2 = forms.CharField(label=_('Your password repeat'), required = True, widget=PasswordInput)
    birthday = forms.DateField(label=_('Birthday'), widget=SelectGraphDate({'showsTime':"false",}), required = False)
    email = forms.EmailField(label=_('Email'), required = False)

    
    def clean_first_name(self):
        if self.cleaned_data['first_name'] == "":
            raise forms.ValidationError(_('Please type your first name'))
        return self.cleaned_data['first_name']
    
    
    def clean_email(self):
        if self.cleaned_data['email'] == "":
            raise forms.ValidationError(_(u'Неверный формат электронной почты'))
        if 0 < User.objects.filter(email=self.cleaned_data['email']).count():
            raise forms.ValidationError(_('This email is already exists.'))
        return self.cleaned_data['email']
    
    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','sex','birthday','address','metro',)

        
# ФОРМА ЗАБЫВЧИВОСТИ ПАРОЛЯ
class FormUserForgot(forms.Form):
    email = forms.EmailField(label = _('Your E-mail'), min_length = 1, required = True)
    
    def clean_email(self):
        if not User.objects.filter(email=self.cleaned_data['email']).count():
            raise forms.ValidationError(_('This email is not register'))
        return self.cleaned_data['email']


# ФОРМА РЕДАКТИРОВАНИЯ ПОЛЬЗОВАТЕЛЯ
class FormUserEdit(forms.ModelForm):
    birthday = forms.DateField(widget=SelectGraphDate({'showsTime':"false",}), required = True)

    def clean_first_name(self):
        if self.cleaned_data['first_name'] == "":
            raise forms.ValidationError('Please type your first name')
        return self.cleaned_data['first_name']
        
    def clean_last_name(self):
        if self.cleaned_data['last_name'] == "":
            raise forms.ValidationError('Please type your last name')
        return self.cleaned_data['last_name']
        
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email', 'sex','birthday','metro','address')
        
        
# ФОРМА СМЕНЫ ПАРОЛЯ (ПОКА НЕ ИСПОЛЬЗУЕТСЯ - НАДО ОБСУЖДАТЬ)
class FormUserChangePassword(forms.Form):
    passwordnew1 = forms.CharField(label=_('Your new password'), required = True, widget=PasswordInput)
    passwordnew2 = forms.CharField(label=_('Your new password repeat'), required = True, widget=PasswordInput)
    
# ФОРМА ВАЛИДАЦИИ
class FormValidation(forms.Form):
    login = forms.CharField(label=_('Your login'), required = True)
    valid_code = forms.CharField(label=_('Your validation code'), required = True)
    
# ФОРМА ДЛЯ ЗАГРУЗКИ СВОЕЙ АВАТАРКИ
class FormUploadAvatars(forms.ModelForm):
    class Meta():
        model = UsersAvatars
        fields = ('title', 'image_orig',)