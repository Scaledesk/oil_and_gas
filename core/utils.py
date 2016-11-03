from django.contrib.auth import authenticate
from django.contrib.auth.models import User


def authenticate_user(username,password):
    """util function for authenticating the user"""
    current_user=authenticate(username=username,password=password)
    authed=False
    if current_user:
        authed=True
    return authed, current_user

def register_user(email, password, first_name, last_name):
    """util function to register the user"""
    registered=False
    current_user=User.object.create(email,email,password)
    registered=True
    return registered,'User registered successfully',current_user

def change_password(username,password):
    """Util functiopn for changing the password of the user"""
    current_user=User.objects.get(username=username)
    current_user.set_password(password)
    current_user.save()
    return True