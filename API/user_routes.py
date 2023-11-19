from API import app
from flask import request
from API import flight_db
from API import user_operations
from functools import wraps

users=flight_db["Users"]
user_session=flight_db['UserSession']
flight_details=flight_db["FlightDetails"]

user=user_operations.User(users,user_session,flight_details)

def user_middleware(f):
    @wraps(f)
    def check_session(*args,**kwargs):
        try:
            key=request.headers['key']
        except:
            return {"Error":"Missing API Key in Header"}, 400
        session_status=user_session.find_one({"api_key":key})
        if(session_status==None):
            return {"Error":"Invalid API Key"}, 400
        return f(*args, **kwargs)
    return check_session
        

@app.route("/userSignUp",methods=['POST'])
def user_signup():
    user_data=request.json
    return  user.user_signup(user_data['username'],user_data['email'],user_data['password'])


@app.route("/userLogin",methods=['POST'])
def user_login():
    user_data=request.json
    return user.user_login(user_data['username'],user_data['password'])



@app.route("/searchFlight")
@user_middleware
def search_flights():
    return user.search_flight(request.json)