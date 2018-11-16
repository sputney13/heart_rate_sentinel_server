# heart_rate_sentinel_server [![Build Status](https://travis-ci.org/sputney13/heart_rate_sentinel_server.svg?branch=master)](https://travis-ci.org/sputney13/heart_rate_sentinel_server)
Heart Rate Sentinel Server Project for BME590: Medical Device Software Design.

### hrss.py
The server code is located in hrss.py. The server is currently running at **vcm-7192.vm.duke.edu:5000**. It should work on all accounts (SendGrid API included) except for the following:

**Note that for some reason, the server vcm-7192.vm.duke.edu:5000 has not been running proper `POST` requests for `/api/heart_rate/interval_average` (throwing 500 errors). The code works when the host is 127.0.0.1:5000, but not on the virtual machine, so I would recommend leaving the host in line 360 of hrss.py set to the 127.0.0.1 address.*

### hrss_test_client.py
This file contains a client to make `POST` and `GET` requests to all the functionalities included in hrss.py. Example executions are included in the file under `if __name__ == "__main__"`.

Note that, at this time, `POST /api/heart_rate/interval_average` only allows users to post times at which heart rate data was taken to calculate the heart rate average since that time. It is recommended that users `GET` these times from `/api/heart_rate/<patient_id>` and then select a time from the resultant timestamp list to use in their `POST`.

If running hrss.py on a different server, change the `api_host` string in line 3 to the appropriate host name and port. It is currently set to the vcm server listed above, although this server address has the noted issue with the final `POST` request.
