from flask import Flask, jsonify, request
import logging
from pymodm import connect
from pymodm import MongoModel, fields
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
    heart_rate_time = fields.ListField()


def validate_new_patient(r):
    if all(k in r for k in ("patient_id", "attending_email", "user_age")):
        if isinstance(r["patient_id"], int) is False:
            raise TypeError("patient_id must be an integer.")
        elif "@" not in r["attending_email"]:
            raise TypeError("attending_email must be an email string.")
        elif isinstance(r["user_age"], float) is False:
            raise TypeError("user_age must be a float.")
    else:
        raise AttributeError("Post must be dict with patient_id,"
                             " attending_email, and user_age keys.")


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    r = request.get_json()
    validate_new_patient(r)
    entry = Patient(r["patient_id"], attending_email=r["attending_email"],
                    user_age=r["user_age"])
    entry.save()
    return "Posted", 200


def validate_heart_rate(r):
    if all(k in r for k in ("patient_id", "heart_rate")):
        if isinstance(r["patient_id"], int) is False:
            raise TypeError("patient_id must be an integer.")
        elif isinstance(r["heart_rate"], int) is False:
            raise TypeError("heart_rate must be an integer.")
    else:
        raise AttributeError("Post must be dict with patient_id and"
                             " heart_rate keys.")


@app.route("/api/heart_rate", methods={"POST"})
def heart_rate():
    r = request.get_json()
    validate_heart_rate(r)
    heart_rate_time_now = str(datetime.now())
    patient = Patient.objects.raw({"_id": r["patient_id"]}).first()
    patient_age = patient.user_age
    patient.heart_rate.append(r["heart_rate"])
    patient.heart_rate_time.append(heart_rate_time_now)
    patient.save()
    tachycardic_status = tachycardia(patient_age, r["heart_rate"])
    return tachycardic_status


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


@app.route("/api/status/<patient_id>", methods=["GET"])
def status_patient_id(patient_id):
    patient_id = int(patient_id)
    patient = Patient.objects.raw({"_id": patient_id}).first()
    patient_age = patient.user_age
    patient_heart_rate = patient.heart_rate[-1]
    patient_time = patient.heart_rate_time[-1]
    tachycardic_status = tachycardia(patient_age, patient_heart_rate)
    patient_status = {
        "patient_id": patient_id,
        "status": tachycardic_status,
        "status_time": patient_time
    }
    return jsonify(patient_status)


@app.route("/api/heart_rate/<patient_id>", methods={"GET"})
def heart_rate_patient_id(patient_id):
    patient_id = int(patient_id)
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
    patient_id = int(patient_id)
    patient = Patient.objects.raw({"_id": patient_id}).first()
    past_heart_rates = patient.heart_rate
    average = sum(past_heart_rates) / len(past_heart_rates)
    hr_average = {
        "patient_id": patient_id,
        "average_heart_rate": average
    }
    return jsonify(hr_average)


def validate_heart_rate_interval_average(r):
    if all(k in r for k in ("patient_id", "heart_rate_average_since")):
        if isinstance(r["patient_id"], int) is False:
            raise TypeError("patient_id must be an integer.")
        elif isinstance(r["heart_rate_average_since"], str) is False:
            raise TypeError("heart_rate_average_since must be a time string.")
        try:
            datetime.strptime(r["heart_rate_average_since"],
                              "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            raise ValueError("Time string must have format"
                             " %Y-%m-%d %H:%M:%S.%f.")
    else:
        raise AttributeError("Post must be dict with patient_id and"
                             " heart_rate_average_since keys.")


def time_string_index(past_rate_times, date_string):
    try:
        time_index = past_rate_times.index(date_string)
    except ValueError:
        raise ValueError("Heart rate data was not taken at this time,"
                         " enter a valid time.")
    return time_index


@app.route("/api/heart_rate/interval_average", methods={"POST"})
def heart_rate_interval_average():
    r = request.get_json()
    validate_heart_rate_interval_average(r)
    patient = Patient.objects.raw({"_id": r["patient_id"]}).first()
    past_rate_times = patient.heart_rate_time
    time_index = time_string_index(past_rate_times,
                                   r["heart_rate_average_since"])
    past_heart_rates = patient.heart_rate[time_index:-1]
    interval_average = str(sum(past_heart_rates) / len(past_heart_rates))
    return interval_average, 200


if __name__ == "__main__":
    app.run(host="127.0.0.1")
