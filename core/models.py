from __future__ import unicode_literals

from django.db import models

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
class CompanyModal(BaseModel):
    """Company Model Profile"""
    WHERE_YOU_HEARD_ABT_US_CHOICES = (
        ('blog', 'Blog'),
        ('website', 'Website'),
        ('advert', 'Advertisement'),
        ('social_media', 'Social Media'),
    )
    company_name=models.CharField(max_length=150, blank=False)
    email=models.CharField(max_length=150,blank=False)
    phone_number=models.CharField(max_length=11,blank=True)
    where_heard_abt_us=models.CharField(max_length=1,choices=WHERE_YOU_HEARD_ABT_US_CHOICES,default='advert')














