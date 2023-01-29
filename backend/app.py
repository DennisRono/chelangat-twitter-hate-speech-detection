from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import tweepy
import json
import credentials
from typing import Tuple
import hashlib
import hmac
from flask_mail import Mail, Message
import random
import uuid
import jwt
import datetime
import binding
import random


app = Flask(__name__)
CORS(app)
dir_path = os.path.dirname(os.path.realpath(__file__))

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'cynthiakiprotich2020@gmail.com'
app.config['MAIL_PASSWORD'] = 'zcisamkypyuzdild'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

def get_db_connection():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_new_password(password: str) -> Tuple[bytes, bytes]:
    salt = os.urandom(16)
    pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt, pw_hash

def is_correct_password(salt: bytes, pw_hash: bytes, password: str) -> bool:
    return hmac.compare_digest(
        pw_hash,
        hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    )

def sendEmail(subject, sender, recepients, message):
    try:
        msg = Message(subject, sender=sender, recipients=recepients)
        msg.html = message
        mail.send(msg)
        return 'sent the email'
    except:
        return 'failed to send email'

def getTweets():
    client = tweepy.Client(bearer_token=credentials.BEARER_TOKEN, return_type=dict)
    lines = open('keywords.txt').read().splitlines()
    keyword =random.choice(lines)
    print(keyword)
    response = client.search_recent_tweets(query=keyword+" -is:retweet", max_results=10)
    tweets = json.dumps(response, indent=2)
    return tweets

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    for post in posts:
        print(post['Fname'])
        print(post['Lname'])
        print(post['Email'])
    return 'helloo'

@app.route('/mail', methods = ['POST', 'GET'])
def sendMail():
    return sendEmail

@app.route('/check', methods = ['POST', 'GET'])
def check():
    data = request.get_json()
    # text to be analyzed for hate speech
    tweet = data['mtweet']
    tpull = data['twitterpull']
    hate = binding.hateanalyze(tweet)
    analysis = binding.sentiment_analysis(tweet)
    analysis = {**analysis, 'state':'true'}
    userToken = data['token']
    user = jwt.decode(userToken['jwt'], credentials.TOKEN_SECRET, algorithms=["HS256"])
    user = user['email']
    # save data to database
    conn = get_db_connection()
    conn.execute("INSERT INTO mtweets (UserID, Tweet, Result, CompoundCore, Negative, Neutral, Positive) VALUES (?,?,?,?,?,?,?)",[user, tweet, hate['result'], analysis['dictionary']['compound'], analysis['dictionary']['neg'], analysis['dictionary']['neu'], analysis['dictionary']['pos']])
    conn.commit()
    conn.close()
    return {'data': [], 'mtweet': tweet, 'tpull': tpull, 'hate': hate, 'analysis':analysis}

@app.route('/twitter', methods = ['POST', 'GET'])
def twitter():
    tweet = getTweets()
    tweet = json.loads(tweet)
    analysis = {'state':'true'}
    tweet = {**tweet, 'analysis':analysis}
    return tweet

@app.route('/history', methods = ['POST', 'GET'])
def history():
    data = request.get_json()
    jwtToken = data['token']['jwt']
    session = jwt.decode(jwtToken, credentials.TOKEN_SECRET, algorithms=["HS256"])
    conn = get_db_connection()
    history = conn.execute("SELECT * FROM mtweets WHERE UserID=?", [session['email']]).fetchall()
    conn.close()
    myhist = []
    for r in history:
        myhist.append(dict(r))
    return myhist

@app.route('/auth/register', methods = ['POST', 'GET'])
def register():
    data = request.get_json()
    conn = get_db_connection()
    # check if user is already registered
    user = conn.execute("SELECT Email FROM users WHERE Email=?",[data['email']]).fetchall()
    if int(len(user)) > 0:
        return {'message':'user already registered, try logging in', 'type':'error'}
    else:
        if data['password'] != data['cpassword']:
            return {'message':'passwords did not match!', 'type':'error'}
        else:
            salt, password = hash_new_password(data['password'])
            conn.execute("INSERT INTO users (Fname, Lname, Email, Password, Salt) VALUES (?,?,?,?,?)",[data['fname'], data['lname'], data['email'], password, salt])
            conn.commit()
            conn.close()
            return {'message':'successfuly registered to the system', 'type':'success'}

@app.route('/auth/login', methods = ['POST', 'GET'])
def login():
    data = request.get_json()
    conn = get_db_connection()
    # check if the user is registered
    user = conn.execute("SELECT * FROM users WHERE Email=?",[data['email']]).fetchall()
    if int(len(user)) < 1:
        return {'message':'user not registered', 'type':'error'}
    else:
        for use in user:
            salt = use['Salt']
            passs= use['Password']
            Email = use['Email']
        if is_correct_password(salt, passs, data['password']):
            # set session to database
            sessionid = str(uuid.uuid4())[:12]
            authToken = jwt.encode({"session": sessionid, 'email':Email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1800)}, credentials.TOKEN_SECRET, algorithm="HS256")
            refreshToken = jwt.encode({"session": sessionid, 'email':Email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)}, credentials.REFRESH_TOKEN_SECRET, algorithm="HS256")
            conn.execute("UPDATE users SET Session=? Where Email=?",[sessionid, data['email']])
            conn.commit()
            conn.close()
            return {'message':'success', 'type':'success', 'authToken':authToken, 'refreshToken':refreshToken}
        else:
            return {'message':'wrong password', 'type':'error'}

@app.route('/auth/verifytoken', methods = ['POST', 'GET'])
def verifytoken():
    data = request.get_json()
    try:
        vertok = jwt.decode(data['token'], credentials.TOKEN_SECRET, algorithms=["HS256"])
        return {'message':'verification passed', 'type':'success', 'logout':'false', 'token': vertok, 'state':'passed'}
    except:
        try:
            verreftok = jwt.decode(data['refreshToken'], credentials.REFRESH_TOKEN_SECRET, algorithms=["HS256"])
            authToken = jwt.encode({"session": verreftok.session, 'email':verreftok.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1800)}, credentials.TOKEN_SECRET, algorithm="HS256")
            return {'message':'renewed token', 'type':'success', 'logout':'false', 'token': authToken, 'state':'renewed'}
        except:
            return {'message':'failed verification', 'type':'error', 'logout':'true', 'token':'', 'state':'failed'}

@app.route('/auth/reqreset', methods = ['POST', 'GET'])
def reqreset():
    data = request.get_json()
    conn = get_db_connection()
    # check if the user is registered
    user = conn.execute("SELECT * FROM users WHERE Email=?",[data['email']]).fetchall()
    if int(len(user)) < 1:
        return {'message':'user not registered', 'type':'error'}
    else:
        otp = random.randint(1000,9999)
        conn.execute("UPDATE users SET OTP=? WHERE Email=?",[otp, data['email']])
        conn.commit()
        conn.close()
        # send email to user
        sendEmail('Here is your OTP', 'admin@hatecrime.com', [data['email']], f'a one time password was requested for your account. <br> Here is your OTP <br><h2>{otp}</h2><br>You can safely ignore this email if you did not request for the OTP')
        return {'message':'otp generated successfully and saved', 'type':'success', 'Email':data['email'] }

@app.route('/auth/otp', methods = ['POST', 'GET'])
def otp():
    data = request.get_json()
    conn = get_db_connection()
    # fetch otp
    user = conn.execute("SELECT OTP FROM users WHERE Email=?",[data['email']]).fetchall()
    for use in user:
        dbotp = use['OTP']
    if dbotp!='':
        if data['otp'] != '':
            if(int(dbotp)==int(data['otp'])):
                return {'message':'otp matched', 'type':'success'}
            else:
                return {'message':'otp did not match', 'type':'error'}
    else:
        return {'message':'OTP not found in db please request for a new OTP', 'type':'error'}

@app.route('/auth/resset', methods = ['POST', 'GET'])
def resset():
    data = request.get_json()
    conn = get_db_connection()
    if data['password'] != data['cpassword']:
        return {'message':'passwords did not match!', 'type': 'error'}
    else:
        salt, password = hash_new_password(data['password'])
        conn.execute("UPDATE users SET Password=?, Salt=? Where Email=?",[password, salt, data['email']])
        conn.commit()
        conn.close()
        return {'message':'successfuly changed your password!', 'type':'success'}

@app.route('/contact', methods = ['POST', 'GET'])
def contact():
    data = request.get_json()
    fname = data['fname']
    lname = data['lname']
    email = data['email']
    brief = data['brief']
    # save data to database
    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO contact(Fname, Lname, Email, Brief) VALUES(?, ?, ?, ?)",(fname, lname, email, brief))
        conn.close()
        # send contact email
        sendEmail('New Message From Twitter Hate Crime Detection', 'admin@hatecrime.com', ['cynthiakiprotich2020@gmail.com', 'dennisrkibet@gmail.com'], f'From: {fname} {lname} <br>Email: {email} <br><h3>message</h3><br>{brief}')
        return {'type': 'success', 'message':'your message was successfully received'}
    except:
        return {'type':'error', 'message':'please try again'}

if __name__ == "__main__":
    app.run(debug=True)