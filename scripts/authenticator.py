from supabase import Client, create_client
from .secretsStreamlit import supa_key, supa_url
import hashlib

supabase: Client = create_client(supabase_url=supa_url, supabase_key=supa_key)

def get_auth(username: str, password: str):
    hashed_obj = hashlib.sha256(password.encode())
    digested = hashed_obj.hexdigest()
    query = supabase.from_("user_authentication").select("*").eq("user_name", username).eq("password", digested).execute()
    check_username = supabase.from_("user_authentication").select("*").eq("user_name", username).execute()
    check_pwd = supabase.from_("user_authentication").select("*").eq("password", digested).execute()
    user_data = query.data
    print(user_data)
    if len(user_data) == 0:
        if len(check_username.data) == 0 and len(check_pwd.data) == 0:
            supabase.table("user_authentication").insert({"user_name": username, "password": digested}).execute()
            print("Get auth: True")
            return True
        else:
            print("Get auth: False")
            return False
    else:
        print("Get auth: True")
        return True

