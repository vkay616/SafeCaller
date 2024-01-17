import csv
import json
import requests
import os
import sys
import logging

# setting up a logger to log all requests and their responses
LOGPATH = os.getcwd() + "/data_population/log"

if not os.path.exists(LOGPATH):
    os.mkdir(LOGPATH)

log = logging.getLogger("")
log.setLevel(logging.INFO)
format = logging.Formatter("%(levelname)s - %(message)s")

log_file = os.path.join(LOGPATH, "response.log")

if os.path.exists(log_file):
    open(log_file, "w").close()

logging.basicConfig(
    filename=os.path.join(LOGPATH, "response.log"),
    filemode="a",
    format="- %(message)s",
)

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)


USER_CREDENTIALS = {
    "number": "9150426159",
    "hashed_password": "iloveanime123"
}


LOGIN_URL = "http://127.0.0.1:8000/api/login/"
REGISTER_URL = "http://127.0.0.1:8000/api/register/"
REPORT_URL = "http://127.0.0.1:8000/api/report/"

headers = {"content-type": "application/json; charset=UTF-8"}


response = requests.post(LOGIN_URL, headers=headers,
                         data=json.dumps(USER_CREDENTIALS))
print(f"Response Code: {response.status_code}")
print(json.dumps(json.loads(response.text), indent=2))

with open("data_population/sample_data.csv", "r") as f:
    reader = csv.DictReader(f)

    for record in reader:
        logging.info(f"POST {json.dumps(record, indent=2)}")
        logging.info("")
        response = requests.post(
            REGISTER_URL, headers=headers, data=json.dumps(record))
        logging.info(f"Response Code: {response.status_code}")
        logging.info(json.dumps(json.loads(response.text), indent=2))
