import pytest
import hrss
from datetime import datetime


def test_validate_new_patient():
    r1 = {"patient_id": 2}
    r2 = {"patient_id": 'a', "attending_email":
          "sarah.putney@duke.edu", "user_age": 13}
    r3 = {"patient_id": 1, "attending_email": "sarah putney", "user_age": 13}
    r4 = {"patient_id": 1, "attending_email":
          "sarah.putney@duke.edu", "user_age": "13"}

    with pytest.raises(AttributeError):
        hrss.validate_new_patient(r1)
    with pytest.raises(TypeError):
        hrss.validate_new_patient(r2)
    with pytest.raises(TypeError):
        hrss.validate_new_patient(r3)
    with pytest.raises(TypeError):
        hrss.validate_new_patient(r4)


def test_validate_heart_rate():
    r1 = {"heart_rate": 137}
    r2 = {"patient_id": 4.4, "heart_rate": 177}
    r3 = {"patient_id": 4, "heart_rate": "176"}

    with pytest.raises(AttributeError):
        hrss.validate_heart_rate(r1)
    with pytest.raises(TypeError):
        hrss.validate_heart_rate(r2)
    with pytest.raises(TypeError):
        hrss.validate_heart_rate(r3)


@pytest.mark.parametrize("a,b,expected", [
    (.001, 161, "tachycardic"),
    (.01, 170, "tachycardic"),
    (.07, 183, "tachycardic"),
    (.1, 180, "tachycardic"),
    (.3, 187, "tachycardic"),
    (.75, 170, "tachycardic"),
    (2, 152, "tachycardic"),
    (4, 138, "tachycardic"),
    (6, 134, "tachycardic"),
    (10, 131, "tachycardic"),
    (14, 120, "tachycardic"),
    (16, 110, "tachycardic"),
    (16, 98, "not tachycardic")
])
def test_tachycardia(a, b, expected):
    assert hrss.tachycardia(a, b) == expected


def test_find_tachycardic_status():
    patient = hrss.Patient(4, attending_email="sarah.putney@duke.edu",
                           user_age=90, heart_rate=[101],
                           heart_rate_time=[str(datetime.now())])
    patient.save()
    patient_time, tachycardic_status = hrss.find_tachycardic_status(4)

    assert type(patient_time) == str
    assert tachycardic_status == "tachycardic"


def test_validate_heart_rate_interval_average():
    r1 = {"patient_id": 2}
    r2 = {"patient_id": 'a', "heart_rate_average_since":
          "2018-11-16 01:19:29.168676"}
    r3 = {"patient_id": 1, "heart_rate_average_since": 2018}
    r4 = {"patient_id": 1, "heart_rate_average_since":
          "11-16-2018 1:19:29.168676"}

    with pytest.raises(AttributeError):
        hrss.validate_heart_rate_interval_average(r1)
    with pytest.raises(TypeError):
        hrss.validate_heart_rate_interval_average(r2)
    with pytest.raises(TypeError):
        hrss.validate_heart_rate_interval_average(r3)
    with pytest.raises(ValueError):
        hrss.validate_heart_rate_interval_average(r4)


def test_time_string_index():
    past_rate_times = ["2018-11-16 01:19:29.168676",
                       "2018-11-16 02:11:56.702286",
                       "2018-11-16 02:20:16.136095"]
    date_string1 = "2018-11-15 00:13:46.703386"
    date_string2 = "2018-11-16 02:11:56.702286"

    with pytest.raises(ValueError):
        hrss.time_string_index(past_rate_times, date_string1)

    time_index = hrss.time_string_index(past_rate_times, date_string2)
    assert time_index == 1
