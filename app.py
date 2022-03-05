#-----------------------------------------------------------------------------------
# SET UP -- DEPENDENCIES AND DATABASE SETUP

#import dependencies
from flask import Flask, jsonify
import json

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#set up the database
engine=create_engine("sqlite:///hawaii.sqlite")

#access and query sqlite database file
Base=automap_base()

#reflect the database
Base.prepare(engine, reflect=True)

#save our references to each tablerement
Measurement=Base.classes.measurement
Station=Base.classes.station

#create session link from Python to database
session=Session(engine)

#----------------------------------------------------------------------------------
# DEFINE FLASK APP

#create flask application (the __name__ of the application will be app)
app=Flask(__name__)

#-----------------------------------------------------------------------------------
# CREATE THE ROUTES

# welcome route
@app.route("/")
def welcome():
    return(
        '''
        Welcome to the Climate Analysis API!
        Available Routes:
        /api/v1.0/precipitation
        /api/v1.0/stations
        /api/v1.0/tobs
        /api/v1.0/temp/start/end
        '''
    )

# precipitation analysis route
@app.route("/api/v1.0/precipitation")
def precipitation():
    #add line that calculates the date on year ago
    prev_year=dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #write a query to get date and precipitation for the previous year
    precipitation=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=prev_year).all()

    #create dictionary with dates as key and precipitation as value 
    #name  = {key:value for key, value in session-query}
    precip = {date:prcp for date,prcp in precipitation}

    #jsonify the file
    #(json files are structured textfiles with attribute-value pairs that can be pushed onto web interfaces, like flask)
    return jsonify(precip)

#stations route
@app.route("/api/v1.0/stations")
def stations():
    #create a uery that allows us to get all the stations in database
    results=session.query(Station.station).all()

    #put results into a one-dimensional array using ravel, then unravel results into list
    stations=list(np.ravel(results))
    return jsonify(stations=stations)

#temperature observations route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    #calculate date from one year ago
    prev_year=dt.date(2017, 8, 13) - dt.timedelta(days=365)

    #query the primary station for all temp observations from the previous year
    results=session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= prev_year).all()

    #unravel results into one-dimensional array and conver array to list
    temps=list(np.ravel(results))

    #return list of jsonfied list
    return jsonify(temps=temps)

#statistics route
#this route will need us to provide starting and ending dates.
#NOTE: when run in browser, you input the <start> and <end> dates in the format YYYY-MM-DD
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):#add parameters to the stats() function
    #create query to select min, avg, and max temps from sqlite database
    sel=[func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    #create an if-not statement. if end is not False (meaning, if end is empty)
    if not end:
        # * indicates that there will be multiple results for query (reutrns min, avg, and max. 3 results)
        #results only take start into account
        results=session.query(*sel).filter(Measurement.date>=start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    #result takes noth start and end into account
    results=session.query(*sel).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    temps=list(np.ravel(results))
    return jsonify(temps)