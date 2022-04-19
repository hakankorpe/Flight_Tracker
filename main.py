from data_manager import DataManager
from flight_data import FlightData
from pprint import pprint
from datetime import datetime, timedelta
from flight_search import FlightSearch
from notification_manager import NotificationManager

flight_search = FlightSearch()
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
mail_data = data_manager.get_mail_data()
notification_manager = NotificationManager()




if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    #print(f"sheet_data:\n {sheet_data}")
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

for row in sheet_data:
    flight = flight_search.get_direct_flight(
        row["iataCode"],
        "LON",
        from_time= (datetime.now() + timedelta(days=1)),
        to_time= (datetime.now() + timedelta(days=180)),
    )
    if flight.price < row["lowestPrice"]:

        message = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
            print(message)

        notification_manager.send_sms(message=message)

    for user in mail_data:

        msg = f"This is the Google flight link for a flight from {flight.origin_airport} to {flight.destination_airport} from {flight.out_date} to {flight.return_date}. \n https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date} *{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"

        send_msg = msg.encode('utf-8')
        notification_manager.send_emails(message=send_msg, mail=user["email"])