from core.models import CompanyModel
from django.contrib.auth.models import User
from core.models import UserProfile



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
    up.user_phone_number = data_dict["user_phone_no"]
    up.save()
    return True

def CreateCompanyUtil(data_dict):
    """
    Util function for Adding New Company. Returns true if executed sucessfully.
    """
    cm = CompanyModel()
    cm.owner = UserProfile.objects.get(user=User.objects.get(email=data_dict['user_email']))
    cm.company_name = data_dict['company_name']
    cm.company_email = data_dict['company_email']
    cm.company_phone_no = data_dict['company_phone_no']
    cm.ad_reference = data_dict['ad_reference']
    cm.save()
    return True

def ClaimCompanyRequestUtil(user, company):
    """
    Util funciton to save claim request by a particular user to database
    """
    cr = user
    cr.company = company
    cr.save()
    return True

def CreateUserAndCompanyUtil(data_dict):
    """
    Util function for user, user profile and company. Returns true if executed sucessfully.
    """
    if CreateUserUtil(data_dict):
        if CreateUserProfileUtil(data_dict):
            if CreateCompanyUtil(data_dict):
                return True
    else:
        return False

def CreateUserAndClaimCompanyUtil(data_dict, company):
    """
    Util function for createing a new user and than save his request to claim the company.
    """
    user = None
    if CreateUserUtil(data_dict):
        user = UserProfile.objects.get(user=User.objects.get(email=data_dict['user_email']))
        if ClaimCompanyRequestUtil(user, company):
            return True
        else:
            False
    else:
        False