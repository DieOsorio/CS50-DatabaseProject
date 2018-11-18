import os

from flask import Flask, render_template, request
import models


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
models.db.init_app(app)

def main():
  models.db.create_all()

if __name__ == "__main__":
  with app.app_context():
    main()