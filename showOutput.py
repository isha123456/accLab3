#!/usr/bin/python

import re
import sys
import matplotlib.pyplot as plt
import numpy as np

fileName = raw_input('Enter name of output file with results you want to plot:' )
print 'Scanning ', fileName

fd = open(fileName, 'r')
content = fd.read()
#print content
pronouns = ['HAN', 'HON', 'DEN', 'DET', 'DENNA', 'DENNE', 'HEN']
pronoun_count = dict.fromkeys(pronouns, 0)
unique_retweets = 0

for word in pronouns:
    target = re.findall("\"" + word + "\":\s+(\d+)", content)
    number = int(target[0])
    print word, number
    pronoun_count[word] = number

target = re.findall("\"unique_retweets\":\s+(\d+)", content)
unique_retweets = int(target[0])
print unique_retweets
labels = [str(i) for i in pronoun_count.values()]
#print labels

plt.rcdefaults()
fig=plt.figure(figsize=(12,6))
y_pos=np.arange(len(pronoun_count.keys()))
rects = plt.bar(y_pos, pronoun_count.values(), align='center', alpha=1, tick_label=labels)
plt.xticks(y_pos, pronoun_count.keys())
plt.ylabel('Number of occurences')
plt.title('Number of occurences of some Swedish pronouns in unique tweets in https://uppsala.box.com/s/qiiggdjd98241wm7rl3lqehfhyjomg4y')
ax = plt.gca()

for rect in rects:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., 1.01*height,
            str(int(height)),
            ha='center', va='bottom')

fig.text(0.1, 0.01, 'Number of unique tweets = ' + str(unique_retweets))
plt.savefig("result.png")
plt.show()
