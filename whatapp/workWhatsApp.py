from flask import Flask, request, jsonify
import requests
import sys
import os
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()

app = Flask(__name__)

# Replace the values here.
INSTANCE_URL = "https://instance-X.whatsapp.yapaytech.com"
API_KEY = ""
ADMIN_API_KEY = ""


@app.route("/")
def hello():
    return app.send_static_file("index.html")


def send_response(number, message):
    body = {'to': number, 'recipient_type': 'individual'}
    body.update(message)
    print('Request Body', body, file=sys.stdout)
    url = INSTANCE_URL + "/v1/messages"
    headers = {'Authorization': "Bearer "+API_KEY,
               'Content-Type': "application/json"}
    response = requests.post(url, json=body, headers=headers)
    print('Response', response.json(), file=sys.stdout)
    return


@app.route("/webhook", methods=['POST'])
def webhook():
    json_data = request.get_json()
    if 'messages' in json_data:
        # Handle Messages
        messages = json_data['messages']
        pprint(messages)
        contacts = ('contacts' in json_data) and json_data['contacts']
        user = contacts and contacts[0]
        wa_id = user['wa_id']
        profile = user['profile']
        print('Incoming Message From ' + wa_id, profile, file=sys.stdout)
        for ms in messages:
            ms_type = ms['type']
            if ms_type == 'text':
                text = ms['text']['body']
                print('Type:', ms_type, 'Text:', text, file=sys.stdout)
                send_response(
                    wa_id, {'type': 'text', 'text': {'body': 'Echo - '+text}})
            else:
                print('Ignored Message Type:', ms_type, ms, file=sys.stdout)

    if 'statuses' in json_data:
        statuses = json_data['statuses']
        # Handle Status Changes
        print(statuses, file=sys.stdout)
    return jsonify({'success': True}), 200



@app.route('/receive_msg', methods=['POST','GET'])
def webhook():
   if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
       if not request.args.get("hub.verify_token")== "YOUR VARIFICATION TOKEN":
           return "Verification token missmatch", 403
       return request.args['hub.challenge'], 200
   return "Hello world", 200

def setup_webhook():
    # public_url = ngrok.connect(9000)
    # public_url = ngrok.connect(9000)
    public_url = public_url.replace("http", "https", 1)
    print('Public Url '+public_url, file=sys.stdout)
    url = INSTANCE_URL + "/v1/settings/application"
    headers = {'Authorization': "Bearer "+ADMIN_API_KEY,
               'Content-Type': "application/json"}
    body = {'webhooks': {'url': public_url+'/webhook'}}
    response = requests.patch(url, json=body, headers=headers)
    print(response.json(), file=sys.stdout)

# Do not use this method in your production environment
# setup_webhook()