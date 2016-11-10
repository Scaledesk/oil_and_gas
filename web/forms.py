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


class CreateUserAndCompanyForm(BaseForm):
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

        cleaned_data = super(CreateUserAndCompanyForm, self).clean()

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


class CreateUserForm(BaseForm):
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
    dob = forms.DateField()
    user_email = forms.EmailField()
    user_phone_no = forms.CharField(max_length=10)
    password = forms.CharField(max_length = 50)
    confirm_password = forms.CharField(max_length=50)


    def clean(self, *args, **kwargs):
        """Clean function"""

        cleaned_data = super(CreateUserForm, self).clean()

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

class CreateCompanyForm(BaseForm):
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
        cleaned_data = super(CreateCompanyForm, self).clean()

        pprint(cleaned_data)

        if self.company_email_already_exists(cleaned_data['company_email']):
            raise forms.ValidationError('Email Id provided already exists in database. Use different Email Id')
        if self.is_phone_no_invalid(cleaned_data['company_phone_no']):
            raise forms.ValidationError('The Company phone number provided is invalid')
        if self.company_phone_no_already_exists(cleaned_data['company_phone_no']):
            raise forms.ValidationError('The Company phone number provided already exist in database')
        else:
            return cleaned_data

#### Free Subscription Form ####

class FreeFieldForm(BaseForm):
    address = forms.CharField(max_length=120, label="Address Line 1:", required=False)
    city = forms.CharField(max_length=30, label="City:", required=False)
    pin = forms.CharField(max_length=6, label="pin", required=False)
    website = forms.CharField(max_length=200, label="Company website:", required=False)
    year_founded = forms.CharField(max_length=4, label="Year Founded:", required=False)
    about = forms.CharField(max_length=100, label="About Company:", required=False)

#### Free Subscription Form ####



#### Premium Subscription Form ####

class BasicPremiumFieldForm(BaseForm):
    logo = forms.ImageField(required=False, label="Company logo:")
    registration_no = forms.CharField(max_length=12, label="Company registration No:", required=False)
    bio = forms.CharField(max_length=1000, label="Company bio:", required=False)
    no_of_emp = forms.IntegerField(required=False, label="No of employee:")
    sale_volume = forms.CharField(max_length=30, label="Sale volume:", required=False)

class GalleryForm(BaseForm):
    image = forms.ImageField(required=False, label="Image:")

class BrochureForm(BaseForm):
    brochure = forms.FileField(required=False, label="Company Brochure:")

class VideoLinkForm(BaseForm):
    video_link = forms.URLField(label="video_link:", required=False)

class KeyClient(BaseForm):
    key_client = forms.CharField(max_length=150, label="Key Client:")

# class KeyAlliance(BaseModel):


class LocationForm(BaseForm):
    location_type = forms.CharField(max_length=30, label="Location Type:", required=False)
    location = forms.CharField(max_length=200, label="Location:", required=False)

class CertificationForm(BaseForm):
    certi_name = forms.CharField(max_length=100, label="Certification name:", required=False)
    certi_description = forms.CharField(max_length=200, label="Certificatio description:", required=False)
    certi_doc = forms.FileField(required=False, label="Certification Document")

class SocialLinkForm(BaseForm):
    facebook = forms.URLField(required=False, label="Facebook Link:")
    twitter = forms.URLField(required=False, label="Twitter Link:")
    linkedin = forms.URLField(required=False, label="Linkedin:")



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
