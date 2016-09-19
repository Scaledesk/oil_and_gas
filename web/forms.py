from django.forms import forms


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
class LoginUserForm(BaseForm):
    """
    Form for handling the incoming user form
    """
    username=forms.CharField(label="Username")
    password=forms.CharField(label="Password")

class RegisterUserForm(BaseForm):
    """
    Form for handling the incoming user registration
    """
    name=forms.CharField(label="Name")
    email=forms.CharField(label="Email")
    password=forms.CharField(label="Password")
    mobile=forms.charField(label="Mobile")
