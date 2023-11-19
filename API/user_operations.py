import secrets
import hashlib
import re
from datetime import datetime,date
from flask import request

class User():
    def __init__(self,users,user_session):
        self.users=users
        self.user_session=user_session
    
    def user_signup(self,username,email,password):
        check_unique_name=self.users.find_one({"username":username})
        if(check_unique_name!=None):
            return {"Error":"Username already exists"}
        
        check_unique_email=self.users.find_one({"email":email})
        if(check_unique_email!=None):
            return {"Error":"Email already exists"}
        
        if(not username.isalpha()):
            return {"Error":"Username must only contain alphabets."}
        if(len(username)<6 or len(username)>20):
            return {"Error":"Username must be atleast 6 characters long and can have atmost 20 characters."}
        
        email_pattern=r'[a-zA-Z0-9_.]+@[a-zA-Z0-9_.]+\.[a-zA-Z0-9]+$'
        if(not bool(re.match(email_pattern,email))):
            return {"Error":"Invalid Email"}
        
        if(not password.isalnum()):
            return {"Error":"Password must contain only alphabets and numbers."}
        if(len(password)<6 or len(password)>20):
            return {"Error":"Password must be atleast 6 characters and can have atmost 20 characters."}
        
        password=hashlib.md5(password.encode()).hexdigest()
        self.users.insert_one({"username":username,"email":email,"password":password})
        return {"Message":"Signup Successful.Login with your username or signed up email and password."}

    def user_login(self,username,password):
        check_auth=self.users.find_one({"$or":[{"username":username},{"email":username}],"password":hashlib.md5(password.encode()).hexdigest()})
    
        if(check_auth!=None):
            session_check=self.user_session.find_one({"user_id":check_auth['_id']})
        
            if(session_check!=None):
                return {"Message":"Already Logged In.","key":session_check["api_key"]}, 200
        
            api_key=secrets.token_urlsafe(16)
            self.user_session.insert_one({"user_id":check_auth['_id'],"login_time":datetime.utcnow(),"api_key":api_key})
            return {"Message":"Logged In Successfully.","key":api_key}, 200
        
        return {"Error":"Invalid Credentials"}, 400


if __name__=="__main__":
    import pymongo
    import os
    from dotenv import load_dotenv
    load_dotenv()
    atlas_url=os.environ['MONGO_URL']
    mongo = pymongo.MongoClient(atlas_url)
    
    #DB
    flight_db=mongo['FlightTicketBooking']
    user=User(flight_db['Users'],flight_db["UserSession"])
    # print(user.user_signup("tester","tester@gmail.com","tester123"))
    print(user.user_login("shrish","shrish123"))
