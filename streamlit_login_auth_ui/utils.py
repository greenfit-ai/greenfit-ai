import re
import json
from courier.client import Courier
import secrets
import hashlib
import requests
from supabase import Client, create_client
from .secretsStreamlit import supa_key, supa_url

class PasswordHasher:
    def __init__(self):
        self.hasher = "hashlib"
        self.hashing_algorithm = "sha256"
    def hash(self, password: str) -> str:
        hashed_obj = hashlib.sha256(password.encode())
        digested = hashed_obj.hexdigest()
        return digested

ph = PasswordHasher() 
supabase: Client = create_client(supabase_url=supa_url, supabase_key=supa_key)

def welcome_w_email(auth_token: str, username_forgot_passwd: str, email_forgot_passwd: str, company_name: str) -> None:
    """
    Triggers an email to the user containing the randomly generated password.
    """
    client = Courier(authorization_token = auth_token)
    resp = client.send(
    message={
        "to": {
        "email": email_forgot_passwd
        },
        "content": {
        "title": company_name + ": Login Password!",
        "body": "Hi! " + username_forgot_passwd + "," + "\n" + "\n" + f"With this email, we are glad to welcome you to {company_name} "
        },
    }
    )

def check_usr_pass(username: str, password: str) -> bool:
    """
    Authenticates the username and password.
    """
    query = supabase.from_("user_authentication").select("*").eq("username", username).eq("password", ph.hash(password)).execute()
    if len(query.data) > 0:
        return True
    return False


def load_lottieurl(url: str) -> str:
    """
    Fetches the lottie animation using the URL.
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        pass


def check_valid_name(name_sign_up: str) -> bool:
    """
    Checks if the user entered a valid name while creating the account.
    """
    name_regex = (r'^[A-Za-z_][A-Za-z0-9_]*')

    if re.search(name_regex, name_sign_up):
        return True
    return False


def check_valid_email(email_sign_up: str) -> bool:
    """
    Checks if the user entered a valid email while creating the account.
    """
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex, email_sign_up):
        return True
    return False


def check_unique_email(email_sign_up: str) -> bool:
    """
    Checks if the email already exists (since email needs to be unique).
    """
    query = supabase.from_("user_authentication").select("email").execute()
    authorized_user_data_master = [datum["email"] for datum in query.data]
    if email_sign_up in authorized_user_data_master:
        return False
    return True


def non_empty_str_check(username_sign_up: str) -> bool:
    """
    Checks for non-empty strings.
    """
    empty_count = 0
    for i in username_sign_up:
        if i == ' ':
            empty_count = empty_count + 1
            if empty_count == len(username_sign_up):
                return False

    if not username_sign_up:
        return False
    return True


def check_unique_usr(username_sign_up: str):
    """
    Checks if the username already exists (since username needs to be unique),
    also checks for non - empty username.
    """
    query = supabase.from_("user_authentication").select("username").execute()
    authorized_user_data_master = [datum["username"] for datum in query.data]

    if username_sign_up in authorized_user_data_master:
        return False
    
    non_empty_check = non_empty_str_check(username_sign_up)

    if non_empty_check == False:
        return None
    return True


def register_new_usr(name_sign_up: str, email_sign_up: str, username_sign_up: str, password_sign_up: str) -> None:
    """
    Saves the information of the new user in the _secret_auth.json file.
    """
    new_usr_data = {'username': username_sign_up, 'name': name_sign_up, 'email': email_sign_up, 'password': ph.hash(password_sign_up)}

    supabase.table("user_authentication").insert(new_usr_data).execute()


def check_username_exists(user_name: str) -> bool:
    """
    Checks if the username exists in the _secret_auth.json file.
    """
    query = supabase.from_("user_authentication").select("username").execute()
    authorized_user_data_master = [datum["username"] for datum in query.data]

    if user_name in authorized_user_data_master:
        return True
    return False
        

def check_email_exists(email_forgot_passwd: str):
    """
    Checks if the email entered is present in the _secret_auth.json file.
    """
    query = supabase.from_("user_authentication").select("*").execute()
    authorized_users_data = query.data

    for user in authorized_users_data:
        if user['email'] == email_forgot_passwd:
            return True, user['username']
    return False, None


def generate_random_passwd() -> str:
    """
    Generates a random password to be sent in email.
    """
    password_length = 10
    return secrets.token_urlsafe(password_length)


def send_passwd_in_email(auth_token: str, username_forgot_passwd: str, email_forgot_passwd: str, company_name: str, random_password: str) -> None:
    """
    Triggers an email to the user containing the randomly generated password.
    """
    client = Courier(authorization_token = auth_token)
    resp = client.send(
    message={
        "to": {
        "email": email_forgot_passwd
        },
        "content": {
        "title": company_name + ": Login Password!",
        "body": "Hi! " + username_forgot_passwd + "," + "\n" + "\n" + "Your temporary login password is: " + random_password  + "\n" + "\n" + "{{info}}"
        },
        "data":{
        "info": "Please reset your password at the earliest for security reasons."
        }
    }
    )


def change_passwd(email_: str, random_password: str) -> None:
    """
    Replaces the old password with the newly generated password.
    """
    query = supabase.table("user_authentication").update({"password": ph.hash(random_password)}).eq("email", email_).execute()

    

def check_current_passwd(email_reset_passwd: str, current_passwd: str) -> bool:
    """
    Authenticates the password entered against the username when 
    resetting the password.
    """
    query = supabase.from_("user_authentication").select("*").eq("email", email_reset_passwd).eq("password", ph.hash(current_passwd)).execute()
    if len(query.data) > 0:
        return True
    return False

# Author: Gauri Prabhakar
# GitHub: https://github.com/GauriSP10/streamlit_login_auth_ui












