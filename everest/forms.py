from django import forms
from django.contrib.auth.models import User
from everest.models import UserProfile
from models import *

class AudioForm(forms.Form):
    audio = forms.FileField()
    language = forms.ChoiceField(choices=('english','nepali'))

class NepaliTranslation(forms.Form):
    translation = forms.CharField(max_length = 400)



#TODO: Use RegexFields for username, first_name, last_name
#TODO: Use EmailField for email

class RegisterForm(forms.Form):
    username   = forms.CharField(max_length = 20, label='Username')
    first_name = forms.CharField(max_length = 120, label='First name')
    last_name  = forms.CharField(max_length = 120, label='Last name')
    email      = forms.CharField(max_length = 30, label='Email')
    password1  = forms.CharField(max_length = 25,
                                 label='Password',
                                 widget = forms.PasswordInput())
    password2  = forms.CharField(max_length = 25,
                                 label='Confirm password',
                                 widget = forms.PasswordInput())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegisterForm, self).clean()
        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        # We must return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        if " " in username:
            raise forms.ValidationError("Username must be one word.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username


#TODO use include instead of exclude
class CreateForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = (
            'created_by',
            'creation_time',
            'updated_by',
            'update_time',
        )


class EditForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = (
            'created_by',
            'creation_time',
            'updated_by',
        )
        widgets = {
            'update_time': forms.HiddenInput,
        }

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length = 20)
    last_name  = forms.CharField(max_length = 20)
    bio = forms.CharField(max_length = 430, required=False)

class AddSentence(forms.Form):
    sentence = forms.CharField(max_length = 200)

class AddLesson(forms.Form):
    title = forms.CharField(max_length = 50)
