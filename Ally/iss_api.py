#! /usr/local/bin/python

import requests
import argparse
from datetime import datetime
# Source of API and Docs: http://open-notify.org/
# Built for the Ally interview 2020-02-06
# Matthew McFalls
# Things to do:
# 1. The get functions in the class could be rewritten into a single function to reduce the duplicate code.
# 2. The display functions could be rewritten into a single function too. There is some duplicate code that could be condensed.
# 3. Consider passing the parameters into main() kwargs.  For the limited number of parameters and options, probably not necessary.
# 4. Check lat/long input to validate ints or floats are entered, and fall between -90.0 and 90.0

api_uri = "http://api.open-notify.org/"

class Iss:
    # Stubs used to complete the API
    astro_uri = "astros.json"
    pass_times_uri = "iss-pass.json?lat=LAT&lon=LON"
    current_location_uri = "iss-now.json"

    # Initialize class with the base URI for the ISS API.
    def __init__(self, uri):
        self.uri = uri
    
    # Fetch when ISS will be passing over a specific latitude/longitude.  Include how long ISS will be visible,
    # and altitude.
    def get_pass(self, latitude, longitude):
        uri = "{}{}".format(self.uri, self.pass_times_uri.replace("LAT", latitude).replace("LON", longitude))
        response = requests.get(uri)
        return response.json()

    # Fetch the current location of ISS from API>
    def get_location(self):
        uri = "{}{}".format(self.uri, self.current_location_uri)
        response = requests.get(uri)
        return response.json()

    # Fetch the people on ISS from the API
    def get_people(self):
        uri = "{}{}".format(self.uri, self.astro_uri)
        response = requests.get(uri)
        return response.json()

    # Process and display when ISS will pass over a specified latitude/longitude.
    def display_pass_info(self, data):
        # Check if the response key exists in the data dictionary.  If it does exist, display information about when ISS passes over the lat/long
        # If response is missing display the reason key from the data dictionary.
        if "response" in data:
            print("The ISS will be overhead {latitude}, {longitude} at {time} for {duration} seconds.".format(latitude=data['request']['latitude'], longitude=data['request']['longitude'], time=self.convert_epoch_to_string(data['response'][0]['risetime']), duration=data['response'][0]["duration"]))
        else:
            print("{}".format(data['reason']))

    # Display the current location of the ISS.  The data parameter is the response fro get_location. 
    def display_current_location(self, data):
        # Check if the iss_position key exists.  If it does display the current latitude/longitude of ISS and the datetime of the API response.
        # If the key does not exist, print a generic error.  The API documentation does not provide a documented error.
        if 'iss_position' in data:
            print("The ISS current location at {time} is {latitude}, {longitude}.".format(time=self.convert_epoch_to_string(data['timestamp']), latitude=data['iss_position']['latitude'], longitude=data['iss_position']['longitude']))
        else:
            print('Something unexpected happened!')
    
    # Display the current people on ISS.  The data parameter is the results from get_people().
    def display_current_people(self, data):
        # Check if the message key contains success.  If so, display the number of people on ISS, then their names. 
        # If the key does not contain success, display a generic error.  
        # The API documentation did not provide documentation on what error would be returned if no data available.
        if data['message'] == 'success':
            print("There are {} people on ISS.\nThe following people are on ISS:".format(data['number']))
            [print("{}".format(person['name'], person['craft'])) for person in data['people']]
        else:
            print("Something unexpected happened!")

    # Function to convert epoch time in the JSON response to a date time string.
    def convert_epoch_to_string(self, epochtime):
        return datetime.fromtimestamp(epochtime).strftime('%Y-%m-%d %H:%M:%S')

def parse_arguments():
    # Initialize argparse Argumentparser
    parser = argparse.ArgumentParser()

    # Add arguments to the ArgumentParser
    # Set --passing, --location, --people with store_true, to suppress needing a value passed on the command line.
    parser.add_argument("-pass", "--passing", required=False, help="Display when ISS passes a specified Latitude/longitude; requires --latitude and --longitude", action='store_true')
    parser.add_argument("-loc", "--location", required=False, help="Display the current location of ISS", action='store_true')
    parser.add_argument("-p", "--people", required=False, help="Display the number of people on ISS and their names.", action='store_true')
    parser.add_argument("-lat", "--latitude", required=False, help="Latitude to predict when ISS passes over")
    parser.add_argument("-long", "--longitude", required=False, help="Longitude to predict when ISS passes over.")
    
    # Parse the arguments on the command line
    args = parser.parse_args()
    
    # Check if latitude and longitude are provided along with the passing arg; if not throw an error, then exit.
    if args.passing and (args.latitude is None or args.longitude is None):
        parser.error("--passing requires --latitude and --longitude")
    
    # Return dictionary of command line arguments
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
        iss.display_current_people(data=iss.get_people())


if __name__ == "__main__":
    # Call function to parse arugments, and return a dictionary with values of the provide arugments.
    arguments = parse_arguments()
    # Pass  the dictionary of the command line arugments into the main function by key value.
    main(**arguments)