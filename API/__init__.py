from flask import Flask, request, redirect
import os
from dotenv import load_dotenv
load_dotenv()

#connect to mongo
import pymongo
atlas_url=os.environ['MONGO_URL']
mongo = pymongo.MongoClient(atlas_url)

#DB
flight_db=mongo['FlightTicketBooking']


app=Flask(__name__)

from API import documentation # Swagger Docs
from API import admin_routes  #Routes related to Admin 
from API import user_routes   #Routes related to User

#Redirect to the API Documentation
@app.route("/")
def redirect_to_docs():
     return redirect("/api/docs")

