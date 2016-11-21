from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import datetime
from test_sub.settings import SERIALIZABLE_VALUE
import pycountry # for help :- https://pypi.python.org/pypi/pycountry
from pprint import pprint

from core.model_validations import *

class BaseModel(models.Model):
    """Base class for all the models"""

    def serialize_data(self):
        #get the serializable keys
        current_instance_name= self.__class__.__name__
        serializable_keys=SERIALIZABLE_VALUE.get(current_instance_name)
        serialized_data={}

        for i in serializable_keys:

            #get the valjue from the class
            current_value=getattr(self,i)

            #handle dates specifically
            if isinstance(current_value, datetime.datetime):
                current_value=str(current_value)
            serialized_data[i] = current_value
            # serialized_data.update({i:current_value}) .update is very slow to execute
        return serialized_data
    class Meta:
        abstract=True


class UserProfile(BaseModel):
    """ Model for storing basic information about a user """

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField()
    user_phone_no = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    def __unicode__(self):
        return self.user.email

    # def save(self, *args, **kwargs):
    #     pprint(self.all())
    #     return False



class SubscriptionPlan(BaseModel):
    """Model to hold the detail of plans only. It will be accesible to admin only"""

    SUBSCRIPTION_OPTIONS = (
        ('F', 'Free'),
        ('P', 'Premium'),
        ('S', 'Super Premium'),)
    sub_type = models.CharField(max_length=1, choices=SUBSCRIPTION_OPTIONS, unique=True)
    cost_per_month = models.FloatField()
    discount = models.FloatField(default=0)

    class Meta:
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'

    def __unicode__(self):
        sub_type = self.sub_type
        if sub_type == 'S':
            return "Super Premium Subscription"
        elif sub_type == 'P':
            return "Premium Subscription"
        else:
            return "Free Subscription"

class ReqSubscriptionPlan(BaseModel):
    """ Subscription Plan for Viewing Requirement"""

    plan_name = models.CharField(unique=True, max_length=30)

    free_price = models.FloatField()
    premium_price = models.FloatField()
    super_premium_price = models.FloatField()

    free_discount = models.FloatField()
    premium_discount = models.FloatField()
    super_premium_discount = models.FloatField()

    class Meta:
        verbose_name = 'Request Subscription Plans'
        verbose_name_plural = 'Request Subscription Plans'

    # def save(self, *args, **kwargs):
    #     """ Override Person's save """
    #     self.full_clean(exclude=None)
    #     super(ReqSubscriptionPlan, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.plan_name


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

    #Company Subscription
    sub_plan = models.ForeignKey(SubscriptionPlan)
    sub_begin_date =  models.DateField(default=datetime.date.today)
    sub_end_date = models.DateField(default=datetime.date.today)
    is_sub_active = models.BooleanField(default=False)

    #Requirement subscription
    req_sub_begin_date =  models.DateField(default=datetime.date.today)
    req_sub_end_date = models.DateField(default=datetime.date.today)
    is_req_sub_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        # unique_together = (("driver", "restaurant"),)

    def __unicode__(self):
        return self.company_name

class ClaimCompanyRequest(BaseModel):
    """Claim requests by the users"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company =  models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default = False)

    class Meta:
        verbose_name = 'Company Claim Requiest'
        verbose_name_plural = 'Company Claim Requests'

    def __unicode__(self):
        return (self.user.email + " | " + self.company.company_name)

class FreeField(BaseModel):
    """ Model to save the free fields of the companies """

    company = models.OneToOneField(CompanyModel, on_delete=models.CASCADE)
    # Make Sure that if one field of address is filled than city and pin is must at form validation.
    address = models.CharField(max_length=120, default=None, blank=True)
    city = models.CharField(max_length=30, default=None, blank=True)
    pin = models.CharField(max_length=6, default=None, blank=True)
    website = models.CharField(max_length=200, default=None, blank=True)
    year_founded = models.CharField(max_length=200, default=None, blank=True)
    about = models.CharField(max_length=100, default=None, blank=True)
    #Product and Services to be added but is not defined.

    class Meta:
        verbose_name = 'Free Field'
        verbose_name_plural = 'Free Fields'

    def save(self, *args, **kwargs):
        """ Override FreeField's save """
        # if validate_free_fields(self):
        #     pprint(self)
        #     return True
        # return True
        self.full_clean(exclude=None)
        super(ReqSubscriptionPlan, self).save(*args, **kwargs)

    def __unicode__(self):
        return (self.company.company_name)

#### PREMIUM SUBSCRIPTION FIELDS #####
class BasicPremiumField(BaseModel):
    """Model to save premium fields"""

    company = models.OneToOneField(CompanyModel, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='company_logo/', default=None, blank=True)
    registration_no = models.CharField(max_length=12, default=None, blank=True)
    no_of_emp = models.PositiveIntegerField(default=None, blank=True)
    sale_volume = models.CharField(max_length=30, default=None, blank=True)

    class Meta:
        verbose_name = 'Basic Premium Field'
        verbose_name_plural = 'Basic Premium Fields'

    def __unicode__(self):
        return (self.company.company_name)


class Gallery(BaseModel): #10
    """Model to save gallery images for premium subscription. Max limit 10"""

    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='company_gallery/')

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'
    def __unicode__(self):
        return (self.company.company_name)

class Brochure(BaseModel):
    """Model to save company brochure. Max Limit = 2"""

    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    brochure = models.FileField(upload_to='company_brouchure/')

    class Meta:
        verbose_name = 'Brochure'
        verbose_name_plural = 'Brochures'
    def __unicode__(self):
        return (self.company.company_name)

class VideoLink(BaseModel):
    """Model to save video links for premium subscription. Max limit 2"""

    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    video_link = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Video Link'
        verbose_name_plural = 'Video Links'
    def __unicode__(self):
        return (self.company.company_name)

class KeyClient(BaseModel): #15
    """Model to sace list of key clients for premium subscription. Max limit 15"""

    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    key_client = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'Key Client'
        verbose_name_plural = 'Key Clients'
    def __unicode__(self):
        return (self.company.company_name)

class KeyAlliance(BaseModel):
    """Model to save list of key alliances for premium subscription to be selected from company data in database. Max Limit 10"""

    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, related_name='company')
    key_alliance = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, related_name='alliance')
    class Meta:
        verbose_name = 'Key Alliance'
        verbose_name_plural = 'Key Alliances'
    def __unicode__(self):
        return (self.company.company_name)

class Location(BaseModel):
    """Model to save list of locations for premium subscription. Max limit = Not Given"""

    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    location_type = models.CharField(max_length=30, default=None, blank=True)
    location = models.CharField(max_length=200, default=None, blank=True)

    class meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
    def __unicode__(self):
        return (self.company.company_name)

class Certification(BaseModel):
    """Model to save list certification/subscription for premium subscription. Max limit 5"""

    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    certi_name = models.CharField(max_length=100)
    certi_description = models.CharField(max_length=200, default=None, blank=True)
    certi_doc = models.FileField(upload_to='company_certification/', default=None , blank=True)

    class meta:
        verbose_name = 'Certification'
        verbose_name_plural = 'Certifications'
    def __unicode__(self):
        return (self.company.company_name)

class SocialLink(BaseModel):
    """Model to save social links for premium subscription."""

    company = models.OneToOneField(CompanyModel, on_delete=models.CASCADE)
    facebook = models.CharField(max_length=200, default=None, blank=True)
    twitter = models.CharField(max_length=200, default=None, blank=True)
    linkedin = models.CharField(max_length=200, default=None, blank=True)

    class meta:
        verbose_name = 'Social Link'
        verbose_name_plural = 'Social Links'
    def __unicode__(self):
        return (self.company.company_name)

#### PREMIUM SUBSCRIPTION FIELDS END #####


######################### SUPER PREMIUM FIELDS ###############################

class Publication(BaseModel):
    """ Model to save the published articles """

    PUB_TYPE=(
        ('A', 'Article'),
        ('P', 'Patent'),
        )
    company = models.ForeignKey(CompanyModel)
    pub_type = models.CharField(max_length=1, choices=PUB_TYPE)
    pub_content = models.CharField(max_length=2000)

    class meta:
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'
    def __unicode__(self):
        return (self.company.company_name)

########################### SUPER PREMIUM FIELDS ################################

class Requirement(BaseModel):
    """ models to save the Requirements posted by the companies """

    company = models.ForeignKey(CompanyModel)
    req_heading = models.CharField(max_length=100)
    req_detail = models.CharField(max_length=2000)

    class meta:
        verbose_name = 'Requirement'
        verbose_name_plural = 'Requirements'
    def __unicode__(self):
        return (self.company.company_name)
