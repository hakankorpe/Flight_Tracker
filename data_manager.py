import requests
import os

sheety_endpoints = os.environ['sheety_endpoints1']
sheety_endpoints_2 = os.environ['sheety_endpoints2']

SHEETY_USERNAME = os.environ['sheety_username']
SHEETY_PASS = os.environ['sheety_pass']

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}
        self.mail_data = {}

    def get_destination_data(self):
        response = requests.get(url=sheety_endpoints, auth=(SHEETY_USERNAME, SHEETY_PASS))
        result = response.json()
        self.destination_data = result["prices"]

        return self.destination_data


    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"],
                    "lowestPrice": city["lowestPrice"]
                }

            }
            response_2 = requests.put(
                url=f"{sheety_endpoints}/{city['id']}",
                json=new_data, auth=(SHEETY_USERNAME,SHEETY_PASS))
            print(response_2.text)


    def get_mail_data(self):
        response = requests.get(url=sheety_endpoints_2, auth=(SHEETY_USERNAME, SHEETY_PASS))
        result = response.json()
        self.mail_data = result["users"]
        print(self.mail_data)

        return self.mail_data

