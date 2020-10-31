# Setup

## Environment Variable
Before deploying the Flask web application you will need to create a `.env` file under the `application` directory.
In the `.env` file, you will need to have the following API KEY
```.env
export NATLPARKS_KEY = '<your-api-key-here>'
export HIKING_KEY = '<your-api-key-here>'
export WEATHER_KEY = '<your-api-key-here>'
```

Once `.env` has been created, start a new virtual env by running the following code `python3 -m venv env` (for Mac user) or `python-m venv env` (for Windows user). Activate your new virtual env by running `source env/bin/activate` (for Mac user) or `env\Scripts\activate` (for Windows user).

## Memcached 
This web application requires memcached. Here are instruction on how to setup the memcached on your machine.

1. Install `memcached` on your local machine. For Mac user install `memcached` with `homebrew`, [here](https://gist.github.com/tomysmile/ba6c0ba4488ea51e6423d492985a7953#step-1--install-homebrew) is an simple instruction to install `homebrew` as well as `memcached` (follow step 1 and 2 on the link) .For Windows user you can install `memcached` from [here](https://memcached.org/)
2. You also need to install Python client for memcached via this command `pip install pymemcache`
3. Then run memcached with `brew services start memcached` (for Mac user) or `memcached.exe -d start` (for Windows user), and leave it running while you starting the Flask web application

*Helpful article for Windows user to install Memcached, click [here](https://www.journaldev.com/42/how-to-install-memcached-server-on-windows-as-service) to learn more.* 


## Flask Web App

1. Download the requirements by running `pip install -r requirements.txt`
1. In your Terminal/Command Prompt, change the directory to the `application` folder
2. Start a Flask web app with `python3 app.py`
3. View the web application at `localhost:5000`


# Unit Testing
Flask unittesting is located in the `application` folder. Run the tests by running `python3 -m unittest test_flask_app.py`

Other testing like API call and database are located under the `testing` folder. Run these with `python3 -m unittest discover testing`  if your current working directory is the `application` folder. Alternately, to run tests in only one of the testing files at once, run `python3 -m unittest testing/<test-file-name-here>.py `


# TroubleShooting

If you are facing any issues in running the Flask web application, make sure to change your directory to the `application` before running `python3 app.py`. Also make sure that you have installed all the requirements using the following command `pip install -r requirements.txt`.

If none of the solutions work for you or you faced other issues, feel free to open an Issue, one of the collaborator will work on fixing the issues or provide you with a solution. 

