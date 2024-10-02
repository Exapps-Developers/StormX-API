from firebase_admin import credentials, firestore, initialize_app, messaging
from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)
cred = credentials.Certificate("key.json")
default_app = initialize_app(cred)
storedb = firestore.client()

def send_push_notification( device_tokens, title, body, data=None):

    message = messaging.Message(
        topic = device_tokens,
        notification = messaging.Notification(
            title = title,
            body = body
        ),
    )
    if data:
        message.data = data

    response = messaging.send(message)

    print("Successfully sent notification:", response)


#refs
posts_ref = storedb.collection('posts')
notifications_ref = storedb.collection('notifications')

@app.route('/')
def home():
    return "Storm-X API"

@app.route('/SendNotification',methods=['POST'])
def SendNotification():
    title = request.form.get('title')
    content = request.form.get('content')
    imgurl = request.form.get('imgurl')

    postref = posts_ref.document()

    Post = {
        'id': postref.id,
        'title': title,
        'content': content,
        'shares': 0,
        'submittedat': int(datetime.now().timestamp() * 1000),
        'sender': ["https://firebasestorage.googleapis.com/v0/b/exa-spacex.appspot.com/o/nasa-logo.png?alt=media&token=1118961f-ca8c-457a-b469-cf16aaf38127",'Nasa'],
        'imgurl': imgurl,
        'likes': [],
        'comments': {}
    }

    posts_ref.document(postref.id).set(Post)

    send_push_notification('news', title, content)
    return  jsonify("Notification Sent Successfully")

if __name__ == '__main__':
    os.system('cls')
    app.run(host="0.0.0.0",port=8000)
