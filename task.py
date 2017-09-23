#!/usr/bin/python

import os
import json
import re

path = "./data"
pronouns = ['HAN', 'HON', 'DEN', 'DET', 'DENNA', 'DENNE', 'HEN']
pronoun_count = dict.fromkeys(pronouns, 0)

fileList = os.listdir(path)
for file in fileList:
    print file
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
            text = json_object["text"]
            print text
            words = re.findall("[\w]+", text)
            for word in words:
                wordUpper = word.upper()
                if wordUpper in pronouns:
                    print word
                    pronoun_count[wordUpper] = pronoun_count[wordUpper] + 1 
            print retweet_count
        else:
            print retweet_count
            print json_object["retweeted"]
            continue
print pronoun_count

