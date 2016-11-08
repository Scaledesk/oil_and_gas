from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import datetime
from test_sub.settings import SERIALIZABLE_VALUE


class BaseModel(models.Model):
    """Base class for all the models"""

    def serialize_data(self):
        #get the serializable keys
        current_instance_name= self.__class__.__name__
        serializable_keys=SERIALIZABLE_VALUE.get(current_instance_name)
        serialized_data={}

        for i in serializable_keys:
            #get the value from the class
            current_value=getattr(self,i)

            #handle dates specifically
            if isinstance(current_value, datetime.datetime):
                current_value=str(current_value)

            serialized_data.update({i:current_value})

        return serialized_data

    class Meta:
        abstract=True

class UserProfile(BaseModel):
    """ Model for storing basic information about a user """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ( 'F', 'Female'),
        ('O', 'Other'))
            
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    dob = models.DateField()
    user_phone_no = models.CharField(max_length=10)


class CompanyModel(BaseModel):
    """Company Model Profile"""

    WHERE_YOU_HEARD_ABT_US_CHOICES = (
        ('B', 'Blog'),
        ('W', 'Website'),
        ('A', 'Advertisement'),
        ('S', 'Social Media'),
        ('O', 'Other'),)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=150, blank=False)
    company_email = models.CharField(max_length=150,blank=False)
    company_phone_no = models.CharField(max_length=10,blank=False)
    ad_reference = models.CharField(max_length=1,choices=WHERE_YOU_HEARD_ABT_US_CHOICES, default='A')
    is_claimed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def request_claim(self,user):
        """method to make the claimrequest object and save it to the db"""
        from .models import ClaimRequest
        ClaimRequest.objects.create(company=self, user=user)


class ClaimCompanyRequest(BaseModel):
    """Claim requests by the users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company =  models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    # user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default = False)


class SubscriptionPlan(BaseModel):
    """Model to hold the detail of plans only. It will be accesible to admin only"""
    SUBSCRIPTION_OPTIONS = (
        ('F', 'Free'),
        ('P', 'Premium'),
        ('S', 'Super Premium'),)    
    sub_type = models.CharField(max_length=4, choices=SUBSCRIPTION_OPTIONS, unique=True)
    cost_per_month = models.FloatField()
    discount = models.FloatField(default=0)

class Subscription(BaseModel):
    """Model to save the detail of company's subscription plans"""
    SUBSCRIPTION_OPTIONS = (
        ('F', 'Free'),
        ('P', 'Premium'),
        ('S', 'Super Premium'),)
    company = models.OneToOneField(CompanyModel, on_delete=models.CASCADE)
    sub_type = models.CharField(max_length=3, default='BSC', choices=SUBSCRIPTION_OPTIONS)
    sub_begin_time =  models.DateField(default=None)
    sub_end_time = models.DateField(default=None)
    is_active = models.BooleanField(default=True)


class FreeFields(BaseModel):
    company = models.OneToOneField(CompanyModel, on_delete=models.CASCADE)
    # Make Sure that if one field of address is filled than city and pin is must at form validation.
    address_line1 = models.CharField(max_length=40, default=None, blank=True)
    address_line2 = models.CharField(max_length=40, default=None, blank=True)
    address_line3 = models.CharField(max_length=40, default=None, blank=True)
    city = models.CharField(max_length=30, default=None, blank=True)
    pin = models.CharField(max_length=6, default=None, blank=True)
    website = models.CharField(max_length=200, default=None, blank=True)
    year_founded = models.CharField(max_length=200, default=None, blank=True)
    about = models.CharField(max_length=100, default=None, blank=True)
    #Product and Services to be added but is not defined.


#### PREMIUM SUBSCRIPTION FIELDS #####
class PremiumFields(BaseModel):
    """Model to save premium fields"""
    company = models.OneToOneField(CompanyModel, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='comapany_logo/', default=None, blank=True) 
    registration_no = models.CharField(max_length=12, default=None, blank=True) #     Company DUNS/Registration Confirmation/ Business Number
    bio = models.CharField(max_length=1000, default=None, blank=True)
    no_of_emp = models.IntegerField(default=None, blank=True)
    sale_volume = models.CharField(max_length=30, default=None, blank=True)


class Gallery(BaseModel): #10
    """Model to save gallery images for premium subscription. Max limit 10"""
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='company_gallery/')

class Brochure(BaseModel):
    """Model to save company brochure. Max Limit = 2"""
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE) 
    brochure = models.FileField(upload_to='company_brouchure/')

class VideoLink(BaseModel):
    """Model to save video links for premium subscription. Max limit 2"""
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE) 
    video_link = models.CharField(max_length=200)

class KeyClient(BaseModel): #15
    """Model to sace list of key clients for premium subscription. Max limit 15""" 
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    key_client = models.CharField(max_length=150)

class KeyAlliance(BaseModel):
    """Model to save list of key alliances for premium subscription to be selected from company data in database. Max Limit 10"""
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, related_name='company')
    key_alliance = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, related_name='alliance')

class Location(BaseModel):
    """Model to save list of locations for premium subscription. Max limit = Not Given"""  
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    location_type = models.CharField(max_length=30, default=None, blank=True)
    location = models.CharField(max_length=200, default=None, blank=True)

class Certification(BaseModel):
    """Model to save list certification/subscription for premium subscription. Max limit 5""" 
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    certi_name = models.CharField(max_length=100)
    certi_description = models.CharField(max_length=200, default=None, blank=True)
    certi_doc = models.FileField(upload_to='certification/', default=None , blank=True)

class SocialLinks(BaseModel):
    """Model to save social links for premium subscription."""  
    company = models.OneToOneField(CompanyModel, on_delete=models.CASCADE)

    facebook = models.CharField(max_length=200, default=None, blank=True)
    twitter = models.CharField(max_length=200, default=None, blank=True)
    linkedin = models.CharField(max_length=200, default=None, blank=True)

#### PREMIUM SUBSCRIPTION FIELDS END #####