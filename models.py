import os
from os import path
import pymysql
import datetime
import random

# info about signing into the google cloud sql database
db_user = 'root'
db_password = ''
db_name = 'FootballPredictionChallenge'
db_connection_name = 'seismic-gecko-326618:us-east4:football-prediction-challenge'

# dates for games that open the week
open_dates = [datetime.datetime(2021,9,9),datetime.datetime(2021,9,16), datetime.datetime(2021,9,23), datetime.datetime(2021,9,30), datetime.datetime(2021,10,7), datetime.datetime(2021,10,14), datetime.datetime(2021,10,21), datetime.datetime(2021,10,28), datetime.datetime(2021,11,4), datetime.datetime(2021,11,11), datetime.datetime(2021,11,18), datetime.datetime(2021,11,25), datetime.datetime(2021,12,2), datetime.datetime(2021,12,9), datetime.datetime(2021,12,16), datetime.datetime(2021,12,23), datetime.datetime(2022,1,2), datetime.datetime(2022,1,9)]

# dates for games that close the week
close_dates = [datetime.datetime(2021,9,13), datetime.datetime(2021,9,20), datetime.datetime(2021,9,27), datetime.datetime(2021,10,4), datetime.datetime(2021,10,11), datetime.datetime(2021,10,18), datetime.datetime(2021,10,25), datetime.datetime(2021,11,1), datetime.datetime(2021,11,8), datetime.datetime(2021,11,15), datetime.datetime(2021,11,22), datetime.datetime(2021,11,29), datetime.datetime(2021,12,6), datetime.datetime(2021,12,13), datetime.datetime(2021,12,20), datetime.datetime(2021,12,27), datetime.datetime(2022,1,3), datetime.datetime(2022,1,9)]

# check if a user is already in the database
# if not they are new and will be added to the database
def check_new_user(username):
    print("Checking new user")
    print(username)
    conn = get_connection()
    cur = conn.cursor()
    count = cur.execute('SELECT * FROM Users WHERE Name=%s', (username,))

    # new user
    if count < 1:
        cur.execute('INSERT INTO Users (Name, Competitions, WinCount, DisplayName) VALUES (%s,%s,%s,%s)', (username,'',0,''))
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
def create_competition_sql(competition_name, user):
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
    cur.execute('INSERT INTO Competitions (Name, Users, DateCreated, DateEnd, Week, JoinCode) VALUES (%s, %s, %s, %s, %s, %s)', (competition_name, user, open_date, close_date, nfl_week, join_code))

    # get the user's current info to add the new competition
    cur.execute('SELECT * FROM Users WHERE Name=%s',(user,))
    query = cur.fetchall()
    user_competitions = query[0][1]
    
    # get the new competition's id
    cur.execute('SELECT * FROM Competitions WHERE JoinCode=%s',(join_code,))
    query = cur.fetchall()
    competition_id = query[0][0]

    if len(user_competitions) == 0:
        user_competitions = '' + str(competition_id)
    else:
        user_competitions += ',' + str(competition_id)

    # update users db with the new competition id addition
    cur.execute('UPDATE Users SET Competitions=%s WHERE Name=%s',(user_competitions,user))

    conn.commit()
    conn.close()

    return True


# INPUT: join code correlating to a competition
# if a competition matches, then add the user to the competition, and add the competition to the user's competitions
def join_competition_sql(join_code, username):
    conn = get_connection()
    cur = conn.cursor()

    # try to get info about a competition with this join code
    matching_competition_count = cur.execute('SELECT * FROM Competitions WHERE JoinCode=%s',(join_code,))
    if matching_competition_count == 0:
        return 'Invalid join code'
    
    # get the users for this competition
    competition = cur.fetchall()
    competition_users = competition[0][2]
    competition_users_li = list(competition_users.split(","))

    # check to see if this user is already in the competition
    if username in competition_users_li:
        return 'You are already in this competition'

    # add this user
    competition_users_li.append(username)

    # convert the array to a string to put in db
    new_competition_users = arr_to_str(competition_users_li)
    print(new_competition_users)

    # update the users for this competition
    cur.execute('UPDATE Competitions SET Users=%s WHERE JoinCode=%s', (new_competition_users,join_code))


    # get the user's current info to add the new competition
    cur.execute('SELECT * FROM Users WHERE Name=%s',(username,))
    query = cur.fetchall()
    user_competitions = query[0][1]
    
    # get the new competition's id
    cur.execute('SELECT * FROM Competitions WHERE JoinCode=%s',(join_code,))
    query = cur.fetchall()
    competition_id = query[0][0]

    if len(user_competitions) == 0:
        user_competitions = '' + str(competition_id)
    else:
        user_competitions += ',' + str(competition_id)

    # update users db with the new competition id addition
    cur.execute('UPDATE Users SET Competitions=%s WHERE Name=%s',(user_competitions,username))

    conn.commit()
    conn.close()


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

    cur.execute('SELECT Competitions FROM Users WHERE Name=%s',(username,))

    competitions = cur.fetchall()

    return list(competitions[0][0].split(','))