from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from core.models import CompanyModel, UserProfile
from pprint import pprint

class BaseForm(forms.Form):
    """
    Base form for all the forms in EMS
    """
    def is_phone_no_invalid(self, phone_number):
        """ Util function for validating phone number """
        return ((not str(phone_number).isdigit()) or (len(phone_number)!=10))

    def is_name_invalid(self,name):
        """
        This function return true if name contains any digit. However it fails to address the special characters.
        """
        return self.has_numbers(name)

    def user_email_already_exists(self, email):
        """
        This function return true if the user email provided already exists in database.
        """
        return User.objects.filter(email=email).exists()

    def company_email_already_exists(self, email):
        """
        This function return true if the company email provided already exists in database.
        """
        return CompanyModel.objects.filter(company_email=email).exists()

    def user_phone_no_already_exists(self, phone_no):
        """
        This function return true if the Phone Number by user provided already exists in user's database.
        """
        return UserProfile.objects.filter(phone_no=phone_no).exists()

    def company_phone_no_already_exists(self, phone_no):
        """
        This function return true if the Phone Number by user provided already exists in user's database.
        """
        return CompanyModel.objects.filter(company_phone_no=phone_no).exists()

    def has_numbers(self,inputString):
        """This function to to check if """
        return any(char.isdigit() for char in inputString)


class RegisterUserAndCompany(BaseForm):
    """
    Form for user registration/creating account
    """


    # USER #
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'))


    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length= 30)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    dob = forms.DateField()
    user_email = forms.EmailField()
    user_phone_no = forms.CharField(max_length=10)
    password = forms.CharField(max_length = 50)
    confirm_password = forms.CharField(max_length=50)


    # COMPANY #
    WHERE_YOU_HEARD_ABT_US_CHOICES = (
        ('B', 'Blog'),
        ('W', 'Website'),
        ('A', 'Advertisement'),
        ('S', 'Social Media'),
        ('O', 'Other'),)
    company_name = forms.CharField(max_length=150)
    company_email = forms.CharField(max_length=150)
    company_phone_no = forms.CharField(max_length=10)
    ad_reference = forms.ChoiceField(choices=WHERE_YOU_HEARD_ABT_US_CHOICES)


    def clean(self, *args, **kwargs):
        """Clean function"""

        cleaned_data = super(RegisterUserAndCompany, self).clean()

        # USER #
        if self.is_name_invalid(cleaned_data.get('first_name')):
            raise forms.ValidationError('First Name you have entered is invalid')

        if self.is_name_invalid(cleaned_data.get('last_name')):
            raise forms.ValidationError('Last Name you have entered is invalid')

        if self.user_email_already_exists(cleaned_data.get('user_email')):
            raise forms.ValidationError('User Email Id provided already exists in database. Use different Email Id')

        if self.is_phone_no_invalid(cleaned_data['user_phone_no']):
            raise forms.ValidationError('The user phone number provided is invalid')

        if self.user_email_already_exists(cleaned_data['user_phone_no']):
            raise forms.ValidationError('The user phone number provided already exist in the database')

        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError('Passwords cannot be different')

        if len(cleaned_data.get('password')) < 8:
            raise forms.ValidationError('Password must contain at least 8 characters')

        # COMPANY #
        if self.company_email_already_exists(cleaned_data['company_email']):
            raise forms.ValidationError('Company Email Id provided already exists in database. Use different Email Id')
        

        if self.is_phone_no_invalid(cleaned_data['company_phone_no']):
            raise forms.ValidationError('The Company phone number provided is invalid')
        
        if self.company_phone_no_already_exists(cleaned_data['company_phone_no']):
            raise forms.ValidationError('The Company phone number provided already exist in database')

        else:
            return cleaned_data

class AddCompanyForm(BaseForm):


    def clean(self, *args, **kwargs):
        """
        Clean function
        """
        cleaned_data = super(AddCompanyForm, self).clean()

        pprint(cleaned_data)








































class RegisterUserForm(BaseForm):
    """
    Form for user registration/creating account
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'))


    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length= 30)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    user_email = forms.EmailField()
    phone_number = forms.CharField(max_length=10)
    password = forms.CharField(max_length = 50)
    confirm_password = forms.CharField(max_length=50)


    def clean(self, *args, **kwargs):
        """Clean function"""

        cleaned_data = super(RegistrationForm, self).clean()

        if self.is_name_invalid(cleaned_data.get('first_name')):
            raise forms.ValidationError('First Name you have entered is invalid')

        if self.is_name_invalid(cleaned_data.get('last_name')):
            raise forms.ValidationError('Last Name you have entered is invalid')

        if self.user_email_already_exists(cleaned_data.get('email')):
            raise forms.ValidationError('Email Id provided already exists in database. Use different Email Id')

        if self.is_phone_no_invalid(cleaned_data['user_phone_no']):
            raise forms.ValidationError('The user phone number provided is invalid')

        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError('Passwords cannot be different')

        if len(cleaned_data.get('password')) < 8:
            raise forms.ValidationError('Password must contain at least 8 characters')
        else:
            return cleaned_data

class AddCompanyForm(BaseForm):
    WHERE_YOU_HEARD_ABT_US_CHOICES = (
        ('B', 'Blog'),
        ('W', 'Website'),
        ('A', 'Advertisement'),
        ('S', 'Social Media'),
        ('O', 'Other'),
    )

    company_name = forms.CharField(max_length=150)
    company_email = forms.CharField(max_length=150)
    company_phone_no = forms.CharField(max_length=10)
    where_heard_abt_us = forms.ChoiceField(choices=WHERE_YOU_HEARD_ABT_US_CHOICES)

    def clean(self, *args, **kwargs):
        """
        Clean function
        """
        cleaned_data = super(AddCompanyForm, self).clean()

        pprint(cleaned_data)

        if self.company_email_already_exists(cleaned_data['company_email']):
            raise forms.ValidationError('Email Id provided already exists in database. Use different Email Id')
        if self.is_phone_no_invalid(cleaned_data['company_phone_no']):
            raise forms.ValidationError('The Company phone number provided is invalid')
        if self.company_phone_no_already_exists(cleaned_data['company_phone_no']):
            raise forms.ValidationError('The Company phone number provided already exist in database')
        else:
            return cleaned_data








































# class BaseForm(forms.Form):
#     """
#     Base forms for getting all the forms
#     """
#     def validate_username(self):
#         """for validating the username"""
#         return False
#     def validate_password(self):
#         """for validating the password"""
#         return False
#     def validate_mobile(self,mobile):
#         """for validating the mobile number"""
#         if not mobile.issigit:
#             return True
#         if len(mobile) == 10 or len(mobile) == 11:
#             return False
#         else:
#             return True



# class LoginUserForm(BaseForm):
#     """
#     Form for handling the incoming user form
#     """
#     username=forms.CharField(label="Username")
#     password=forms.CharField(label="Password")

# class RegisterUserForm(BaseForm):
#     """
#     Form for handling the incoming user registration
#     """
#     name=forms.CharField(label="Name")
#     email=forms.CharField(label="Email")
#     password=forms.CharField(label="Password")
#     mobile=forms.charField(label="Mobile")
