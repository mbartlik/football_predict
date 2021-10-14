import os
from os import path
import pymysql
import datetime
import random

# info about signing into the google cloud sql database
db_user = 'root'
db_password = ''
db_name = 'main'
db_connection_name = 'seismic-gecko-326618:us-east4:nfl-prediction-challenge'

# dates for games that open the week
open_dates = [datetime.datetime(2021,9,9),datetime.datetime(2021,9,16), datetime.datetime(2021,9,23), datetime.datetime(2021,9,30), datetime.datetime(2021,10,7), datetime.datetime(2021,10,14), datetime.datetime(2021,10,21), datetime.datetime(2021,10,28), datetime.datetime(2021,11,4), datetime.datetime(2021,11,11), datetime.datetime(2021,11,18), datetime.datetime(2021,11,25), datetime.datetime(2021,12,2), datetime.datetime(2021,12,9), datetime.datetime(2021,12,16), datetime.datetime(2021,12,23), datetime.datetime(2022,1,2), datetime.datetime(2022,1,9)]

# dates for games that close the week
close_dates = [datetime.datetime(2021,9,13), datetime.datetime(2021,9,20), datetime.datetime(2021,9,27), datetime.datetime(2021,10,4), datetime.datetime(2021,10,11), datetime.datetime(2021,10,18), datetime.datetime(2021,10,25), datetime.datetime(2021,11,1), datetime.datetime(2021,11,8), datetime.datetime(2021,11,15), datetime.datetime(2021,11,22), datetime.datetime(2021,11,29), datetime.datetime(2021,12,6), datetime.datetime(2021,12,13), datetime.datetime(2021,12,20), datetime.datetime(2021,12,27), datetime.datetime(2022,1,3), datetime.datetime(2022,1,9)]

# check if a user is already in the database
# if not they are new and will be added to the database
def check_new_user(username):
    conn = get_connection()
    cur = conn.cursor()
    count = cur.execute('SELECT * FROM Users WHERE Name=%s', (username,))

    # new user
    if count < 1:
        cur.execute('INSERT INTO Users (Name, WinCount, DisplayName) VALUES (%s,%s,%s)', (username,0,''))
        conn.commit()
    
    conn.close()

# Randomly generate a 6 character join code
letters_and_nums = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','1','2','3','4','5','6','7','8','9']
def get_join_code():
    return ''.join(random.choice(letters_and_nums) for i in range(6))

# Convert an array in the form ['entry_1','entry_2',...,'entry_n'] to a string in the form 'entry_1,entry_2,...,entry_n'
def arr_to_str(arr):
    res = ''
    for i in range(len(arr)-1):
        res += arr[i] + ','
    res += arr[len(arr)-1]

    return res

# gets the current nfl week
def get_current_nfl_week():
    nfl_week = -1
    python_date = datetime.datetime.now()
    for i in range(len(open_dates)):
        if i == (len(open_dates) - 1):
            raise Exception('Date out of range')   
        if python_date < open_dates[i]:
            nfl_week = i + 1
            break

    return nfl_week


# Takes python datetime object and returns a string that is consistent with SQL date formatting
def get_sql_date(date):
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)

    if len(month) == 1:
        month = '0' + str(month)
    if len(day) == 1:
        day = '0' + str(day)

    formatted_date = year + '-' + month + '-' + day

    return formatted_date




# Establishes connection with Google Cloud SQL database
def get_connection():
	# when deployed to app engine the 'GAE_ENV' variable will be set to 'standard'
	if os.environ.get('GAE_ENV') == 'standard':
		# use the local socket interface for accessing Cloud SQL
		unix_socket = '/cloudsql/{}'.format(db_connection_name)
		conn = pymysql.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name)
	else:
		# if running locally use the TCP connections instead
		# set up Cloud SQL proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
		host = '127.0.0.1'
		conn = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)

	return conn


# Makes a new competition in the gcloud sql database
def create_competition_sql(competition_name, username):
    conn = get_connection()
    cur = conn.cursor()

    # get current date and format it
    python_date = datetime.datetime.now()
    open_date = get_sql_date(python_date)

    # get current nfl week and end date
    nfl_week = -1
    close_date = ''
    for i in range(len(open_dates)):
        if i == (len(open_dates) - 1):
            raise Exception('Date out of range')   
        if python_date < open_dates[i]:
            nfl_week = i + 1
            close_date = get_sql_date(close_dates[i])
            break

    # get join codes until you get one that doesn't yet exist
    join_code = ''
    while(True):
        join_code = get_join_code()
        matching_join_code_count = cur.execute('SELECT * FROM Competitions WHERE JoinCode=%s',(join_code,))
        if matching_join_code_count != 1:
            break
    
    # add the new competition
    cur.execute('INSERT INTO Competitions (Name, DateCreated, DateEnd, Week, JoinCode) VALUES (%s, %s, %s, %s, %s)', (competition_name, open_date, close_date, nfl_week, join_code))

    # get the new competition's id
    cur.execute('SELECT * FROM Competitions WHERE JoinCode=%s',(join_code,))
    query = cur.fetchall()
    competition_id = query[0][0]

    # add this user and competition id to the competing relation
    cur.execute('INSERT INTO Competing (Username, CompetitionID) VALUES (%s, %s)', (username, competition_id))

    conn.commit()
    conn.close()

    return competition_id


# INPUT: join code correlating to a competition
# if a competition matches, then add the user to the competition, and add the competition to the user's competitions
def join_competition_sql(join_code, username):
    conn = get_connection()
    cur = conn.cursor()

    # try to get info about a competition with this join code
    matching_competition_count = cur.execute('SELECT * FROM Competitions WHERE JoinCode=%s',(join_code,))
    if matching_competition_count == 0:
        return 'Invalid join code'

    competition_id = cur.fetchall()[0][0]

    # add this user and competition id to the competing relation
    cur.execute('INSERT INTO Competing (Username, CompetitionID) VALUES (%s, %s)', (username, competition_id))
    
    conn.commit()
    conn.close()

    return competition_id


# get info about a single competition based on id
def get_competition(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM Competitions WHERE ID=%s', (id,))
    competition = cur.fetchall()

    conn.close()

    return competition

# get all competitions associated with a user
# returns list of competition IDs
def get_competitions(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('SELECT CompetitionID FROM Competing WHERE Username=%s',(username,))

    competitions = cur.fetchall()

    competition_ids = [competition[0] for competition in competitions]

    if len(competition_ids) == 0:
        return []

    competitions_info = [get_competition(id) for id in competition_ids]

    return competitions_info

def get_users_in_competition(competition_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('SELECT Username FROM Competing WHERE CompetitionID=%s',(competition_id,))

    users = cur.fetchall()

    users_list = [user[0] for user in users]

    return users_list


def get_binary_picks(username, competition_id):
    conn = get_connection()
    cur = conn.cursor()

    exists = cur.execute('SELECT * FROM Competing WHERE Username=%s AND CompetitionID=%s', (username, competition_id))

    if exists == 0:
        return 'competition does not exist'
    
    query_res = cur.fetchall()
    binary_picks = query_res[0][2:18]

    return binary_picks


# Given a username and competition id, return all the picks by that user for a competition
# Returns array of game predictions where each prediction is in the following form:
# ('team picked by user', ('home team', 'away team'))
def get_user_picks(username, competition_id):
    conn = get_connection()
    cur = conn.cursor()

    binary_picks = get_binary_picks(username, competition_id)

    # get week of competition
    cur.execute('SELECT Week FROM Competitions WHERE ID=%s',(competition_id,))
    week = cur.fetchall()[0][0]

    week = 6

    # get list of home teams
    cur.execute('SELECT Team FROM Games WHERE Week=%s AND Home=1', (week, ))
    home_teams = cur.fetchall()

    # get list of away teams
    cur.execute('SELECT Team FROM Games WHERE Week=%s AND Home=0', (week, ))
    away_teams = cur.fetchall()
    
    picks = []

    # assign binary picks to actual team values with the home and away teams
    for i in range(len(binary_picks)):
        if binary_picks[i] == 0:
            picks.append((away_teams[i][0], (home_teams[i][0], away_teams[i][0])))
        elif binary_picks[i] == 1:
            picks.append((home_teams[i][0], (home_teams[i][0], away_teams[i][0])))
        else:
            break

    conn.close()

    return picks


# Returns a list of tuples, where each tuple is 2 teams, the 1st one being the home team
# The week of games must be specified as an int
def get_games(week):
    conn = get_connection()
    cur = conn.cursor()

    # get home teams
    cur.execute('SELECT * FROM Games WHERE Week=%s AND Home=1', (week,))
    home_teams = cur.fetchall()

    # get away teams
    cur.execute('SELECT * FROM Games WHERE Week=%s AND Home=0', (week,))
    away_teams = cur.fetchall()

    matchups = []
    for i in range(16):
        if home_teams[i][2] != away_teams[i][2]:
            return 'Error with database. Let Max know'
        matchups.append((home_teams[i][1], away_teams[i][1]))

    conn.close()

    return matchups

def update_picks(competition_id, username, picks):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('UPDATE Competing SET Pick1=%s, Pick2=%s, Pick3=%s, Pick4=%s, Pick5=%s, Pick6=%s, Pick7=%s, Pick8=%s, Pick9=%s, Pick10=%s, Pick11=%s, Pick12=%s, Pick13=%s, Pick14=%s, Pick15=%s, Pick16=%s WHERE Username=%s AND CompetitionID=%s', (picks[0], picks[1], picks[2], picks[3], picks[4], picks[5], picks[6], picks[7], picks[8], picks[9], picks[10], picks[11], picks[12], picks[13], picks[14], picks[15], username, competition_id))

    conn.commit()
    conn.close()


# Gets the week of a competition, given the competition id
def get_week(competition_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('SELECT Week FROM Competitions WHERE ID=%s',(competition_id,))
    week = cur.fetchall()[0][0]

    conn.close()

    return week