from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import datetime
from test_sub.settings import SERIALIZABLE_VALUE
import pycountry # for help :- https://pypi.python.org/pypi/pycountry

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

    # def __unicode__(self):
    #     return self.user

class SubscriptionPlan(BaseModel):
    """Model to hold the detail of plans only. It will be accesible to admin only"""
    SUBSCRIPTION_OPTIONS = (
        ('F', 'Free'),
        ('P', 'Premium'),
        ('S', 'Super Premium'),)    
    sub_type = models.CharField(max_length=4, choices=SUBSCRIPTION_OPTIONS, unique=True)
    cost_per_month = models.FloatField()
    discount = models.FloatField(default=0)
    def __unicode__(self):
        return self.sub_type


class CompanyModel(BaseModel):
    """Company Model Profile"""

    WHERE_YOU_HEARD_ABT_US_CHOICES = (
        ('B', 'Blog'),
        ('W', 'Website'),
        ('A', 'Advertisement'),
        ('S', 'Social Media'),
        ('O', 'Other'),)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=150, blank=False, unique=True)
    company_email = models.CharField(max_length=150,blank=False)
    company_phone_no = models.CharField(max_length=10,blank=False)
    ad_reference = models.CharField(max_length=1,choices=WHERE_YOU_HEARD_ABT_US_CHOICES, default='A')
    is_claimed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False) 
    sub_plan = models.ForeignKey(SubscriptionPlan)
    sub_begin_date =  models.DateField(default=datetime.date.today)
    sub_end_date = models.DateField(default=datetime.date.today)
    is_sub_active = models.BooleanField(default=False)
    def request_claim(self,user):
        """method to make the claimrequest object and save it to the db"""
        from .models import ClaimRequest
        ClaimRequest.objects.create(company=self, user=user)


class ClaimCompanyRequest(BaseModel):
    """Claim requests by the users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company =  models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default = False)


# class Subscription(BaseModel):
#     """Model to save the detail of company's subscription plans"""
#     SUBSCRIPTION_OPTIONS = (
#         ('F', 'Free'),
#         ('P', 'Premium'),
#         ('S', 'Super Premium'),)
#     company = models.OneToOneField(CompanyModel, on_delete=models.CASCADE)
#     sub_type = models.CharField(max_length=3, default='BSC', choices=SUBSCRIPTION_OPTIONS)
#     sub_begin_time =  models.DateField(default=None)
#     sub_end_time = models.DateField(default=None)
#     is_active = models.BooleanField(default=True)


class FreeField(BaseModel):
    company = models.OneToOneField(CompanyModel, on_delete=models.CASCADE)
    # Make Sure that if one field of address is filled than city and pin is must at form validation.
    address = models.CharField(max_length=120, default=None, blank=True)
    city = models.CharField(max_length=30, default=None, blank=True)
    pin = models.CharField(max_length=6, default=None, blank=True)
    website = models.CharField(max_length=200, default=None, blank=True)
    year_founded = models.CharField(max_length=200, default=None, blank=True)
    about = models.CharField(max_length=100, default=None, blank=True)
    #Product and Services to be added but is not defined.


#### PREMIUM SUBSCRIPTION FIELDS #####
class BasicPremiumField(BaseModel):
    """Model to save premium fields"""
    company = models.OneToOneField(CompanyModel, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='company_logo/', default=None, blank=True) 
    registration_no = models.CharField(max_length=12, default=None, blank=True)
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
    certi_doc = models.FileField(upload_to='company_certification/', default=None , blank=True)

class SocialLink(BaseModel):
    """Model to save social links for premium subscription."""  
    company = models.OneToOneField(CompanyModel, on_delete=models.CASCADE)

    facebook = models.CharField(max_length=200, default=None, blank=True)
    twitter = models.CharField(max_length=200, default=None, blank=True)
    linkedin = models.CharField(max_length=200, default=None, blank=True)

#### PREMIUM SUBSCRIPTION FIELDS END #####


######################### SUPER PREMIUM FIELDS ###############################

class Publication(BaseModel):
    PUB_TYPE=(
        ('A', 'Article'),
        ('P', 'Patent'),
        )
    company = models.ForeignKey(CompanyModel)
    pub_type = models.CharField(max_length=1, choices=PUB_TYPE)
    pub_content = models.CharField(max_length=2000)

# class Country(BaseModel):
#     # A country field for Django models that provides all ISO 3166-1 countries as choices.
#     company = models.ForeignKey(CompanyModel)
#     country = 

########################### SUPER PREMIUM FIELDS ################################

class Requirement(BaseModel):
    company = models.ForeignKey(CompanyModel)
    req_heading = models.CharField(max_length=100)
    req_detail = models.CharField(max_length=2000)

class ReqSubscriptionPlan(BaseModel):
    plan_name = models.FloatField(unique=True)

    free_price = models.FloatField()
    premium_price = models.FloatField()
    super_premium_price = models.FloatField()

    free_discount = models.FloatField()
    premium_discount = models.FloatField()
    super_premium_discount = models.FloatField()

class ReqViewSubscription(object):
    """docstring for ReqViewSubscription"""
    company = models.ForeignKey(CompanyModel, unique=True)
    sub_plan = models.ForeignKey(SubscriptionPlan)    
    is_subscribed = models.BooleanField(default=False)
    sub_begin_date =  models.DateField(default=datetime.date.today)
    sub_end_date = models.DateField(default=datetime.date.today)
    is_sub_active = models.BooleanField(default=False)