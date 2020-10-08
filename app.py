  
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()


# reflect the tables
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station
session=Session(engine)


app = Flask(__name__)

#Routes

@app.route("/")
def welome():
    return(
        f'Welcome to Climate App! <br/>'
        f'Avaiable Routes: </br>'
        f'/api/v1.0/precipitation </br>'
        f'/api/v1.0/stations </br>'
        f'/api/v1.0/tobs </br>'
        f'/api/v1.0/<start> </br>'
        f'/api/v1.0/<start>/<end></br>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    #Query the dates and precipitation
    results = session.query(func.strftime("%Y-%m-%d", measurement.date), measurement.prcp).\
    filter(func.strftime("%Y-%m-%d",measurement.date) >= dt.date(2016, 8, 23)).all()

    #add to a dictionary    
    for result in results:
        precip_dict= {}
        precip_dict["date"]= measurement.date
        precip_dict["prcp"]= measurement.prcp
    return jsonify(results)

@app.route('/api/v1.0/stations')
def station():
    results = active = session.query(measurement.station, func.count(measurement.station)).\
    group_by(measurement.station).\
    order_by(func.count(measurement.station).desc()).all()
    
    list_stations = list(np.ravel(results))

    return jsonify(list_stations)

@app.route('/api/v1.0/tobs')
def temp():
    results = session.query(measurement.station, measurement.tobs).\
        filter(measurement.date >= "2016, 8, 23").\
        filter(measurement.station == "USC00519281").all()
    
    # Convert list into dictionary
    for result in results:
        results_dict = {}
        results_dict["date"]=measurement.station
        results_dict["tobs"]=measurement.tobs
    return jsonify(results)

@app.route('/api/v1.0/<start>')

def start_temp(start):
    data = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >=start).all()
    return jsonify(data)

@app.route('/api/v1.0/<start>/<end>')

def start_end_temp(start, end):
    data = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >=start, measurement.date <= end).all()
    return jsonify(data)
if __name__ == "__main__":
    app.run(debug=True)

    