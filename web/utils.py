from django.contrib.auth.models import User
from core.models import *
from pprint import pprint



def CreateUserUtil(data_dict):
    """
    Util function for Adding New User. Returns true if executed sucessfully.
    """
    first_name = data_dict["first_name"]
    last_name = data_dict["last_name"]
    user_email = data_dict['user_email']
    password = data_dict["password"]
    current_user = User.objects.create_user(username = user_email, email = user_email, password = password, first_name = first_name, last_name = last_name)
    return True

def CreateUserProfileUtil(data_dict):
    """
    Util function for registering user. Returns true if executed sucessfully.
    """
    up = UserProfile()
    up.user = User.objects.get(email=data_dict['user_email'])
    up.gender = data_dict["gender"]
    up.dob = data_dict["dob"]
    up.user_phone_no = data_dict["user_phone_no"]
    up.save()
    return True

def CreateUserAndUserProfileUtil(data_dict):
    """
    Util function for Adding New User by creating entry in user and userprofile table. Returns true if executed sucessfully.
    """
    first_name = data_dict["first_name"]
    last_name = data_dict["last_name"]
    user_email = data_dict['user_email']
    password = data_dict["password"]
    current_user = User.objects.create_user(username = user_email, email = user_email, password = password, first_name = first_name, last_name = last_name)

    up = UserProfile()
    # up.user = User.objects.get(email=data_dict['user_email'])
    up.user = current_user
    up.gender = data_dict["gender"]
    up.dob = data_dict["dob"]
    up.user_phone_no = data_dict["user_phone_no"]
    up.save()
    return True

def CreateCompanyUtil(data_dict):
    """
    Util function for Adding New Company. Returns true if executed sucessfully.
    """
    cm = CompanyModel()
    # cm.owner = UserProfile.objects.get(user=User.objects.get(email=data_dict['user_email']))is_superuser=True
    cm.owner = UserProfile.objects.get(user=User.objects.filter(is_superuser=True))
    cm.company_name = data_dict['company_name']
    cm.company_email = data_dict['company_email']
    cm.company_phone_no = data_dict['company_phone_no']
    cm.ad_reference = data_dict['ad_reference']
    cm.save()
    return True

def ClaimCompanyRequestUtil(user, company_name):
    """
    Util funciton to save claim request by a particular user to database
    """
    cr = ClaimCompanyRequest()
    cr.user = user
    cr.company = CompanyModel.objects.get(company_name=company_name)
    cr.save()
    return True

def CreateUserAndCompanyUtil(data_dict):
    """
    Util function for user, user profile and company. Returns true if executed sucessfully.
    """
    if CreateUserAndUserProfileUtil(data_dict):
        if CreateCompanyUtil(data_dict):
            user = UserProfile.objects.get(user=User.objects.get(email=data_dict['user_email']))
            company_name = data_dict['company_name']
            if ClaimCompanyRequestUtil(user, company_name):
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def CreateUserAndClaimCompanyUtil(data_dict, company_name):
    """
    Util function for createing a new user and than save his request to claim the company.
    """
    if CreateUserAndUserProfileUtil(data_dict):
        user = UserProfile.objects.get(user=User.objects.get(email=data_dict['user_email']))
        pprint(user)

        if ClaimCompanyRequestUtil(user, company_name):
            return True
        else:
            return False
    else:
        return False