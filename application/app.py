from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from api_calls import natlParks_api, hiking_api, weather_api, state_name_and_code
from database import models, database_functions
import peewee
import requests
import logging

# Custom Exception 
class AppError(Exception):
    pass

# Logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%y %H:%M:%S')
log = logging.getLogger('root')
app = Flask(__name__)

# CONSTANT
STATE_DICT = state_name_and_code.get_state_abbrev()

@app.before_request
def before_request():
    try:
        # create db if needed and/or connect
        models.initialize_db()
    except Exception as e:
        log.exception(e)
        abort(400, description=f'Page not found')
       

@app.teardown_request
def teardown_request(exception):
    # close the db connection
    models.db.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('show_saved_trails'))
    else:
        try:
            return render_template('index.html', states_dict=STATE_DICT)
        except Exception as e:
            log.exception(e)
            abort(500, description =f'The page you are looking for is not available. Please try again later.')


@app.route('/parks', methods=['GET', 'POST'])
def show_national_park():
    if request.method == 'POST':
        return redirect(url_for('home'))
    else:
        try:
            state_input = request.args.get('states')

            # Check if the state_input is valid state
            if state_input not in STATE_DICT.values():
                raise AppError('User has entered invalid input.')
            # Make API Call to get state park information
            park_list = natlParks_api.get_response(state_input.lower())
            # redirect to the state page
            return render_template('park_list.html', park_list=park_list, state=state_input)
        except requests.exceptions.HTTPError as e:
            log.exception(e)
            abort(403, description =f'The page you are looking for is not available. Please try again later.')
        except Exception as e:
            log.exception(e)
            abort(400, description =f'The URL is invalid. Please double check your spelling.')



@app.route('/moreinfo/<state>/<park>/<lat>/<lon>', methods=['GET', 'POST'])
def get_trail_weather(state, park, lat, lon):
    if request.method == 'POST':
        if request.form.get('trail-obj'):
            # Convert the `trail-obj` to dictionary format
            trail_obj = eval(request.form.get('trail-obj'))
            # Save the db here
            # then rendered the show_saved_trails page on the return
            try:
                database_functions.add_trail(name=trail_obj['name'], leng=trail_obj['length'],
                                             summ=trail_obj['summary'],
                                             natl_pk=park, state=state)
                return redirect(url_for('show_saved_trails'))
            except peewee.IntegrityError as e:
                log.exception(e)
                abort(400, description=f'{trail_obj["name"]} is already in the database. Please try to save another trail to the system.')
            except Exception as e:
                log.exception(e)
                abort(500, description=f'{trail_obj["name"]} was not able to add in the database at this moment. '
                                           f'Please try again later.')
        elif request.form.get('back-page'):
            # redirect to the previous page
            return redirect(url_for('show_national_park', states=state))
        else:
            log.exception(e)
            abort(400, 'No data provided.')
    else:
        try:
            tmp_park_name = park.replace(' ','').replace('&','').replace('\'','').replace('-','').replace('`','').replace('ʻ','')
            # Check if the url consist non-character string
            if not state.isalpha() or not tmp_park_name.isalpha():
                raise AppError('The URL consists of invalid character. Please double check your spelling befor proceeding.')
            else:
                trail_list = hiking_api.get_trails(lat, lon)
                weather_list = weather_api.get_weather(lat, lon)
                return render_template('hikes_weather.html', park=park, trail_list=trail_list, weather_list=weather_list)
        except requests.exceptions.HTTPError as e:
            log.exception(e)
            abort(403, description =f'The page you are looking for is not available. Please try again later.')
        except Exception as e:
            log.exception(e)
            abort(400, description=f'The URL is invalid. Please double check your spelling.')



@app.route('/savedtrails', methods=['GET', 'POST'])
def show_saved_trails():
    if request.method == 'POST':
        if request.form.get('back-page'):
            return redirect(url_for('home'))
        else:
            try:
                selected_row = request.form.get('selected-row')
                database_functions.delete_trail_by_id(eval(selected_row)['id'])
                return redirect(url_for('delete_trail', trail_name=eval(selected_row)['name']))
            except Exception as e:
                log.exception(e)
                abort(500,
                      description=f'{eval(selected_row)["name"]} was not able to be deleted from the database at this '
                                  f'moment. '
                                  f'Please try again later.')
    else:
        try:
            # Mainly retrieve the trail info from db
            saved_trails = database_functions.get_all_saved_trails()
            # pass bookmark_list to the template
            return render_template('save_trail.html', bookmark_list=saved_trails)
        except Exception as e:
            log.exception(e)
            abort(500,
                  description=f'Unable to retrieved saved trail at this moment. Please try again later.')
            
            
@app.route('/deleted/<trail_name>', methods=['GET', 'POST'])
def delete_trail(trail_name):
    if request.method == 'POST':
        if request.form.get('back-page'):
            return redirect(url_for('show_saved_trails'))
        else:
            return redirect(url_for('home'))
    else:
        return render_template('deleted_confirmation.html', trail_name=trail_name)


# Error Handler when an exception happen
@app.errorhandler(500)
def internal_error(error):
    log.error(f'Error 500. More detail: {error}')
    return render_template('errors.html', error_message=error.description)


@app.errorhandler(400)
def not_found(error):
    log.error(f'Error 400. More detail: {error}')
    return render_template('errors.html', error_message=error.description)

@app.errorhandler(403)
def invalid_page(error):
    log.error(f'Error 403. More detail: {error}')
    return render_template('errors.html', error_message=error.description)

@app.errorhandler(404)
def missing_params(error):
    log.error(f'Error 404. More detail: {error}')
    return render_template('errors.html', error_message='The URL is invalid. Please double check your spelling')

if __name__ == "__main__":
    app.run()

