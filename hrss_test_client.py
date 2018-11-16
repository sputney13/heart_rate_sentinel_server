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


def get_status_patient_id():
    r = requests.get('http://127.0.0.1:5000/api/status/3')
    patient_status = r.json()
    return patient_status


def get_heart_rate_patient_id():
    r = requests.get('http://127.0.0.1:5000/api/heart_rate/3')
    hr_list = r.json()
    return hr_list


def get_heart_rate_average():
    r = requests.get('http://127.0.0.1:5000/api/heart_rate/average/3')
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
    post1 = post_new_patient(3, "sarah.putney@duke.edu", 1.4)
    post2 = post_heart_rate(3, 178)
    patient_status = get_status_patient_id()
    hr_list = get_heart_rate_patient_id()
    hr_average = get_heart_rate_average()
    post3 = post_heart_rate_interval_average(1, "2018-11-16 01:19:29.168676")
    print(post1)
    print(post2)
    print(patient_status)
    print(hr_list)
    print(hr_average)
    print(post3)
