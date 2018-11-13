import requests
from flask import Flask, jsonify, request
import logging
import warnings
from pymodm import connect
from pymodm import MongoModel, fields
import numpy as np
import sendgrid
import os
from sendgrid.helpers.mail import *

app = Flask(__name__)
connect('mongodb://sputney13:sputney13@ds155653.mlab.com:55653/bme590')


class Patient(MongoModel):
    patient_id = fields.IntegerField(primary_key=True)
    attending_email = fields.EmailField()
    user_age = fields.FloatField()
    heart_rate = fields.ListField(field=fields.IntegerField())
    heart_rate_time = fields.ListField(field=fields.DateTimeField())


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    r = request.get_json()
    entry = Patient(r["patient_id"], attending_email=r["attending_email"],
                    user_age=r["user_age"])
    entry.save()
    return entry, 200


if __name__ == "__main__":
    print("Run")
    entry = Patient(1, 'sarah.putney@duke.edu', 13)
    entry.save()
