from flask import Flask, render_template, request, redirect, url_for
from api_calls import natlParks_api as np_api
# from models import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/parks', methods=['GET'])
def show_national_park():

    user_input = request.args.get('state')
    park_list = np_api.get_response(user_input)
    return render_template('park_list.html', park_list=park_list, state=user_input)


if __name__ == "__main__":
    app.run(debug=True)
