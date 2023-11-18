from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()
import os



import pymongo
atlas_url=os.environ['MONGO_URL']
mongo = pymongo.MongoClient(atlas_url)

#DB
flight_db=mongo['FlightTicketBooking']




app=Flask(__name__)

from API import documentation
from API import admin_routes

