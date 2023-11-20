from API import app
from flask import request
from API import flight_db
from API import admin_operations
from functools import wraps

admin=flight_db["Admin"]
admin_session=flight_db['AdminSession']
flight_details=flight_db["FlightDetails"]
bookings=flight_db["Bookings"]

# admin=flight_db['Admin']
admin=admin_operations.Admin(admin,admin_session,flight_details,bookings)

def admin_middleware(f):
    @wraps(f)
    def check_session(*args,**kwargs):
        try:
            key=request.headers['key']
        except:
            return {"Error":"Missing API Key in Header"}, 400
        session_status=admin_session.find_one({"api_key":key})
        if(session_status==None):
            return {"Error":"Invalid API Key"}, 400
        return f(*args, **kwargs)
    return check_session
        
@app.route("/adminLogin", methods=["POST"])
def admin_login():
    admin_data=request.json    
    return admin.admin_login(admin_data["username"],admin_data["password"])

@app.route("/addFlight",methods=["POST"])
@admin_middleware
def add_flight():
    flight_data=request.json
    return admin.add_flight(flight_data["flightid"],flight_data['flightname'],flight_data['date'])



@app.route("/viewBookings")
@admin_middleware
def view_bookings():
    return admin.view_bookings(request.args)
    