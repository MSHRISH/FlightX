# from API import flight_db
import secrets
from datetime import datetime,date


class Admin():
    def __init__(self,admin,admin_session):
        self.admin=admin
        self.admin_session=admin_session
    
    def admin_login(self,user_name,pass_word):
        check_auth=self.admin.find_one({"admin_user":user_name,"admin_password":pass_word})
        
        if(check_auth!=None):
            session_check=self.admin_session.find_one({"admin_user":user_name})
        
            if(session_check!=None):

                return {"Message":"Already Logged In.","key":session_check["api_key"]}, 200
        
            api_key=secrets.token_urlsafe(16)
            self.admin_session.insert_one({"admin_user":user_name,"login_time":datetime.utcnow(),"api_key":api_key})
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

    admin=Admin(flight_db['Admin'],flight_db['AdminSession'])
    print(admin.admin_login("admin","admin123"))
