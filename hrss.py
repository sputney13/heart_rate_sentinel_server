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

logging.basicConfig(filename="hrss.log", filemode='w', level=logging.INFO)


class Patient(MongoModel):
    patient_id = fields.IntegerField(primary_key=True)
    attending_email = fields.EmailField()
    user_age = fields.FloatField()
    heart_rate = fields.ListField(field=fields.IntegerField())
    heart_rate_time = fields.ListField()


def validate_new_patient(r):
    """ Validates user inputs for posts to /api/new_patient

    Args:
        r: dictionary containing (at minimum) patient_id, attending_email,
           and user_age keys for posting to database

    Returns:
        AttributeError: when r does not contain the 3 required keys
        TypeError: when the patient_id is not an integer, the attending_email
                   is not an email string, or the user_age is not a float

    """
    if all(k in r for k in ("patient_id", "attending_email", "user_age")):
        if isinstance(r["patient_id"], int) is False:
            logging.exception("TypeError: patient_id not integer.")
            raise TypeError("patient_id must be an integer.")
        elif "@" not in r["attending_email"]:
            logging.exception("TypeError: attending_email not email string.")
            raise TypeError("attending_email must be an email string.")
        elif isinstance(r["user_age"], float) is False:
            logging.exception("TypeError: user_age not float.")
            raise TypeError("user_age must be a float.")
    else:
        logging.exception("AttributeError: Post does not have proper keys.")
        raise AttributeError("Post must be dict with patient_id,"
                             " attending_email, and user_age keys.")
    logging.info("Passed new patient POST validation.")


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    """ POSTS new patient information

    Posts new patient information containing patient_id (int), attending_email
    (email string), and user_age (int) to MongoDB database.

    Returns:
        200 Status after posting has occurred.

    """
    r = request.get_json()
    validate_new_patient(r)
    entry = Patient(r["patient_id"], attending_email=r["attending_email"],
                    user_age=r["user_age"])
    entry.save()
    logging.info("New patient information posted to database.")
    return "Posted", 200


def validate_heart_rate(r):
    """ Validates user inputs for posts to /api/heart_rate

    Args:
        r: dictionary containing (at minimum) patient_id and heart
           rate for posting to database

    Returns:
        AttributeError: when r does not contain the 2 required keys
        TypeError: when the patient_id or the heart rate is not an integer

    """
    if all(k in r for k in ("patient_id", "heart_rate")):
        if isinstance(r["patient_id"], int) is False:
            logging.exception("TypeError: patient_id not integer.")
            raise TypeError("patient_id must be an integer.")
        elif isinstance(r["heart_rate"], int) is False:
            logging.exception("TypeError: heart rate not integer.")
            raise TypeError("heart_rate must be an integer.")
    else:
        logging.exception("AttributeError: Post does not have proper keys.")
        raise AttributeError("Post must be dict with patient_id and"
                             " heart_rate keys.")
    logging.info("Passed heart rate POST validation.")


def send_attending_email(attending_email, patient_id):
    patient_id = str(patient_id)
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("sep52@duke.edu")
    to_email = Email(attending_email)
    subject = "WARNING: Tachycardic Patient"
    content = Content("text/plain", "Patient ID " + patient_id + " displayed "
                                                                 "a "
                                                                 "tachycardic"
                                                                 " heart "
                                                                 "rate.")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    logging.info("Sent tachycardia warning email to attending.")
    return str(response)


@app.route("/api/heart_rate", methods={"POST"})
def heart_rate():
    """ POSTS new patient heart rate information

    Posts new heart rate information containing patient_id (int) and heart
    rate (int) to MongoDB database.

    Returns:
        tachycardic_status = string containing patient tachycardia status
        200 Status after posting has occurred.

    """
    r = request.get_json()
    validate_heart_rate(r)
    heart_rate_time_now = str(datetime.now())
    patient = Patient.objects.raw({"_id": r["patient_id"]}).first()
    patient_age = patient.user_age
    attending_email = patient.attending_email
    patient.heart_rate.append(r["heart_rate"])
    patient.heart_rate_time.append(heart_rate_time_now)
    patient.save()
    logging.info("New heart rate posted to database.")
    tachycardic_status = tachycardia(patient_age, r["heart_rate"])
    if tachycardic_status is "tachycardic":
        send_attending_email(attending_email, r["patient_id"])
    return tachycardic_status, 200


def tachycardia(patient_age, patient_heart_rate):
    """ Determines if patient is tachycardic based on their age and heart rate

    Args:
        patient_age: integer extracted from patient database entry
        patient_heart_rate: integer posted to patient database entry

    Returns:
        tachycardic_status: string containing either "tachycardic" or
                            "not tachycardic"

    """
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
    logging.info("Tachycardic status calculated: " + tachycardic_status)
    return tachycardic_status


def find_tachycardic_status(patient_id):
    """ Determines if patient's most recent heart rate entry is tachycardic

    Args:
        patient_id: int representing patient's id number

    Returns:
         patient_time: time of most recent heart rate entry in patient db
         tachycardic_status: string containing "tachycardic" or "not
                             tachycardic" based on most recent entry

    """
    patient_id = int(patient_id)
    patient = Patient.objects.raw({"_id": patient_id}).first()
    patient_age = patient.user_age
    patient_heart_rate = patient.heart_rate[-1]
    patient_time = patient.heart_rate_time[-1]
    tachycardic_status = tachycardia(patient_age, patient_heart_rate)
    return patient_time, tachycardic_status


@app.route("/api/status/<patient_id>", methods=["GET"])
def status_patient_id(patient_id):
    """ GETs most recent tachycardia status for specified patient

    Args:
        patient_id: int representing patient's id number

    Returns:
        patient_status: json containing patient id, time of most recent
                        heart rate entry, and tachycardic status of that entry

    """
    patient_time, tachycardic_status = find_tachycardic_status(patient_id)
    patient_status = {
        "patient_id": patient_id,
        "status": tachycardic_status,
        "status_time": patient_time
    }
    logging.info("Patient tachycardic status retrieved.")
    return jsonify(patient_status)


@app.route("/api/heart_rate/<patient_id>", methods={"GET"})
def heart_rate_patient_id(patient_id):
    """ GETs all stored heart rates/time stamps for specified patient

    Args:
        patient_id: int representing patient's id number

    Returns:
        heart_rates: json containing patient id and all stored heart rates and
                     associated time stamps for that patient

    """
    patient_id = int(patient_id)
    patient = Patient.objects.raw({"_id": patient_id}).first()
    past_heart_rates = patient.heart_rate
    past_rate_times = patient.heart_rate_time
    heart_rates = {
        "patient_id": patient_id,
        "stored_heart_rates": past_heart_rates,
        "stored_heart_rate_times": past_rate_times
    }
    logging.info("Patient heart rate data retrieved.")
    return jsonify(heart_rates)


@app.route("/api/heart_rate/average/<patient_id>", methods={"GET"})
def heart_rate_average(patient_id):
    """ GETs average heart rate over all entries for specified patient

    Args:
         patient_id: int representing patient's id number

    Returns:
        hr_average: json containing patient id and average heart rate
                    over all heart rate entries for specified patient

    """
    patient_id = int(patient_id)
    patient = Patient.objects.raw({"_id": patient_id}).first()
    past_heart_rates = patient.heart_rate
    average = sum(past_heart_rates) / len(past_heart_rates)
    hr_average = {
        "patient_id": patient_id,
        "average_heart_rate": average
    }
    logging.info("Patient heart rate average calculated: " + str(average))
    return jsonify(hr_average)


def validate_heart_rate_interval_average(r):
    """ Validates user inputs for posts to /api/heart_rate/interval_average

    Args:
        r: dictionary containing patient_id and heart_rate_average_since keys

    Returns:
         AttributeError: when r does not contain the 2 specified keys
         TypeError: when patient_id is not an integer or
                    heart_rate_average_since is not a string
         ValueError: when the time string in heart_rate_average_since
                     is not in the proper datetime format

    """
    if all(k in r for k in ("patient_id", "heart_rate_average_since")):
        if isinstance(r["patient_id"], int) is False:
            logging.exception("TypeError: patient_id not integer.")
            raise TypeError("patient_id must be an integer.")
        elif isinstance(r["heart_rate_average_since"], str) is False:
            logging.exception("TypeError: time stamp entered not string.")
            raise TypeError("heart_rate_average_since must be a time string.")
        try:
            datetime.strptime(r["heart_rate_average_since"],
                              "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            logging.exception("ValueError: time string in wrong format")
            raise ValueError("Time string must have format"
                             " %Y-%m-%d %H:%M:%S.%f.")
    else:
        logging.exception("AttributeError: Post does not have proper keys.")
        raise AttributeError("Post must be dict with patient_id and"
                             " heart_rate_average_since keys.")
    logging.info("Passed heart rate interval average POST validation.")


def time_string_index(past_rate_times, date_string):
    """ Iterates through list of times to find index of specified time

    Args:
        past_rate_times: list of heart rate timestamps
        date_string: user-specified time to find in list of timestamps

    Returns:
        ValueError: when date_string is not included in past_rate_times
        time_index: index in past_rate_times at which date_string occurs

    """
    try:
        time_index = past_rate_times.index(date_string)
    except ValueError:
        logging.exception("ValueError: time string entered not in database.")
        raise ValueError("Heart rate data was not taken at this time,"
                         " enter a valid time.")
    return time_index


@app.route("/api/heart_rate/interval_average", methods={"POST"})
def heart_rate_interval_average():
    """ Calculates heart rate average since a user-specified time

        Returns:
            interval_average = average heart rate since specified time
            200 Status after posting has occurred

    """
    r = request.get_json()
    validate_heart_rate_interval_average(r)
    patient = Patient.objects.raw({"_id": r["patient_id"]}).first()
    past_rate_times = patient.heart_rate_time
    time_index = time_string_index(past_rate_times,
                                   r["heart_rate_average_since"])
    past_heart_rates = patient.heart_rate[time_index:-1]
    interval_average = str(sum(past_heart_rates) / len(past_heart_rates))
    logging.info("Heart rate interval average calculated: " +
                 interval_average + ' bpm')
    return interval_average, 200


if __name__ == "__main__":
    app.run(host="127.0.0.1")
