import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# # Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################



# Define what to do when a user hits the index route
@app.route("/")
def home():
    return (
        f"Available Routs:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return precipitation measurements"""
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    precip_dict = dict(results)

    return precip_dict


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return stations"""
    results = session.query(Station.station, Station.name).all()

    station_list = dict(results)

    session.close()


    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return tobs measurements"""

    oneYear = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > oneYear).\
    filter(Measurement.station == 'USC00519281').all()

    session.close()

    # Convert list of tuples into normal list
    tobs_dict = dict(results)

    return jsonify(tobs_dict)


@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return tobs measurements"""

    minTemp = session.query(func.min(Measurement.tobs)).filter(Measurement.date > start).one()
    maxTemp = session.query(func.max(Measurement.tobs)).filter(Measurement.date > start).one()
    avgTemp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date > start).one()

    session.close()

    # Store in dictionary
    filter_dict = {"Minimum Temperature": minTemp[0], "Maximum Temperature": maxTemp[0], "Average Temperature": avgTemp[0]}

    return jsonify(filter_dict)

@app.route("/api/v1.0/<start>/<end>")
def tempDates(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return tobs measurements"""

    minTemp = session.query(func.min(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date < end).one()
    maxTemp = session.query(func.max(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date < end).one()
    avgTemp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date < end).one()

    session.close()

    # Store in dictionary
    filter_dict = {"Minimum Temperature": minTemp[0], "Maximum Temperature": maxTemp[0], "Average Temperature": avgTemp[0]}

    return jsonify(filter_dict)


if __name__ == "__main__":
    app.run(debug=True)
