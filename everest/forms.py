from django import forms

from models import *

USER_TYPE_CHOICES = (('E', 'ESL Teacher'), ('T', 'Bhutanese Translator'), ('O', 'Other'))


class AudioForm(forms.Form):
    audio = forms.FileField()
    language = forms.ChoiceField(choices=(('english', 'english'), ('nepali', 'nepali')))


class NepaliTranslation(forms.Form):
    translation = forms.CharField(max_length=400)


class AddSentence(forms.Form):
    sentence = forms.CharField(max_length=200)


class QueryForm(forms.Form):
    query = forms.CharField(max_length=200)


class AddLesson(forms.Form):
    title = forms.CharField(max_length=50)


"""
These are forms used to edit the users profile
"""


class ChangePersonalForm(forms.Form):
    first_name = forms.RegexField(regex=r'^[a-zA-Z_]+$', max_length=20, label='First name')
    last_name = forms.RegexField(regex=r'^[a-zA-Z_]+$', max_length=40, label='Last name')
    email = forms.EmailField(max_length=30, label='Email')
    bio = forms.CharField(max_length=430, required=False)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)


class ChangePasswordForm(forms.Form):
    current = forms.CharField(max_length=25)
    password1 = forms.CharField(max_length=25)
    password2 = forms.CharField(max_length=25)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        # We must return the cleaned data we got from our parent.
        return cleaned_data


class ChangePictureForm(forms.Form):
    image = forms.ImageField()

"""
This is the registration form
"""


class ResetForm(forms.Form):
    username = forms.RegexField(regex=r'^[a-zA-Z0-9_]+$', max_length=20, label='Username')


class RegisterForm(forms.Form):
    username = forms.RegexField(regex=r'^[a-zA-Z0-9_]+$', max_length=20, label='Username')
    first_name = forms.RegexField(regex=r'^[a-zA-Z_]+$', max_length=20, label='First name')
    last_name = forms.RegexField(regex=r'^[a-zA-Z_]+$', max_length=40, label='Last name')
    email = forms.EmailField(max_length=30, label='Email')
    password1 = forms.CharField(max_length=25)
    password2 = forms.CharField(max_length=25)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username
