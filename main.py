from models import create_competition_sql, check_new_user, join_competition_sql, get_competition, get_competitions

from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask import request
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

from functools import wraps

app = Flask(__name__)

app.secret_key = 'giusdbwfaw'

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='djEG1S4NhP9s8fOFvZZDNcED8G379qsG',
    client_secret='DoaRskKn7y6FzdvzNOsKiyLp2UcUBmjD0s_Euv2uEd18zot18L0oUKZGgnlvU3L2',
    api_base_url='https://dev-w24y1oq2.us.auth0.com',
    access_token_url='https://dev-w24y1oq2.us.auth0.com/oauth/token',
    authorize_url='https://dev-w24y1oq2.us.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/home')

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            # Redirect to Login page here
            return redirect('/')
        return f(*args, **kwargs)

    return decorated


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='http://127.0.0.1:5000/callback')


@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    return redirect(auth0.api_base_url + '/v2/logout?returnTo=http%3A%2F%2F127.0.0.1:5000/&client_id=06F6PVKlsBK5xXyHHc6QiBnDYPox7ctx')


@app.route("/home")
@requires_auth
def home():
    check_new_user(session['profile']['user_id'])

    # get list of competition IDs for this user
    competition_ids = get_competitions(session['profile']['user_id'])
    print(competition_ids)

    # get info about all the competitions associated with the user
    competitions_info = [get_competition(int(id)) for id in competition_ids]
    print(competitions_info)
    print(competitions_info[0])

    # isolate all the competition names
    competition_names = [competitions_info[i][0][1] for i in range(len(competitions_info))]

    # make links to go along with each name with the appropriate id
    display_links = ['/display-competition?id=' + str(competitions_info[i][0][0]) for i in range(len(competitions_info))]

    return render_template('home.html', userinfo=session['profile'], competition_names=competition_names, display_links=display_links)

@app.route("/profile")
@requires_auth
def profile():
    return render_template('your_profile.html', userinfo=session["profile"])

@app.route("/about")
@requires_auth
def about():
    return render_template('about.html')

@app.route("/create-competition", methods=["GET","POST"])
@requires_auth
def create_competition():
    if request.method == 'POST':
        print("test")
        competition_name = request.form["name"]
        this_user = session['profile']['user_id']
        success = create_competition_sql(competition_name, this_user)
        print("test_@")
        if not success:
            return render_template('error.html', error_message='Could not create competition. Please try again later.')
        return redirect('/display-competition')

    return render_template('create_competition.html')

@app.route("/display-competition")
@requires_auth
def display_competition():
    id = request.args.get('id')

    competition = get_competition(id)

    name = competition[0][1]
    join_code = competition[0][6]

    return render_template('display_competition.html', name=name, join_code=join_code)

@app.route("/join-competition", methods=["GET","POST"])
@requires_auth
def join_competition():
    if request.method == 'POST':
        res = join_competition_sql(request.form["join_code"], session['profile']['user_id'])
        print(res)


    return render_template('join_competition.html')