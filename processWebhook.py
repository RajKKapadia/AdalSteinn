import flask
import requests
import json
import os

app = flask.Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return "Hello World"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():

    req = flask.request.get_json(force=True)
    action = req.get('queryResult').get('action')

    if action == "DefaultFallbackIntent.DefaultFallbackIntent-yes":
        headers = {'Content-type': 'application/json'}
        API_KEY = os.environ.get("API_KEY")
        url = "https://graph.facebook.com/v2.6/me/pass_thread_control?access_token="+API_KEY
        PSID = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
        payload = {"recipient":{"id":str(PSID)},
                   "target_app_id":263902037430900,
                   "metadata":"String to pass to secondary receiver app"}
        data = requests.post(url, data=json.dumps(payload), headers=headers)
        if data.status_code == 200:
            response = {'fulfillmentText':"From webhook"}
        else:
            response = {'fulfillmentText':"did not get good response"}

    return flask.make_response(flask.jsonify(response))

if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    app.debug = True
    app.run()
