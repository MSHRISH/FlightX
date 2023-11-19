from API import app
from flask import request
from API import flight_db
from API import user_operations

user=user_operations.User(flight_db["Users"],flight_db["UserSession"])



@app.route("/userSignUp",methods=['POST'])
def user_signup():
    user_data=request.json
    return  user.user_signup(user_data['username'],user_data['email'],user_data['password'])


@app.route("/userLogin",methods=['POST'])
def user_login():
    user_data=request.json
    return user.user_login(user_data['username'],user_data['password'])
