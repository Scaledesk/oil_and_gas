from django.contrib.auth.models import User
from core.models import *
from pprint import pprint
from datetime import datetime



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
    cm.sub_plan = SubscriptionPlan.objects.get(sub_type='F')
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

def IsPremium(user):
    """
    Util function return Trye if the company of user has premium/super_premium subscription.
    """
    c = CompanyModel.objects.get(owner=user)
    if c.sub_plan.sub_type=='P' or c.sub_plan.sub_type=='S':
        return True
    else:
        return False

def IsPremium(user):
    """
    Util function return true only if the company of user has superpremium subscription
    """
    c = CompanyModel.objects.get(owner=user)
    if c.sub_plan.sub_type=='S':
        return True
    else:
        return False

############################################## Free Fields #######################################################

def CreateFreeFieldUtil(data_dict, user):
    """
    Util function to save Free Fields
    """
    pprint(str(user))
    pprint(str(data_dict))
    ff=FreeField()
    ff.company = CompanyModel.objects.get(owner=user)
    ff.address = data_dict['address']
    ff.city = data_dict['city']
    ff.pin = data_dict['pin']
    ff.website = data_dict['website']
    ff.year_founded = data_dict['year_founded']
    ff.about = data_dict['about']
    ff.save()
    return True

############################################## Free Feind End ########################################################

############################################## Premium Fields ######################################################


def CreateBasicPremiumFieldUtil(data_dict, user):
    """
    Util function to save the basic premium field model data.
    """
    pf = BasicPremiumField()
    pf.company = CompanyModel.objects.get(owner=user)
    pf.logo = data_dict['logo'] #See later if files to passed will be individual file or dictionary of files depending on how the form are filled.
    pf.registration_no = data_dict['registration_no']
    pf.bio = data_dict['bio']
    pf.no_of_emp = data_dict['no_of_emp']
    pf.sale_volume = data_dict['sale_volume']
    pf.save()
    return True

def CreateGalleryUtil(files, user):
    """
    Util model to save the gallery image for the company.
    """
    g = Gallery()
    g.company = CompanyModel.objects.get(owner=user)
    g.image = files['image']
    g.save()
    return True

def CreateBrochureUtil(data_dict, user):
    """
    Util function to save the company brochure.
    """
    b = Brochure()
    b.company = CompanyModel.objects.get(owner=user)
    b.brochure = data_dict['brochure']
    b.save()
    return True

def CreateVideoLinkUtil(data_dict, user):
    """
    Util function to save the video link of the company.
    """
    vl = VideoLink()
    vl.company = CompanyModel.objects.get(owner=user)
    vl.video_link = data_dict['video_link']
    vl.save()
    return True

def CreateKeyClient(data_dict, user):
    """
    Util function to save the key clients of the company.
    """
    return True
    kc = KeyClient()
    kc.company = CompanyModel.objects.get(owner=user)
    kc.key_client = data_dict['key_client']
    return True

def CreateKeyAlliance(data_dict, user):
    """
    Util funcition to save the alliance from companymodel database.
    """
    ka = KeyAlliance()
    ka.company = CompanyModel.objects.get(owner=user)
    ka.key_alliance = data_dict['key_alliance']
    ka.save()
    return True

def CreateLocationUtil(data_dict, user):
    """
    Util function to save the company locations.
    """
    l.company = CompanyModel.objects.get(owner=user)
    l.location_type = data_dict['location_type']
    l.location = data_dict['location']
    l.save()
    return True

def CreateCertificationUtil(data_dict, user):
    """
    Util function to save the certificates sofy copy of the company
    """
    c = Certification()
    c.company = CompanyModel.objects.get(owner=user)
    c.certi_name = data_dict['certi_name']
    c.certi_description = data_dict['certi_description']
    c.certi_doc = data_dict['certi_doc']
    c.save()
    return True

def CreateSocialLinkUtil(data_dict, user):
    """
    Util function to save the links of social media links of the company.
    """
    sl = SocialLink()
    sl.company = CompanyModel.objects.get(owner=user)
    sl.facebook = data_dict['facebook']
    sl.twitter = data_dict['twitter']
    sl.linkedin = data_dict['linkedin']
    sl.save()
    return True

####################################### Premium Fields End ####################################################


################################ Super Premium Fields Start #######################################

def PublicationUtil(data_dict, user):
    """
    Util functio to save the Published articles of the company.
    """
    p = Publication()
    p.company = CompanyModel.objects.get(owner=user)
    p.pub_type = data_dict['pub_type']
    p.pub_content = data_dict['pub_content']
    p.save()
    return True