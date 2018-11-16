import requests


def post_new_patient(patient_id, attending_email, user_age):
    data = {
        "patient_id": patient_id,
        "attending_email": attending_email,
        "user_age": user_age
    }
    r = requests.post('http://127.0.0.1:5000/api/new_patient', json=data)
    return r


def post_heart_rate(patient_id, heart_rate):
    data = {
        "patient_id": patient_id,
        "heart_rate": heart_rate
    }
    r = requests.post('http://127.0.0.1:5000/api/heart_rate', json=data)
    return r


def get_status_patient_id(patient_id):
    website = 'http://127.0.0.1:5000/api/status/' + str(patient_id)
    r = requests.get(website)
    patient_status = r.json()
    return patient_status


def get_heart_rate_patient_id(patient_id):
    website = 'http://127.0.0.1:5000/api/heart_rate/' + str(patient_id)
    r = requests.get(website)
    hr_list = r.json()
    return hr_list


def get_heart_rate_average(patient_id):
    website = 'http://127.0.0.1:5000/api/heart_rate/average/' + str(patient_id)
    r = requests.get(website)
    hr_average = r.json()
    return hr_average


def post_heart_rate_interval_average(patient_id, heart_rate_average_since):
    data = {
        "patient_id": patient_id,
        "heart_rate_average_since": heart_rate_average_since
    }
    r = requests.post('http://127.0.0.1:5000/api/heart_rate/'
                      'interval_average', json=data)
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
