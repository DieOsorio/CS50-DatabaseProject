import csv
import os

from flask import Flask, render_template, request
import models as data


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
data.db.init_app(app)

def main():
  f = open("flights.csv")
  reader = csv.reader(f)
  for origin, destination, duration in reader:
    flight = data.Flight(origin=origin, destination=destination, duration=duration)
    data.db.session.add(flight)
    print(f"Add flight from {origin} to {destination} lasting {duration} minutes.")
  data.db.session.commit()

if __name__ == "__main__":
  with app.app_context():
    main()