from models import create_competition_sql, check_new_user, join_competition_sql, get_competition, get_competitions, get_users_in_competition, get_user_picks, get_games, update_picks, get_week, get_current_nfl_week, get_binary_picks, update_competition_results, get_win_count, get_competition_results, set_display_name, get_user

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

#base_url = 'http://127.0.0.1:5000/'
base_url = 'https://seismic-gecko-326618.ue.r.appspot.com/'

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
    return auth0.authorize_redirect(redirect_uri=base_url + 'callback')


@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    return redirect(auth0.api_base_url + '/v2/logout?returnTo=' + base_url + '&client_id=djEG1S4NhP9s8fOFvZZDNcED8G379qsG')


@app.route("/home")
@requires_auth
def home():
    try:
        username = session['profile']['user_id']

        # get list of competitions with details for this user
        competitions_info = get_competitions(username)

        # get current week
        nfl_week = get_current_nfl_week()

        current_competitions = []
        for competition in competitions_info:
            if competition[0][4] >= nfl_week:
                current_competitions.append(competition)

        if len(current_competitions) != 0:
            # isolate all the competition names
            competition_names = [current_competitions[i][0][1] for i in range(len(current_competitions))]

            # make links to go along with each name with the appropriate id
            display_links = ['/display-competition?id=' + str(current_competitions[i][0][0]) for i in range(len(current_competitions))]
        else:
            competition_names = []
            display_links = []

        # check if this user has admin abilities
        admin = False
        if username == 'google-oauth2|117368091909014194509':
            admin = True

        return render_template('home.html', userinfo=session['profile'], competition_names=competition_names, display_links=display_links, admin=admin, nfl_week=nfl_week)
    except Exception as e:
        return render_template('error.html', error_message='problem loading the home screen', error_detail=e)

@app.route("/profile", methods=["GET","POST"])
@requires_auth
def profile():
    try:
        if request.method == 'POST':
            display_name = request.form['display_name']
            set_display_name(session['profile']['user_id'], display_name)
        
        user_info = get_user(session['profile']['user_id'])
        display_name = user_info[3]
        wins = get_win_count(session['profile']['user_id'])
        return render_template('your_profile.html', userinfo=session["profile"], wins=wins, display_name=display_name)
    except Exception as e:
        return render_template('error.html', error_message='problem loading profile page', error_detail=e)

@app.route("/about")
@requires_auth
def about():
    return render_template('about.html')

@app.route("/create-competition", methods=["GET","POST"])
@requires_auth
def create_competition():
    try:
        if request.method == 'POST':
            competition_name = request.form["name"]
            this_user = session['profile']['user_id']
            competition_id = create_competition_sql(competition_name, this_user)
            return redirect('/display-competition?id=' + str(competition_id))

        return render_template('create_competition.html')
    except Exception as e:
        return render_template('error.html', error_message='Could not create competition', error_detail=e)

@app.route("/display-competition")
@requires_auth
def display_competition():
    try:
        id = request.args.get('id')

        competition = get_competition(id)
        name = competition[0][1]
        week = competition[0][4]
        join_code = competition[0][5]
        
        users = get_users_in_competition(id)

        participating = []
        for user in users:
            user_info = get_user(user)
            display_name = user_info[3]
            if display_name:
                participating.append(user_info[3])
            else:
                participating.append(user_info[1])

        picks = get_user_picks(session['profile']['user_id'],int(id))

        picks_made = False
        if len(picks) > 0:
            picks_made = True

        week = get_week(id)

        make_picks_link = '/make-picks?competition_id=' + id + '&week=' + str(week)

        # get the competition results if this is a previous competition
        results = None
        if week < get_current_nfl_week():
            results = get_competition_results(id)

        display_names = []
        results_cleaned = []
        if results:
            for result in results:
                user_info = get_user(result[1])
                display_name = user_info[3]
                if display_name:
                    display_names.append(user_info[3])
                else:
                    display_names.append(user_info[1])

            for i in range(len(results)):
                results_cleaned.append((results[i][2], display_names[i]))

        return render_template('display_competition.html', name=name, week=week, join_code=join_code, users=users, picks=picks, picks_made=picks_made, make_picks_link=make_picks_link, results=results_cleaned, participating=participating)
    except Exception as e:
        return render_template('error.html', error_message='problem displaying competition details', error_detail=e)

@app.route("/join-competition", methods=["GET","POST"])
@requires_auth
def join_competition():
    try:
        if request.method == 'POST':
            res = join_competition_sql(request.form["join_code"], session['profile']['user_id'])
            if res == 'Invalid join code':
                print('Invalid join code')
            elif res == 'You are already in this competition':
                print('You are already in this competition')
            else:
                return redirect('/display-competition?id=' + str(res))


        return render_template('join_competition.html')
    except Exception as e:
        return render_template('error.html', error_message='Could not join competition', error_detail=e)

@app.route("/make-picks", methods=["GET", "POST"])
@requires_auth
def make_picks():
    if request.method == 'POST':
        data = json.loads(request.data)
        picks = data["picks"]
        competition_id = data["competition_id"]

        update_picks(competition_id, session['profile']['user_id'], picks)

        return "Success"

    try:
        competition_id = request.args.get('competition_id')
        week = request.args.get('week')

        matchups = get_games(week)

        binary_picks = get_binary_picks(session['profile']['user_id'], competition_id)

        return render_template('make_picks.html', matchups=matchups, competition_id=competition_id, binary_picks=binary_picks)

    except Exception as e:
        return render_template('error.html', error_message='problem loading this page', error_detail=e)

@app.route('/previous-competitions')
@requires_auth
def prev_competitions():
    try:
        # get list of competitions with details for this user
        competitions_info = get_competitions(session['profile']['user_id'])

        # get current week
        nfl_week = get_current_nfl_week()

        prev_competitions = []
        for competition in competitions_info:
            if competition[0][4] < nfl_week:
                prev_competitions.append(competition)

        if len(prev_competitions) != 0:
            # make links to go along with each name with the appropriate id
            display_links = ['/display-competition?id=' + str(prev_competitions[i][0][0]) for i in range(len(prev_competitions))]
        else:
            display_links = []

        return render_template('prev_competitions.html', userinfo=session['profile'], prev_competitions=prev_competitions, display_links=display_links)

    except Exception as e:
        return render_template('error.html', error_message='problem loading this page', error_detail=e)

@app.route('/admin', methods=['GET', 'POST'])
@requires_auth
def admin():
    try:
        username = session['profile']['user_id']

        # check if this user has admin abilities
        admin = False
        if username == 'google-oauth2|117368091909014194509':
            admin = True

        if request.method == 'POST':
            week = int(request.form.get('week'))

            message = update_competition_results(week)

            return render_template('admin.html', admin=admin, message=message)

        return render_template('admin.html', admin=admin)

    except Exception as e:
        return render_template('error.html', error_message='problem loading this page', error_detail=e)