import os
from flask import Flask, request, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

database_url = os.environ.get('DATABASE_URL')
engine = create_engine(database_url)
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
  flights = db.execute("SELECT * FROM flights").fetchall()

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
  if db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).rowcount == 0:
    return render_template("error.html", message="No such flight with that id.",)
  db.execute("INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id)",
              {"name": name, "flight_id": flight_id})
  db.commit() 
  return render_template("success.html")

@app.route("/flights")
def flights():
  """List all flights."""
  flights = db.execute("SELECT * FROM flights").fetchall()
  return render_template("flights.html", flights=flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
  """List details about a sigle flight."""

  #Make sure flight exist
  flight = db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).fetchone()
  if flight is None:
    return render_template("error.html", message="No such flight.")

  # Get all passengers
  passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
                          {"flight_id": flight_id}).fetchall()
  return render_template("flight.html", flight=flight, passengers=passengers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)