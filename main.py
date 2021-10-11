from models import create_competition_sql, check_new_user, join_competition_sql, get_competition, get_competitions, get_users_in_competition, get_user_picks, get_games, update_picks, get_week

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

    check_new_user(session['profile']['user_id'])

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
    # get list of competition IDs for this user
    competition_ids = get_competitions(session['profile']['user_id'])

    if len(competition_ids) != 0:
        # get info about all the competitions associated with the user
        competitions_info = [get_competition(id) for id in competition_ids]

        # isolate all the competition names
        competition_names = [competitions_info[i][0][1] for i in range(len(competitions_info))]

        # make links to go along with each name with the appropriate id
        display_links = ['/display-competition?competition_id=' + str(competitions_info[i][0][0]) for i in range(len(competitions_info))]
    else:
        competitions_info = []
        competition_names = []
        display_links = []

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
        competition_name = request.form["name"]
        this_user = session['profile']['user_id']
        competition_id = create_competition_sql(competition_name, this_user)
        return redirect('/display-competition?competition_id=' + str(competition_id))

    return render_template('create_competition.html')

@app.route("/display-competition")
@requires_auth
def display_competition():
    id = request.args.get('competition_id')

    competition = get_competition(id)
    name = competition[0][1]
    join_code = competition[0][5]

    users = get_users_in_competition(id)

    picks = get_user_picks(session['profile']['user_id'],int(id))

    picks_made = False
    if len(picks) > 0:
        picks_made = True

    week = get_week(id)

    make_picks_link = '/make-picks?competition_id=' + id + '&week=' + str(week)

    return render_template('display_competition.html', name=name, join_code=join_code, users=users, picks=picks, picks_made=picks_made, make_picks_link=make_picks_link)

@app.route("/join-competition", methods=["GET","POST"])
@requires_auth
def join_competition():
    if request.method == 'POST':
        res = join_competition_sql(request.form["join_code"], session['profile']['user_id'])
        if res == 'Invalid join code':
            print('Invalid join code')
        elif res == 'You are already in this competition':
            print('You are already in this competition')
        else:
            return redirect('/display-competition?id=' + str(res))


    return render_template('join_competition.html')

@app.route("/make-picks", methods=["GET", "POST"])
@requires_auth
def make_picks():
    if request.method == 'POST':
        data = json.loads(request.data)
        picks = data["picks"]
        competition_id = data["competition_id"]

        update_picks(competition_id, session['profile']['user_id'], picks)

        return "Success"

    competition_id = request.args.get('competition_id')
    week = request.args.get('week')

    # FIX LATER - MUST GET WEEK NUMBER DYNAMICALLY
    matchups = get_games(week)

    return render_template('make_picks.html', matchups=matchups, competition_id=competition_id)