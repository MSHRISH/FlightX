# from API import flight_db
import secrets
from datetime import datetime,date
from flask import request
from functools import wraps


class Admin():
    def __init__(self,admin,admin_session,flight_details):
        self.admin=admin
        self.admin_session=admin_session
        self.flight_details=flight_details    
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
    
    def add_flight(self,flight_id,flight_name,date):
        try:
            #YYYY-MM-DD
            date=datetime.strptime(date,'%Y-%m-%d').date()
        except:
            return {"Error":"Invalid Date"}, 400
        current_time=datetime.now().date()
        if(date<current_time):
            return {"Error":"Invalid Date"}
        self.flight_details.insert_one({"flight_id":flight_id,"flight_name":flight_name,"date":str(date),"seats":60})
        return {"Message":"Flight Successfully Added.Users can book tickets now."}, 200

if __name__=="__main__":
    import pymongo
    import os
    from dotenv import load_dotenv
    load_dotenv()
    atlas_url=os.environ['MONGO_URL']
    mongo = pymongo.MongoClient(atlas_url)

    #DB
    flight_db=mongo['FlightTicketBooking']

    admin=Admin(flight_db['Admin'],flight_db['AdminSession'],flight_db["FlightDetails"])
    # print(admin.admin_login("admin","admin123"))

    print(admin.add_flight("123x","flighta","2023-12-25"))
    #YYYY-MM-DD
    # date="2023-11-20"
    # date=datetime.strptime(date,'%Y-%m-%d').date()
    # if(date<datetime.now().date()):
    #     print("OLd")    
    # print(date)
