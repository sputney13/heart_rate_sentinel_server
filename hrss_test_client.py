import requests

api_host = "http://vcm-7129.vm.duke.edu:5000"


def post_new_patient(patient_id, attending_email, user_age):
    """ Makes new patient POST request to /api/new_patient

    Args:
        patient_id: integer representing patient ID number
        attending_email: string containing patient attending's email
        user_age: integer representing patient's age

    Returns:
         r: the status of the post request (200 if completed)

    """
    data = {
        "patient_id": patient_id,
        "attending_email": attending_email,
        "user_age": user_age
    }
    r = requests.post(api_host + '/api/new_patient', json=data)
    return r


def post_heart_rate(patient_id, heart_rate):
    """ Makes new heart rate data POST request to /api/heart_rate

    Args:
        patient_id: integer representing patient ID number
        heart_rate: integer representing recent patient heart rate

    Returns:
         r: the status of the post request (200 if completed)

    """
    data = {
        "patient_id": patient_id,
        "heart_rate": heart_rate
    }
    r = requests.post(api_host + '/api/heart_rate', json=data)
    return r


def get_status_patient_id(patient_id):
    """ Makes GET request to api/status/<patient_id>

    Args:
        patient_id: int representing patient's ID number

    Returns:
         patient_status: json containing patient ID, tachycardia status,
                         and the time the status was calculated

    """
    website = api_host + '/api/status/' + str(patient_id)
    r = requests.get(website)
    patient_status = r.json()
    return patient_status


def get_heart_rate_patient_id(patient_id):
    """ Makes GET request to api/heart_rate/<patient_id>

    Args:
        patient_id: int representing patient's ID number

    Returns:
        hr_list: json containing patient ID, a list of all heart rates stored
                 for the patient, and a list of all the heart rate timestamps

    """
    website = api_host + '/api/heart_rate/' + str(patient_id)
    r = requests.get(website)
    hr_list = r.json()
    return hr_list


def get_heart_rate_average(patient_id):
    """ Makes GET request to api/heart_rate_average/<patient_id>

    Args:
        patient_id: int representing patient's ID number

    Returns:
        hr_average: json containing patient ID and the average of all stored
                    heart rate data for the patient

    """
    website = api_host + '/api/heart_rate/average/' + str(patient_id)
    r = requests.get(website)
    hr_average = r.json()
    return hr_average


def post_heart_rate_interval_average(patient_id, heart_rate_average_since):
    """ Makes new POST request to /api/heart_rate/interval_average

    Args:
        patient_id: integer representing patient ID number
        heart_rate_average_since: string containing time user wants to
                                  calculate heart rage average after

    Returns:
        r: the status of the post request (200 if completed)

    """
    data = {
        "patient_id": patient_id,
        "heart_rate_average_since": heart_rate_average_since
    }
    r = requests.post(api_host + '/api/heart_rate/interval_average',
                      json=data)
    return r


if __name__ == "__main__":
    # Example Execution for post_new_patient
    post1 = post_new_patient(3, "sarah.putney@duke.edu", 1.4)
    print(post1)
    # Example Execution for post_heart_rate
    post2 = post_heart_rate(3, 178)
    print(post2)
    # Example Execution for get_status_patient_id
    patient_status = get_status_patient_id(3)
    print(patient_status)
    # Example Execution for get_heart_rate_patient_id
    hr_list = get_heart_rate_patient_id(3)
    print(hr_list)
    # Example Execution for get_heart_rate_average
    hr_average = get_heart_rate_average(3)
    print(hr_average)
    # Example Execution for post_heart_rate_interval_average
    post3 = post_heart_rate_interval_average(1, "2018-11-16 01:19:29.168676")
    print(post3)
