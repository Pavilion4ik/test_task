from flask import Flask, jsonify, request
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from collections import Counter

from validators import EventQueryParams

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "events.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# database connection
engine = create_engine('sqlite:///events.db')
metadata = MetaData()
metadata.reflect(bind=engine)
# get database table
events = metadata.tables['events']
Session = sessionmaker(bind=engine)
session = Session()


@app.route("/api/info")
def get_info():
    res = [{"startDate": "2019-06-01", "endDate": "2019-07-01", "Type": ["cumulative", "usual"],
            "Grouping": ["weekly", "bi-weekly", "monthly"], "Filters": ["attr", "values"]}]
    return jsonify({"possible_filtering": res})


@app.route("/api/timeline")
def get_timeline():
    args = request.args
    startDate = args.get("startDate")
    endDate = args.get("endDate")
    type_ = args.get("Type")
    grouping = args.get("Grouping")
    try:
        EventQueryParams(type_=type_, grouping=grouping)
    except Exception as e:
        return jsonify({'message': str(e)}), 400

    result = {"timeline": []}
    if None not in (startDate, endDate):
        events_result = session.query(events).filter(events.c.date >= startDate,
                                                     events.c.date <= endDate).all()
        print([type(e) for e in events_result])
        count_date = dict(Counter([event.date for event in events_result]))
        for date, count in count_date.items():
            result["timeline"].append({"date": date.strftime("%Y-%m-%d"), "value": count,
                                       "type": type_, "grouping": grouping})

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
