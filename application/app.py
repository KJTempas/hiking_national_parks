from flask import Flask, render_template, request, redirect, url_for
from api_calls import natlParks_api, hiking_api, weather_api, state_name_and_code
from database import models, database_functions

import logging

# Logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%y %H:%M:%S')
log = logging.getLogger('root')
# from models import *
app = Flask(__name__)


@app.before_request
def before_request():
    # create db if needed and connect
    models.initialize_db()


@app.teardown_request
def teardown_request(exception):
    # close the db connection
    models.db.close()


@app.route('/', methods=['GET'])
def home():
    state_dict = state_name_and_code.get_state_abbrev()

    return render_template('index.html', states_dict=state_dict)


# TODO: Modified the route based on the selected state
@app.route('/parks', methods=['GET', 'POST'])
def show_national_park():
    if request.method == 'POST':
        return redirect(url_for('home'))
    else:

        state_input = request.args.get('states')

        park_list = natlParks_api.get_response(state_input.lower())

        return render_template('park_list.html', park_list=park_list, state=state_input)


@app.route('/moreinfo/<state>/<park>/<lat>/<lon>', methods=['GET', 'POST'])
def get_trail_weather(state, park, lat, lon):
    if request.method == 'POST':
        if request.form.get('trail-obj'):
            trail_obj = eval(request.form.get('trail-obj'))
            # Save the db here
            # database_functions.add_saved_trail(trail_name, length, summary, park, state)
            # then rendered the show_saved_trails page on the return
            # add_saved_trail(name, leng, summ, natl_pk, state)

            database_functions.add_trail(name=trail_obj['name'], leng=trail_obj['length'], summ=trail_obj['summary'],
                                         natl_pk=park, state=state)
            return redirect(url_for('show_saved_trails'))
        elif request.form.get('back-page'):
            return redirect(url_for('show_national_park', states=state))
    else:
        trail_list = hiking_api.get_trails(lat, lon)
        weather_list = weather_api.get_weather(lat, lon)

        return render_template('hikes_weather.html', park=park, trail_list=trail_list, weather_list=weather_list)


@app.route('/savedtrails')
def show_saved_trails():
    # trail_name, length, summary, park, state
    # Mainly retrieve the trail info from db
    saved_trails = database_functions.get_all_saved_trails()
    log.info(saved_trails)
    # pass bookmark_list to the template

    return render_template('save_trail.html', bookmark_list=saved_trails)


if __name__ == "__main__":
    app.run(debug=True)
