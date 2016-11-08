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
    cm.owner = User.objects.get(is_superuser=True)
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
            user = User.objects.get(email=data_dict['user_email'])
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
        user = user=User.objects.get(email=data_dict['user_email'])
        if ClaimCompanyRequestUtil(user, company_name):
            return True
        else:
            return False
    else:
        return False


#### Free Fields ####

def CreateFreeFieldsUtil(data_dict, company):
    """
    Util function to save Free Fields
    """
    ff=FreeFields()
    ff.company = company
    ff.address_line1 = data_dict['address_line1']
    ff.address_line1 = data_dict['address_line2']
    ff.address_line3 = data_dict['address_line3']
    ff.city = data_dict['city']
    ff.pin = data_dict['pin']
    ff.website = data_dict['website']
    ff.year_founded = data_dict['year_founded']
    ff.about = data_dict['about']
    ff.save()
    return True

#### Free Feind End ####

#### Premium Fields ####

def CreatePremiumFieldsUtil(data_dict, files, company):
    pf = PremiumFields()
    pf.company = company
    pf.logo = files['logo'] #See later if files to passed will be individual file or dictionary of files depending on how the form are filled.
    pf.registration_no = data_dict['registration_no']
    pf.no_of_emp = data_dict['no_of_emp']
    pf.sale_volume = data_dict['sale_volume']
    pf.save()
    return True

def CreateGallaryUtil(files, company):
    g = Gallery()
    g.company = company
    g.image = files['gallery']

def CreateBrochureUtil(files, company):
    b = Brochure()
    b.brochure = files['brochure']
    b.save()
    return True

def CreateVideoLinkUtil(data_dict, company):
    vl = VideoLink()
    vl.company = company
    vl.video_link = data_dict['video_link']
    vl.save()

def CreateKeyClient(data_dict, company):
    kc = KeyClient()
    kc.company = company
    kc.key_client = data_dict['key_client']

def CreateKeyAlliance(data_dict, company):
    ka = KeyAlliance()
    ka.company = company
    ka.key_alliance = data_dict['key_alliance']

def CreateLocation(data_dict, company):
    l = Location()
    l.company = company
    l.company_type = data_dict['company_type']
    l.company = data_dict['company']

def CreateCertificationUtil(data_dict, files, company):
    c = Certification()
    c.company = company
    c.certi_name = data_dict['certi_name']
    c.certi_description = data_dict['certi_description']
    c.certi_doc = files['certi_doc']

def CreateSocialLinkUtil(data_dict, company):
    sl = SocialLinks()
    sl.facebook = data_dict['facebook']
    sl.twitter = data_dict['twitter']
    sl.linkedin = data_dict['linkedin']