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
            
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
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
    owner = models.ForeignKey(UserProfile) #for the companies created and added by oil_and_gas admin, default user can be admin himself.
    company_name = models.CharField(max_length=150, blank=False)
    company_email = models.CharField(max_length=150,blank=False)
    company_phone_no = models.CharField(max_length=10,blank=True)
    ad_reference = models.CharField(max_length=1,choices=WHERE_YOU_HEARD_ABT_US_CHOICES,default='advert')
    is_claimed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def request_claim(self,user):
        """method to make the claimrequest object and save it to the db"""
        from .models import ClaimRequest
        ClaimRequest.objects.create(company=self, user=user)


class ClaimCompanyRequest(BaseModel):
    """Claim requests by the users"""
    
    company =  models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default = False)

class SubscriptionPlan(BaseModel):
    SUBSCRIPTION_OPTIONS = (
        ('BSC', 'Basic'),
        ('STD', 'Standard'),
        ('PRO', 'Pro'),
        ('PRE', 'Social Media'),)
    sub_type = models.CharField(max_length=3, choices=SUBSCRIPTION_OPTIONS, primary_key=True)
    cost_per_month = models.FloatField()
    discount = models.FloatField()

class Subscription(BaseModel):
    """For subscription"""

    SUBSCRIPTION_OPTIONS = (
        ('BSC', 'Basic'),
        ('STD', 'Standard'),
        ('PRO', 'Pro'),
        ('PRE', 'Social Media'),)
    # user  = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    company = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    sub_type = models.CharField(max_length=3, default='BSC', choices=SUBSCRIPTION_OPTIONS)
    sub_begin_time =  models.DateField(default=None)
    sub_end_time = models.DateField(default=None)