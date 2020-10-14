from flask import Flask, render_template, request, redirect, url_for
from api_calls import natlParks_api as np_api
# from models import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['GET'])
def show_national_park():


    user_input = request.form['state']
    data = np_api.get_response(user_input)


    return redirect(url_for('home'), user_inputs=user_input)


if __name__ == "__main__":
    app.run(debug=True)
