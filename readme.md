# Weather Data Scrapper

This script aids in collection of weather data from an API(s). 

## Description

It has an element of automation whereby provided the script is running (as a microservice or cron job) collection will continue until explicitly stopped.

The current script collects data from the following APIs:
* Accuweather
* WeatherAPI
* WorldWeatherOnline

The data collected is stored in a MongoDB database.

The script should run twice a day, with a 12 hour difference between both collections (i.e. 9am and 9pm etc). This is because Accuweather provides 12hr forecasts hence to collect a full day's forecast (24hrs), data would be collected twice every 24 hours. 

### Ini Files
There are two ini files in the repo:
* [config.ini](config.ini)
    * API parameters are stored here together with other additional parameters such as *cycle* that keeps track of how often collect data from a API and *coll* that indicated the prefix of the table/collection name.
* [date.ini](date.ini)
    * Keeps track of the last time data was collected from an API. The entries here are tied to the *cycle* entry in the config.ini file. For instance, if the *cycle* is 5 [collection is done every 5 days], the script adjust the date entry for '5' to the next 5<sup>th</sup> day for the next collection.

### Adding Or Updating An API
To add a new API or update values of an already existing API, edit the [config.ini](config.ini). 


### Adding Or Updating A Location
Each API has it's own way of referencing a location. Accuweather has a number system while WorldWeatherOnline and WeatherAPI use the location name i.e. 'Nanyuki' or 'Naivasha'. A key for this has been added to the [config.ini](config.ini) file depicted as **'loc'**.  
In [script.py](script.py), there is a dictionary of lists called **'location'** that keeps track of all the locations.  
* To add a new location with the existing keys, the new line of code would be:  
    ```
    locations = {
        "q": ["nanyuki", "naivasha", "embu"], 
        "accu": ["225705", "225702", "225708"]
    }
    ```
* If you add a new API that has a different way of referencing it's location parameter, say **'pin'**, the new line of code reflecting this change would be as follows:
    ```
    locations = {
        "q": ["nanyuki", "naivasha"], 
        "accu": ["225705", "225702"],
        "pin": ["NBI", "MBA"]
    }
    ```

## Getting Started

### Dependencies

Pipenv has been used for dependency management for this project. The following are key dependencies:
* pymongo == 3.12.0
* python-dotenv == 0.19.0
* requests == 2.26.0
* black == 21.6b0
* flake8 == 3.9.2
* isort == 5.9.3


### Installing
> Ensure to have **Python 3.8** and **Pipenv** installed  
> Pipenv has been used for dependency management  

After cloning the project repository:
1. Run this to install dependencies  
    ```
    pipenv install --dev
    ```
2. Run this to launch a virtual environment
    ```
    pipenv shell
    ```

### Executing program

Key things to note before running the script for the *first time*:  
* Edit the following [config.ini](config.ini) entries:  
    * *dt* and *date*: both referring to the date. The sections containing these entries collect actual weather data. Hence, if the link is to run from today those values should be set to the date yesterday
* Edit the following [date.ini](date.ini) entries:  
    * *1*, *3* and *5* in the *[date]* section: corresponding to the next dathe script should run. If running for the first time, this date should always be the current day and in the format *YYYY-MM-DD*
* These values will auto-update once the script is running regularly as a microservice or cron job

* To run [script.py](script.py)
    ```
    python script.py
    ```

## Version History

* 0.1
    * Initial Release
    * Collection from three APIs
    * Data is saved to MongoDB