from django import forms
from .models import Account

class CreateUserForm(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class LoginUserForm(forms.Form):
    name = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())

class CreateProfileModelForm(forms.ModelForm):
    class Meta:
        fields = ["name", "age", "zodiac", "about_bad_habits", "image"]
        model = Account

class EditProfileForm(forms.Form):
    name = forms.CharField(max_length=20)
    age = forms.IntegerField()
    zodiac = forms.CharField(max_length=10)
    about_bad_habits = forms.CharField(widget=forms.Textarea())

class ChatForm(forms.Form):
    chat_text = forms.CharField(widget= forms.Textarea()) 
    # receiver = forms.CharField(max_length=20, empty=True)


