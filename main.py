#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
import json
import sys
import requests as R

import firebase_admin
from firebase_admin import db
import facebook


app = Flask(__name__)
ACCESS_TOKEN = 'EAAbysoLqFlMBADTYl25Wc8ZBFlyCxpT8iU2qzZBYH2GPb8XN9nUqrFgf2Y09l7fVYe0ZA3VFoAiA6QdVID2JVoKKcZAM7TI60VZAmFmKhHgNbqH1iiIwbisIPUzR8NRimnJ5CZBLSJdH0WldPrZCw8C8Yrn13wDVFIfZATn5Gt2gtgZDZD'
VERIFY_TOKEN = 'ITEC_LOMBOK'

graph = facebook.GraphAPI(access_token=ACCESS_TOKEN)

bot = Bot(ACCESS_TOKEN)

firebase_admin.initialize_app(options={
    'databaseURL': 'https://itec-training.firebaseio.com/'
})

db_member = db.reference('members')

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

@app.route("/", methods=['GET', 'POST'])
def terima_pesan():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
        for ent in output.get('entry'): 
           if ent is not None:
                for item in ent.get('messaging'):
                    sender = item.get('sender').get('id')
                    sys.stderr.write("messaging: " + json.dumps(item))
                    if item.get('message') is not None:
                        text = item.get('message').get('text')
                        if (text is not None):
                            setProcessText(sender, text)
                        elif item.get('message').get('attachments') is not None:
                            for atch in item.get('message').get('attachments'):
                                if atch.get('payload') is not None:
                                    url = atch.get('payload').get('url')
                                    setProcessText(sender, '', attachment=url)
                    if item.get('postback') is not None:
                        payload = item.get('postback').get('payload')
                        text = item.get('postback').get('title')
                        processPayload(sender, payload, text)
    return 'Message processed'

def setProcessText(sender, text, attachment=None):
    bot.send_text_message(sender, 'unknown command ' + text)
    showMemberButton(sender)

def showMemberButton(sender):
    buttons = []
    mmbr = db_member.get()
    if mmbr is None or mmbr.get(sender) is None:
        buttons.append({
                "type": "postback",
                "title": "Register",
                "payload": 'REGISTER'
            })
    else:
        buttons.append( {
                    "type": "postback",
                    "title": "List Member",
                    "payload": 'MEMBERS'
                })
        buttons.append({
                    "type": "postback",
                    "title": "Upcoming Events",
                    "payload": 'EVENTS'
                })

        buttons.append({
                    "type": "postback",
                    "title": "Freebies",
                    "payload": 'FREE'
                })
    bot.send_button_message(sender,'Please select any actions', buttons)
    
def processPayload(sender, payload, text):
    if payload == 'FREE':
        bot.send_text_message(sender, 'Come again next time, our creeps currently finding some gold to buys some goodies for you...')
    if payload == 'EVENTS':
        bot.send_text_message(sender, 'Sorry, its not possible at this times...')
        # args = {'fields' : 'id,name', }
        # events = graph.get_object('me/events')
        # sys.stderr.write("JSON: " + json.dumps(events))
        # if len(events.get('data')) == 0:
        #     bot.send_text_message(sender, 'No event available at this time...')
        # else:
        #     for ev in events.get('data'):
        #         bot.send_text_message(sender, 'Event: ' + ev.get('name'))
    if payload == 'START':
        args = {'fields' : 'id,name', }
        profile = graph.get_object(sender, **args)
        bot.send_text_message(sender, 'hi ' + profile.get('name'))
        bot.send_text_message(sender, 'Welcome to Lombok Dev, the most awesome community in Lombok')

    if payload == 'REGISTER':
        args = {'fields' : 'id,name', }
        profile = graph.get_object(sender, **args)
        db_member.child(profile.get('id')).set(profile.get('name'))
        bot.send_text_message(sender, 'hi ' + profile.get('name') + ', you have been registered as Lombok Dev Member. ')
        bot.send_text_message(sender, 'Any updates about events and challenge will be directly send to your messanger.')

    if payload == 'MEMBERS':
        mmbr = db_member.get()
        bot.send_text_message(sender, 'Lombok DEV members:')
        i = 1
        for key, val in mmbr.items():
            bot.send_text_message(sender, str(i) + '. ' + val)
        bot.send_text_message(sender, '======')

    showMemberButton(sender)


if __name__ == "__main__":
    app.run()
