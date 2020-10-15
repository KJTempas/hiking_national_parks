from flask import Flask, render_template, request, redirect, url_for
from api_calls import natlParks_api

# from models import *
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    state_list = natlParks_api.get_all_state_name()
    test_name = request.args.get('states')

    # if request.method == 'GET':
    #     test_name = request.args.get('states')
    #     print(test_name)
    #     return render_template(redirect('/'), states=state_list, test=test_name)
    # else:
    #

    return render_template('index.html', states=state_list, test=test_name)




@app.route('/parks', methods=['GET'])
def show_national_park():

    # TODO Some state like CA will have out of range list
    user_input_1 = request.args.get('states')
    park_list = natlParks_api.get_response(user_input_1.lower())
    return render_template('park_list.html', park_list=park_list, state=user_input_1)


if __name__ == "__main__":
    app.run(debug=True)
