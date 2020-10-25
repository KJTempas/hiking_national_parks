# Getting Started

Before deploy the Flask web application you will need to create a `.env` file under the `application` directory.
In the `.env` file, you will need to have the following API KEY
```.env
export NATLPARKS_KEY = '<replace-me>'
export HIKING_KEY = '<replace-me>'
export WEATHER_KEY = '<replace-me>'
```

Once `.env` has been created, you will need to start a new virtual env by running the following code `python3 -m venv env`. You can activate your new virtual env by running `source env/bin/activate`.

## Start memcached on local machine
1. Install `memcached` on your local machine. Macs install with homebrew, Windows install
https://memcached.org/
2. Install Python client for memcached https://pymemcache.readthedocs.io/en/latest/getting_started.html
3. Run memcached, leave it running while you run your code


## Start a new Flask Web App
1. Download the requirements with `pip install -r requirements.txt`
2. Start a Flask web app with `python3 application/app.py`
3. View the web application on `localhost:5000`

