import os
from flask import Flask, render_template, request
import models as data


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
data.db.init_app(app)

@app.route("/")
def index():
  flights = data.Flight.query.all()
  return render_template("index.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
  """Book a flight."""

  # Get form information
  name = request.form.get("name")
  try:
    flight_id = int(request.form.get("flight_id"))
  except ValueError:
    return render_template("error.html", message="Invalid flight number.")

  # Make sure the flight exist
  flight = data.Flight.query.get(flight_id)
  if flight is None:
    return render_template("error.html", message="No such flight with that id.")

  # Add passenger
  passenger = data.Passenger(name=name, flight_id=flight_id)
  data.db.session.add(passenger)
  data.db.session.commit()
  return render_template("success.html")

@app.route("/flights")
def flights():
  """List all flights."""
  flights = data.Flight.query.all()
  return render_template("flights.html", flights=flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
  """List details about a single flight."""

  # Make sure flight exist
  flight = data.Flight.query.get(flight_id)
  if flight is None:
    return render_template("error.html", message="No such flight")

  # Get all passengers
  passengers = flight.passengers
  return render_template("flight.html", flight=flight, passengers=passengers)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000, debug=True)