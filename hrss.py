import requests
from flask import Flask, jsonify, request
import logging
import warnings
from pymodm import connect
from pymodm import MongoModel, fields
import numpy as np
from datetime import datetime
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


@app.route("/api/heart_rate", methods={"POST"})
def heart_rate():
    r = request.get_json()
    heart_rate_time_now = datetime.now()
    patient = Patient.objects.raw({"_id": r["patient_id"]}).first()
    patient.heart_rate.append(r["heart_rate"])
    patient.heart_rate_time.append(heart_rate_time_now)
    patient.save()
    return patient, 200


def tachycardia(patient_age, patient_heart_rate):
    if patient_age < .008 and patient_heart_rate > 159:
        tachycardic_status = "tachycardic"
    elif patient_age < .019 and patient_heart_rate > 166:
        tachycardic_status = "tachycardic"
    elif patient_age < .083 and patient_heart_rate > 182:
        tachycardic_status = "tachycardic"
    elif patient_age < .250 and patient_heart_rate > 179:
        tachycardic_status = "tachycardic"
    elif patient_age < .500 and patient_heart_rate > 186:
        tachycardic_status = "tachycardic"
    elif patient_age < 1 and patient_heart_rate > 169:
        tachycardic_status = "tachycardic"
    elif patient_age < 3 and patient_heart_rate > 151:
        tachycardic_status = "tachycardic"
    elif patient_age < 5 and patient_heart_rate > 137:
        tachycardic_status = "tachycardic"
    elif patient_age < 8 and patient_heart_rate > 133:
        tachycardic_status = "tachycardic"
    elif patient_age < 12 and patient_heart_rate > 130:
        tachycardic_status = "tachycardic"
    elif patient_age <= 15 and patient_heart_rate > 119:
        tachycardic_status = "tachycardic"
    elif patient_heart_rate > 100:
        tachycardic_status = "tachycardic"
    else:
        tachycardic_status = "not tachycardic"
    return tachycardic_status


def find_tachycardic_status(patient_id):
    patient = Patient.objects.raw({"_id": patient_id}).first()
    patient_age = patient.user_age
    patient_heart_rate = patient.heart_rate[-1]
    patient_time = patient.heart_rate_time[-1]
    tachycardic_status = tachycardia(patient_age, patient_heart_rate)
    return patient_time, tachycardic_status


@app.route("/api/status/<patient_id>", methods=["GET"])
def status_patient_id(patient_id):
    patient_time, tachycardic_status = find_tachycardic_status(patient_id)
    patient_status = {
        "patient_id": patient_id,
        "status": tachycardic_status,
        "status_time": patient_time
    }
    return jsonify(patient_status)


@app.route("/api/heart_rate/<patient_id>", methods={"GET"})
def heart_rate_patient_id(patient_id):
    patient = Patient.objects.raw({"_id": patient_id}).first()
    past_heart_rates = patient.heart_rate
    past_rate_times = patient.heart_rate_time
    heart_rates = {
        "patient_id": patient_id,
        "stored_heart_rates": past_heart_rates,
        "stored_heart_rate_times": past_rate_times
    }
    return jsonify(heart_rates)


@app.route("/api/heart_rate/average/<patient_id>", methods={"GET"})
def heart_rate_average(patient_id):
    patient = Patient.objects.raw({"_id": patient_id}).first()
    past_heart_rates = patient.heart_rate
    average = sum(past_heart_rates) / len(past_heart_rates)
    hr_average = {
        "patient_id": patient_id,
        "average_heart_rate": average
    }
    return jsonify(hr_average)


if __name__ == "__main__":
    print("Run")
    # entry = Patient(1, 'sarah.putney@duke.edu', 13)
    # entry.save()
