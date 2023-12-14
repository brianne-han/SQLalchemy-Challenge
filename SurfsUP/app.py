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
    results = session.query(Station.station).group_by(Station.station).all()
    stations_list = list(np.ravel(results))
    resturn jsonify(stations_list)


# 4. /api/v1.0/tobs. Query the dates and temperature observations of the most-active station for the previous year of data. 
# Return a JSON list of temperature observations for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    year_results = session.query(Measurement.tobs).\
        filter(Station.station == 'USC00519281').\
        filter(Measurement.date >= one_year).all()
    temp = list(np.ravel(year_results))

    return jsonify(temp)


# 5. /api/v1.0/<start> and /api/v1.0/<start>/<end>. Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

@app.route("/api/v1.0/<start>")
def temps_start():
    session = Session(engion)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    
    session.close()

    temps = []
    for min_temp, avg_temp, max_temp in results:
        temps_dict = {}
        temps_dict['Min Temp'] = min_temp
        temps_dict['Avg Temp'] = avg_temp
        temps_dict['Max Temp'] = max_temp
        temps.append(temps_dict)

    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def temps_start_end():
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()

    temps = []
    for temp_min, temp_avg, temp_max in results:
        temps_dict = {}
        temps_dict["Min Temp"] = min_temp
        temps_dict["Avg Temp"] = avg_temp
        temps_dict["Max Temp"] = max_temp
        temps.append(temps_dict)

    return jsonify(temps)

    

