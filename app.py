import pandas as pd
import datetime as dt 
import numpy as np 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#  Database Setup

engine = create_engine("sqlite:///resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

#  Saving References

Measurement = Base.classes.measurement
Station = Base.classes.station

#  Creating A Session

session = Session(engine)


# Flask Setup

app = Flask(__name__)

#  Setting Up Routes

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API <br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    
    )
@app.route("/api/v1.0/precipitation")
def precipitation():

    previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    precipitation = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date >= previous_year).all()
    
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():

    results = session.query(Station.station).all()

    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
   
    previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= previous_year).all()

    temps = list(np.ravel(results))

    return jsonify(results)



    
if __name__ == '__main__':
    app.run()