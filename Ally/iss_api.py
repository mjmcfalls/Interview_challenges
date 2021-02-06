#! /usr/local/bin/python

import requests
import argparse
from datetime import datetime

api_uri = "http://api.open-notify.org/"
class Iss:

    astro_uri = "astros.json"
    pass_times_uri = "iss-pass.json?lat=LAT&lon=LON"
    current_location_uri = "iss-now.json"

    def __init__(self, uri):
        self.uri = uri
    
    def get_pass(self, latitude, longitude):
        uri = "{}{}".format(self.uri, self.pass_times_uri.replace("LAT", latitude).replace("LON", longitude))
        response = requests.get(uri)
        return response.json()

    def get_location(self):
        uri = "{}{}".format(self.uri, self.current_location_uri)
        response = requests.get(uri)
        return response.json()

    def get_people(self):
        print("Get_people function")
        
    def display_pass_info(self, data):
        if "response" in data:
            print("The ISS will be overhead {latitude}, {longitude} at {time} for {duration} seconds.".format(latitude=data['request']['latitude'], longitude=data['request']['longitude'], time=self.convert_epoch_to_string(data['response'][0]['risetime']), duration=data['response'][0]["duration"]))
        else:
            print("{}".format(data['reason']))
    def display_current_location(self, data):
        if 'iss_position' in data:
            print("The ISS current location at {time} is {latitude}, {longitude}.".format(time=self.convert_epoch_to_string(data['timestamp']), latitude=data['iss_position']['latitude'], longitude=data['iss_position']['longitude']))
        else:
            print('Something unexpected happened!')
    
    def display_current_people(self, data):
        pass

    
    def convert_epoch_to_string(self, epochtime):
        return datetime.fromtimestamp(epochtime).strftime('%Y-%m-%d %H:%M:%S')

    

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-pass", "--passing", required=False, help="When passing", action='store_true')
    parser.add_argument("-loc", "--location", required=False, help="current location of iss", action='store_true')
    parser.add_argument("-p", "--people", required=False, help="Get details of current crew", action='store_true')
    parser.add_argument("-lat", "--latitude", required=False, help="Latitude for when passing")
    parser.add_argument("-long", "--longitude", required=False, help="Longitude for when passing")
    args = parser.parse_args()
    # 
    if args.passing and (args.latitude is None or args.longitude is None):
        parser.error("--passing requires --latitude and --longitude")

    return vars(args)

def main(passing, location, people, latitude, longitude):
    # Initialize class with api_url
    iss = Iss(uri=api_uri)
    # Process command line parameters to determine next action.
    # if passing is set to true, then display when ISS will pass over the specifed latitude/longitude.
    if passing:
        iss.display_pass_info(data=iss.get_pass(latitude=latitude, longitude=longitude))
    elif location:
        # if location is true, then get the current ISS location, and pass the data to print_current_location to display location on the console.
        iss.display_current_location(iss.get_location())
    elif people:
        # if people is true, then get the current people on the ISS, and display information about the people.
        iss.get_people()


if __name__ == "__main__":
    # 
    arguments = parse_arguments()
    # Pass command line parameters into main function by key
    main(**arguments)