#! /usr/local/bin/python

import requests
import argparse

api_uri = "http://api.open-notify.org/"
class Iss:

    astro_uri = "astros.json"
    pass_times_uri = "iss-pass.json?lat=LAT&lon=LON"
    current_location_uri = "iss-now.json"
    def __init__(self, uri):
        self.uri = uri
    
    def get_pass(self, latitude, longitude):
        print("Get_pass function - lat: {}, long: {}".format(latitude, longitude))

    def get_people(self):
        print("Get_people function")

    def get_location(self):
        print("Get_location function")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-pass", "--passing", required=False, help="When passing", action='store_true')
    parser.add_argument("-loc", "--location", required=False, help="current location of iss", action='store_true')
    parser.add_argument("-p", "--people", required=False, help="Get details of current crew", action='store_true')
    parser.add_argument("-lat", "--latitude", required=False, help="Latitude for when passing")
    parser.add_argument("-long", "--longitude", required=False, help="Longitude for when passing")
    args = parser.parse_args()
    print(args)
    if args.passing and (args.latitude is None or args.longitude is None):
        parser.error("--passing requires --latitude and --longitude")

    return vars(args)

def main(passing, location, people, latitude, longitude):
    iss = Iss(uri=api_uri)
    print(iss.uri)
    if passing:
        iss.get_pass(latitude=latitude, longitude=longitude)
        print("The ISS will be overhead {latitude}, {longitude} at {time} for {duration}".format(latitude=latitude, longitude=longitude, time="time", duration="duration"))
    elif location:
        iss.get_location()
        print("The ISS current location at {time} is {latitude}, {longitude}".format(time="time", latitude=latitude, longitude=longitude))
    elif people:
        iss.get_people()


if __name__ == "__main__":
    arguments = parse_arguments()
    print(arguments)
    # print(type(arguments))
    main(**arguments)