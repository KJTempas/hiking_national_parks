from flask import Flask, render_template, request, redirect, url_for
from api_calls import natlParks_api, hiking_api, weather_api

# from models import *
app = Flask(__name__)
# TODO need to validate if the parklist, weatherlist and traillist has data or no

@app.route('/', methods=['GET'])
def home():
    state_list = natlParks_api.get_all_state_name()

    return render_template('index.html', states=state_list)


# TODO: Modified the route based on the selected state
@app.route('/parks', methods=['GET'])
def show_national_park():
    # TODO Some state like CA will have out of range list
    state_input = request.args.get('states')
    state_code = natlParks_api.get_state_code(state_input)
    park_list = natlParks_api.get_response(state_code.lower())
    return render_template('park_list.html', park_list=park_list, state=state_input)


@app.route('/moreinfo/<park>/<lat>/<lon>')
def get_trail(park, lat, lon):

    trail_list = hiking_api.get_trails(lat, lon)
    weather_list = weather_api.get_weather(lat, lon)


    return render_template('hikes_weather.html', park=park, trail_list=trail_list, weather_list=weather_list)


if __name__ == "__main__":
    app.run(debug=True)