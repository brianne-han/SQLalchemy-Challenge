# Import the dependencies.
import np as numpy
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# 1. / Start at the homepage. List all the available routes.

@app.route("/")
def welcome():
    f"Welcome to the Hawaii Climate API<br/>"
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/<start> (enter as YYYY-MM-DD)<br/>"
    f"/api/v1.0/<start>/<end> (enter as YYYY-MM-DD/YYYY-MM-DD)"


# 2. /api/v1.0/precipitation. Convert the query results from your precipitation analysis 
# (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    one_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    prev_year_date = dt.date(one_year.year, one_year.month, one_year.day)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year_date).order_by(Measurement.date).all()

    prcp_dict = dict(results)
    return jsonify(prcp_dict)


# 3. /api/v1.0/stations. Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    

