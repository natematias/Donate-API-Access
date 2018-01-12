'''
flask-tweepy-oauth

an example showing how to authorize a twitter application
in python with flask and tweepy.

Updated from Kawan's original script at:
find me on github at github.com/whichlight

J. Nathan Matias

To set up, make a local copy of the config/env.json file such as development.json

Then set CS_ENV=development to specify which environment to run in

'''

from flask import Flask
from flask import request
from flask import session
import flask 
import tweepy
import simplejson as json
import os
app = Flask(__name__)

ENV = os.environ['CS_ENV']

config = json.loads(open(os.path.join("config",ENV+".json"),"r").read())

app.secret_key = config['secret_key']

CONSUMER_TOKEN=config['consumer_token']
CONSUMER_SECRET=config['consumer_secret']
CALLBACK_URL = 'http://civictechai.media.mit.edu:5010/verify'
db = {}#dict() #you can save these values to a database

@app.route("/")
def send_token():
  auth = tweepy.OAuthHandler(CONSUMER_TOKEN, 
    CONSUMER_SECRET, 
    CALLBACK_URL)
  
  try: 
    #get the request tokens
    link_url= auth.get_authorization_url()
    session['request_token']= (auth.request_token['oauth_token'],
      auth.request_token['oauth_token_secret'])
  except tweepy.TweepError:
    print('Error! Failed to get request token')
  
  return flask.render_template('welcome.html', link=link_url)

  #this is twitter's url for authentication
  #return flask.redirect(redirect_url)  

@app.route("/verify")
def get_verification():
  
  #get the verifier key from the request url
  verifier= request.args['oauth_verifier']
  
  auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
  token = session['request_token']
  auth.request_token = {"oauth_token":session['request_token'][0],
                        "oauth_token_secret": session['request_token'][1]}
  del session['request_token']
  #auth.set_request_token(token[0], token[1])

  try:
        auth.get_access_token(verifier)
#  auth.get_access_token(verifier)

  except tweepy.TweepError:
        print('Error! Failed to get access token.')
  
  #now you have access!
  api = tweepy.API(auth)
  username = api.auth.get_username()
  user = api.get_user(api.auth.username)
  
  output_dict = {"username":username,
                 "user_id":user.id,
                  "oauth_token":api.auth.access_token,
                  "oauth_token_secret":api.auth.access_token_secret}
  with open(os.path.join("keys",username+".json"), "w") as f:
    f.write(json.dumps(output_dict))

  session['username'] = username

  ## ARCHIVE TO A NEW FILE
  return flask.redirect(flask.url_for('success'))

@app.route("/success")
def success():
  #auth done, app logic can begin
  return flask.render_template('success.html', username=session['username'])

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5010)#debug=True)
  #app.run()

