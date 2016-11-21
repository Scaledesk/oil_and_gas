from pprint import pprint
from core.models import *



#### Methods to validate model objects before saving #####
def is_phone_no_invalid(self, phone_number):
    """ Returns True if phone no provided is invalid """
    return ((not str(phone_number).isdigit()) or (len(phone_number)!=10))

def is_pin_invalid(self, pin):
    """ Returns True if pin provided is invalid """
    return ((not str(pin).isdigit()) or (len(pin)!=6))

def is_year_invalid(self, year):
    """ Returns True if year provided is invalid """
    return ((not str(year).isdigit()) or (len(year)!=4))

def is_name_invalid(self,name):
    """Returns True if name provided is Invalid"""
    return self.has_numbers(name)

def user_email_already_exists(self, email):
    """Returns True if user-email provided already exists in database."""
    return User.objects.filter(email=email).exists()

def company_email_already_exists(self, email):
    """Returns True if company email provided already exists in database"""
    return CompanyModel.objects.filter(company_email=email).exists()

def user_phone_no_already_exists(self, phone_no):
    """Returns True if Phone Number provided already exists in user database."""
    return UserProfile.objects.filter(phone_no=phone_no).exists()

def company_phone_no_already_exists(self, phone_no):
    """Returns True if Phone Number provided already exists in company database"""
    return CompanyModel.objects.filter(company_phone_no=phone_no).exists()

def has_numbers(self,inputString):
    """Returns True if string has numbers"""
    return any(char.isdigit() for char in inputString)
#### Methods to validate model objects before saving End #####

def validate_user_profile(self):
    """Returns True if the UserProfile object has valid data"""
    if is_phone_no_invalid(self.user_phone_no):
        return False
    else:
        return True

def validate_subscription_plan(self):
    """Returns True if SubscriptionPlan object has valid data"""
    return True

def validate_req_subscription_plan(self):
    """Returns True if ReqSubscriptionPlan object has valid data"""
    return True

def validate_company_model(self):
    """Returns True if CompanyModel object has valid data"""
    if is_phone_no_invalid(self.company_phone_no):
        return False
    else:
        return True

def validate_claim_company_requests(self):
    """Returns True if the ClaimCompanyRequest object has valid data"""
    if ClaimCompanyRequest.object.filter(user=self.user, company=self.company).exists():
        return False
    else:
        return True

def validate_free_fields(self):
    """Returns True if FreeField object has valid data"""
    if is_pin_invalid(self.pin):
        return False
    elif is_year_invalid(self.year_founded):
        return False
    else:
        return True

def validate_basic_premium_fields(self):
    """Returns True if BasicPremiumField objects has valid data"""
    return True

def validate_gallery(self):
    """Returns True if Gallery object has valid data"""
    return True

def validate_brochure(self):
    """Returns True if Brochure object has valid data"""
    return True

def validate_video_link(self):
    """Returns True if VideoLink object has valid data"""
    return True

def validate_key_client(self):
    """Returns True if KeyClient has valid data"""
    return True

def validate_key_alliance(self):
    """Returns True if KeyAlliance object has valid data"""
    if self.company == self.key_alliance:
        return False
    else:
        return True

def validate_loction(self):
    """Returns True if Location object has valid data"""
    return True

def validate_certification(self):
    """Returns True if Certification object has valid data"""
    return True

def validate_social_link(self):
    """Returns True if SocialLink object has valid data"""
    return True

def validate_publication(self):
    """Returns True if Publication object has valid data"""
    return True

def validate_requirement(self):
    """Returns True if Requirement object has valid data"""
    return True
