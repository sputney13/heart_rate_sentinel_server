# heart_rate_sentinel_server [![Build Status](https://travis-ci.org/sputney13/heart_rate_sentinel_server.svg?branch=master)](https://travis-ci.org/sputney13/heart_rate_sentinel_server)
Heart Rate Sentinel Server Project for BME590: Medical Device Software Design.

### hrss.py
The server code is located in hrss.py. The server is currently running at **vcm-7192.vm.duke.edu:5000**. However, this server is running using my SendGrid API Key. To update with a different API key (strongly recommended, as my API key often throws 401 errors), insert a different API key string into line 13 in hrss.py:
```python
SENDGRID_API_KEY = 'SENDGRID_API_KEY'
```
Then, uncomment lines 141-143 in `heart_rate` (commented out on GitHub) which call upon `send_attending_email` to send an email when a tachycardic heart rate is posted, and run hrss.py to the server again to update.

To run hrss.py on a different server, change the `host` address in line 360.

### hrss_test_client.py
This file contains a client to make `POST` and `GET` requests to all the functionalities included in hrss.py. Example executions are included in the file under `if __name__ == "__main__"`.

Note that, at this time, `POST /api/heart_rate/interval_average` only allows users to post times at which heart rate data was taken to calculate the heart rate average since that time. It is recommended that users `GET` these times from `/api/heart_rate/<patient_id>` and then select a time from the resultant timestamp list to use in their `POST`.

If running hrss.py on a different server, change the `api_host` string in line 3 to the appropriate host name and port.
