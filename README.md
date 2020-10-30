# Setup

## Environment Variable
Before deploy the Flask web application you will need to create a `.env` file under the `application` directory.
In the `.env` file, you will need to have the following API KEY
```.env
export NATLPARKS_KEY = '<replace-me>'
export HIKING_KEY = '<replace-me>'
export WEATHER_KEY = '<replace-me>'
```

Once `.env` has been created, you will need to start a new virtual env by running the following code `python3 -m venv env` (for mac user) or `python-m venv env` (for windows user). You can activate your new virtual env by running `source env/bin/activate` (for mac user) or `env\Scripts\activate` (for windows user).

## Memcached 
This web application requires memcached and here is the instruction on how to setup the memcached on your machine.
1. Install `memcached` on your local machine. Macs install with homebrew, Windows install
https://memcached.org/
2. Install Python client for memcached https://pymemcache.readthedocs.io/en/latest/getting_started.html
3. Run memcached, and leave it running while you starting the Flask web application


## Flask Web App

1. Download the requirements by running `pip install -r requirements.txt`
1. On your Terminal/Command Prompt, change the directory to the `application` folder
2. Then start a Flask web app with `python3 app.py`
3. View the web application on `localhost:5000`


# Unit Testing
For the Flask unittesting, it locates under `application` folder. You can run the testing by running `python3 -m unittest test_basicapp.py`

As for the API and database unittesting, they are located under th `testing` folder, so you will need to run with this `python3 -m unittest testing/<test-file-name-here>.py `