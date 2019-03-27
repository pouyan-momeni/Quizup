__author__ = 'sara'

# Import the forms library to create forms
from django import forms
#from captcha.fields import ReCaptchaField
from registration.forms import RegistrationForm

class RegistrationForm2(RegistrationForm):
  username = forms.CharField()
  email = forms.EmailField()
  password1 = forms.CharField(widget=forms.PasswordInput) # Set the widget to
                                                         # PasswordInput
  password2 = forms.CharField(widget=forms.PasswordInput,
                              label="Confirm password") # Set the widget to
                                                        # PasswordInput and
                                                        # set an appropriate
                                                        # label
#  captcha = ReCaptchaField(attrs={'theme' : 'clean'})
  # clean_<fieldname> method in a form class is used to do custom validation
  # for the field.
  # We are doing a custom validation for the 'password2' field and raising
  # a validation error if the password and its confirmation do not match
  def __init__(self, *args, **kwargs):
    super(RegistrationForm,self).__init__(*args, **kwargs)

  def clean_password2(self):
    password1 = self.cleaned_data['password1'] # cleaned_data dictionary has the
                                             # the valid fields
    password2 = self.cleaned_data['password2']
    if password1 != password2:
      raise forms.ValidationError("Passwords do not match.")
    return password2
