#!/usr/bin/python

import os
import json
import re

from flask import Flask, jsonify
from celery import Celery


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://jimmy:jimmy123@localhost/jimmy_vhost'
app.config['CELERY_RESULT_BACKEND'] = 'amqp://jimmy:jimmy123@localhost/jimmy_vhost'
celery = Celery(app.name, 
                broker=app.config['CELERY_BROKER_URL'], 
                backend=app.config['CELERY_RESULT_BACKEND'])

@celery.task(bind=True)
def fun_pronoun_count(self):
    path = "./data"
    pronouns = ['HAN', 'HON', 'DEN', 'DET', 'DENNA', 'DENNE', 'HEN']
    pronoun_count = dict.fromkeys(pronouns, 0)
    unique_retweets = 0

    fileList = os.listdir(path)
    for file in fileList:
        #print file
        lines = open(path + "/" + file, 'r')
        
        for line in lines:
            try:
                json_object = json.loads(line)
            except:
                if line == '\n':
                    continue
                else:
                    break #EOF
        
            #print json_object
            retweet_count = int(json_object["retweet_count"])
            if retweet_count == 0:
                unique_retweets = unique_retweets + 1
                text = json_object["text"]
                #print text
                words = re.findall("[\w]+", text)
                for word in words:
                    wordUpper = word.upper()
                    if wordUpper in pronouns:
                        #print word
                        pronoun_count[wordUpper] = pronoun_count[wordUpper] + 1
                #print retweet_count
            #else:
            #    print retweet_count
            #    print json_object["retweeted"]
            #    continue
    print pronoun_count
    print unique_retweets
    return {'pronoun_count': pronoun_count, 'unique_retweets' : unique_retweets}

@app.route('/task_pronoun_count', methods=['GET'])
def task_pronoun_count():
    return jsonify(fun_pronoun_count())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
