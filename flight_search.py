import requests
import datetime
import os
from pprint import pprint

flight_endpoints = "https://tequila-api.kiwi.com"
KIWI_API = os.environ['KIWI']

from flight_data import FlightData

class FlightSearch:

    #This class is responsible for talking to the Flight Search API.
    def get_destination_code(self, city_name):
        header = {
            "apikey": KIWI_API,
        }

        params = {
            "term": city_name,
            "location_types": "city"
        }

        response = requests.get(url=f"{flight_endpoints}/locations/query", headers=header, params=params)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code
        #result = response.json()
        #print(result)
        #code = result["city_name"]["term"]
        #return code

    def get_direct_flight(self, destination_iata_code, origin_iata_code, from_time, to_time):
        header = {
            "apikey" : KIWI_API
        }
        params = {
            "fly_from" : origin_iata_code,
            "fly_to" : destination_iata_code,
            #"date_from" : datetime.datetime.now().strftime("%d/%m/%Y"),
            #"date_to" : (datetime.datetime.now() + datetime.timedelta(days=180)).strftime("%d/%m/%Y"),
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "curr" : "GBP",
            "max_stopovers" : 0
        }
        response = requests.get(url=f"{flight_endpoints}/search", headers=header, params=params)
        try:
            result = response.json()["data"][0]
        except IndexError:
            params["max_stopovers"] = 1
            response = requests.get(url=f"{flight_endpoints}/search", headers=header, params=params)
            result = response.json()["data"][0]

            try:
                test = result["route"][0]["local_departure"].split("T")[0],
            except:
                test = "N/A"

            try:
                test_2 = result["route"][2]["local_departure"].split("T")[0],
            except:
                test_2 = "N/A"

            pprint(result)
            flight_data = FlightData(
                price=result["price"],
                origin_city=result["route"][0]["cityFrom"],
                origin_airport=result["route"][0]["flyFrom"],
                destination_city=result["route"][1]["cityTo"],
                destination_airport=result["route"][1]["flyTo"],
                out_date=test,
                return_date=test_2,
                stop_overs = 1,
                via_city=result["route"][0]["cityTo"],
            )
            #print(f"No flights found for {destination_iata_code}.")
            return flight_data
        else:

            try:
                test = result["route"][0]["local_departure"].split("T")[0],
            except:
                test = "N/A"

            try:
                test_2 = result["route"][2]["local_departure"].split("T")[0],
            except:
                test_2 = "N/A"

            flight_data = FlightData(
                price=result["price"],
                origin_city=result["route"][0]["cityFrom"],
                origin_airport=result["route"][0]["flyFrom"],
                destination_city=result["route"][0]["cityTo"],
                destination_airport=result["route"][0]["flyTo"],
                out_date=test,
                return_date=test_2,
            )
            print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data
