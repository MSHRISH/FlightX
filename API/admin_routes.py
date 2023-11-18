from API import app
from flask import request
from API import flight_db
from API import admin_operations
from functools import wraps

admin=flight_db["Admin"]
admin_session=flight_db['AdminSession']

# admin=flight_db['Admin']
admin=admin_operations.Admin(flight_db['Admin'],flight_db["AdminSession"])

def admin_middleware(f):
    def check_session(*args,**kargs):
        try:
            key=request.headers['key']
        except:
            return {"Error":"Missing API Key in Header"}
        session_status=admin_session.find_one({"api_key":key})
        if(session_status==None):
            return {"Error":"Invalid API Key"}
        return f(*args, **kargs)
    return check_session
        
@app.route("/adminLogin", methods=["POST"])
def admin_login():
    admin_data=request.json    
    return admin.admin_login(admin_data["username"],admin_data["password"])










@app.route("/protected")
@admin_middleware
def protected():
    return "hello"



    