from flask import Flask, request, redirect
import os
# from dotenv import load_dotenv
# load_dotenv()

import pymongo
atlas_url=os.environ["mongodb+srv://mynameisshrish:R7N0Q9EQXVHKoFWi@flight.gzqsbny.mongodb.net/"]
mongo = pymongo.MongoClient(atlas_url)

#DB
flight_db=mongo['FlightTicketBooking']


app=Flask(__name__)

from API import documentation
from API import admin_routes
from API import user_routes

@app.route("/")
def redirect_to_docs():
     return redirect("/api/docs", code=302)

