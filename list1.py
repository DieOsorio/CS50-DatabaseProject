import os

from flask import Flask, render_template, request
import models as data


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
data.db.init_app(app)

def main():
  flights = data.Flight.query.all()
  for flight in flights:
    print(f"{flight.origin} to {flight.destination}, {flight.duration} minutes.")

if __name__ == "__main__":
  with app.app_context():
    main()