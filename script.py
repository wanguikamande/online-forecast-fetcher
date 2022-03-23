import configparser
import os
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
uri = os.environ.get("DB_URI")
user = os.environ.get("DB_USERNAME")
password = os.environ.get("DB_PASSWORD")
auth = os.environ.get("DB_AUTH")
mechanism = os.environ.get("DB_MECHANISM")


# Connect to Mongo client
client = MongoClient(
    uri, username=user, password=password, authSource=auth, authMechanism=mechanism
)

config = configparser.ConfigParser()
config.read("config.ini")

the_date = configparser.ConfigParser()
the_date.read("date.ini")

# locations
locations = {"q": ["nanyuki", "naivasha"], "accu": ["225705", "225702"]}

# parameters to remove afterwards
to_pop = ["cycle", "db", "coll", "loc", "base_url"]

date_today = datetime.now()
today = date_today.strftime("%Y-%m-%d")

# Get the cycles to run, i.e the ones whose date matches the date today
cycles = ["0"]

for each_section in the_date.sections():
    the_dates = dict(the_date.items(each_section))
    specific = None

    for key, value in the_dates.items():
        if value == today:
            cycles.append(key)

            print(f"Before: {the_date[each_section][key]}")
            the_date[each_section][key] = (
                date_today + timedelta(days=int(key))
            ).strftime("%Y-%m-%d")
            with open("date.ini", "w") as configfile:
                the_date.write(configfile)
            print(f"After: {the_date[each_section][key]}")


def generate_link(links):
    # Get base url and remove from parameters
    base_url = links.pop("base_url")

    # Get location and remove from parameters
    location_param = links.pop("loc")

    # Get the collection
    prefix = links.pop("coll")

    if location_param in locations.keys():
        coll = None
        for location in locations[location_param]:
            if location_param == "q":
                links.update({location_param: location})
            elif location_param == "accu":
                base_url = base_url.replace("***", location)

            # Collection post fix
            coll = f"{prefix}{location}"
            fetch(base_url, links, coll)
    else:
        print("not found")


def fetch(url, params, coll):
    db = "Weather-Data"
    response = requests.get(url, params=params)
    print({response.url})
    data = response.json()
    database = client[db]
    table = database[coll]
    obs = len(data)

    try:
        table.insert_one(data)
        print("Table: " + coll + " | Objects: " + str(obs) + " ::: SUCCESS\n")
    except TypeError:
        table.insert_many(data)
        print("Table: " + coll + " | Objects: " + str(obs) + " ::: SUCCESS\n")


for each_section in config.sections():
    params = dict(config.items(each_section))

    # Get the cycle and update its 'date' parameter
    if params["cycle"] in cycles:
        thecycle = params["cycle"]

        if "date" in params:
            config[each_section]["date"] = today
        elif "dt" in params:
            config[each_section]["dt"] = today

        with open("config.ini", "w") as configfile:
            config.write(configfile)
        del params["cycle"]
        generate_link(params)
    else:
        continue
