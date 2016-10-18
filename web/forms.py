from django.core.exceptions import ValidationError

from django import forms


class BaseForm(forms.Form):
    """
    Base forms for getting all the forms
    """
    def validate_username(self):
        """for validating the username"""
        return False
    def validate_password(self):
        """for validating the password"""
        return False
    def validate_mobile(self,mobile):
        """for validating the mobile number"""
        if not mobile.issigit:
            return True
        if len(mobile) == 10 or len(mobile) == 11:
            return False
        else:
            return True


# class LoginUserForm(BaseForm):
#     """
#     Form for handling the incoming user form
#     """
#     username=forms.CharField(label="Username")
#     password=forms.CharField(label="Password")
#
# class RegisterUserForm(BaseForm):
#     """
#     Form for handling the incoming user registration
#     """
#     name=forms.CharField(label="Name")
#     email=forms.CharField(label="Email")
#     password=forms.CharField(label="Password")
#     mobile=forms.CharField(label="Mobile")

class CompanyRegistrationForm(forms.Form):
    """Forms for handeling the post request from the company registration form"""
    company_name = forms.CharField(label="Company Name")
    company_email = forms.CharField(label="Company Email")
    username = forms.CharField(label="Name")
    Ad_CHOICES = (
        ('blog', 'Blog'),
        ('website', 'Website'),
        ('advert', 'Advertisement'),
        ('social_media', 'Social Media'),
    )
    ad_reference = forms.ChoiceField(choices=Ad_CHOICES, required=True, label='How did you hear about us?')
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="confirm_password")

    def clean(self):
        cleaned_data = super(CompanyRegistrationForm, self).clean()
        if not cleaned_data.get('password') == cleaned_data.get('confirm_password'):
            raise ValidationError(("password and confirm password are do not match"), code="invalid")
