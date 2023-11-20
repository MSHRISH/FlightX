# from API import flight_db
import secrets
from datetime import datetime,date
from flask import request
from functools import wraps



class Admin():
    def __init__(self,admin,admin_session,flight_details,bookings):
        self.admin=admin
        self.admin_session=admin_session
        self.flight_details=flight_details    
        self.bookings=bookings

    #Login the Admin
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
    
    #Add a Flight
    def add_flight(self,flight_id,flight_name,date):
        try:
            #YYYY-MM-DD
            date=datetime.strptime(date,'%Y-%m-%d').date()
        except:
            return {"Error":"Invalid Date"}, 400
        
        current_time=datetime.now().date()
        if(date<current_time):
            return {"Error":"Invalid Date"}
        
        flight_id_check=self.flight_details.find_one({"date":str(date),"flight_id":flight_id})
        if(flight_id_check!=None):
            return {"Error":"Flight with same ID exists on that day"}
        
        self.flight_details.insert_one({"flight_id":flight_id,"flight_name":flight_name,"date":str(date),"seats":60})
        return {"Message":"Flight Successfully Added.Users can book tickets now."}, 200
    
    #View all booked tickets
    def view_bookings(self,filter):      
        flight_list=list(self.flight_details.find(filter))
        if(len(flight_list)==0):
            return {"Error":"No Bookings Found.Enter proper flight details."}
        
        def make_flight_list(data_object):
            return data_object["_id"]
        flight_list=list(map(make_flight_list,flight_list))
        
        pipeline=[
            {"$match":{"flight":{"$in":flight_list}}},
            {
                "$lookup":{
                    "from":"FlightDetails",
                    "localField":"flight",
                    "foreignField":"_id",
                    "as":"flightDetails"
                }
            },
            {
                "$lookup":{
                    "from":"Users",
                    "localField":"user_id",
                    "foreignField":"_id",
                    "as":"userDetails"
                }
            },
            {
                "$unwind":"$flightDetails"
            },
            {
                "$unwind":"$userDetails"
            },
            {
                "$project":{
                    "_id":0,
                    "seats_booked":1,
                    "booking_id":1,
                    "user_name":"$userDetails.username",
                    "flight_id":"$flightDetails.flight_id",
                    "flight_name":"$flightDetails.flight_name",
                    "date":"$flightDetails.date"
                }
            }
        ]

        bookings=list(self.bookings.aggregate(pipeline))

        if(len(bookings)==0):
            return {"Error":"No Bookings Found.Enter proper flight details."}
        
        return {"Tickets Booked":bookings}



#Testing purposes kindly ignore
if __name__=="__main__":
    import pymongo
    import os
    from dotenv import load_dotenv
    load_dotenv()
    atlas_url=os.environ['MONGO_URL']
    mongo = pymongo.MongoClient(atlas_url)

    #DB
    flight_db=mongo['FlightTicketBooking']

    admin=Admin(flight_db['Admin'],flight_db['AdminSession'],flight_db["FlightDetails"],flight_db['Bookings'])
    # print(admin.admin_login("admin","admin123"))

    # print(admin.add_flight("123x","flighta","2023-12-25"))
    #YYYY-MM-DD
    # date="2023-11-20"
    # date=datetime.strptime(date,'%Y-%m-%d').date()
    # if(date<datetime.now().date()):
    #     print("OLd")    
    # print(date)
    print(admin.view_bookings({"date":"2023-12-24"}))
