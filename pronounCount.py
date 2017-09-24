#!/usr/bin/python

import os
import json
import re

from flask import Flask
from celery import Celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'amqp://localhost:637970'

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
        self.update_state(state='PROGRESS', 
                          meta={'pronoun_count': pronoun_count,
                                'unique_retweets': unique_retweets})    
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
    return {'pronoun_count': pronoun_count, 'unique_retweets': unique_retweet}

@app.route('/task_pronoun_count', methods=['POST'])
def task_pronoun_count():
    task = fun_pronoun_count()
    return jsonify({}), 202, {'Location': url_for('taskstatus', task_id = task.id)}

@app.route('/status/<task_id>')
def taskstatus(task_id):
    pronouns = ['HAN', 'HON', 'DEN', 'DET', 'DENNA', 'DENNE', 'HEN']
    pronoun_count = dict.fromkeys(pronouns, 0)
    unique_retweets = 0

    task = fun_pronoun_count.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = { 'state': task.state, 
                     'pronoun_count': pronoun_count, 
                     'unique_retweets': unique_retweet,
                     'status' : 'Pending...' }
    elif task.state != 'FAILURE':
        response = { 'state': task.state, 'status': task.info.get('status', '') }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = { 'state': task.state,
                     'pronoun_count': pronoun_count, 
                     'unique_retweets': unique_retweet,
                     'status': str(task.info) }
    return jsonify(response)

        
#pronoun_count, unique_retweets = fun_pronoun_count()
#print pronoun_count
#print unique_retweets

if __name__ == '__main__':
    app.run(debug=True)
