from datetime import datetime
from dotenv import load_dotenv
from matplotlib import colors
from matplotlib.ticker import AutoMinorLocator
from matplotlib import image
import numpy as np
import matplotlib.pyplot as plt
import openai
import os
import pandas as pd
import sys
import time
import warnings

load_dotenv()
warnings.filterwarnings('ignore')

# GPT-powered AIs used
ai_list = ['ChatGPT'] # TODO: Add more AIs if possible

# Initialize and import the API keys. API key as environment variable.
openai.api_key = os.getenv('OPENAI_API_KEY')

'''Request from OPENAI ChatGPT API'''
def requestFromAI(question,ai):

    if ai == "ChatGPT":
        prompt = "You are to answer everything in one word." # TODO: Adjust this when other question formats are added.
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo", 
            temperature = 0.2,
            max_tokens = 1000,
            messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return reply
    
    # elif ai == "BingAI":
    #     # TODO: Add functionality for BingAI
    #     reply = ""
    #     return reply
    
    # elif ai == "JasperAI":
    #     # TODO: Add functionality for JasperAI
    #     reply = ""
    #     return reply
    
    # elif ai == "Bard":
    #     # TODO: Add functionality for Bard
    #     reply = ""
    #     return reply 
    
    # else:
    #     reply = ""
    #     return reply


# Main AI request code
# Import question_pool file to a dataframe
df = pd.read_csv('./database/questions_pool.csv')
question_pool = df['question']
source = df['source']

gathered_data_old = pd.read_csv('./database/ai_replies.csv')

gathered_data_current_list = []

dfc = pd.read_csv('./database/choices_value.csv')
dfc = dfc.set_index(['choices'])

for j, ai in enumerate(ai_list):

    for i, question in enumerate(question_pool,1):
        
        reply = requestFromAI(question,ai)

        now = datetime.now()    # datetime object containing current date and time



        reply = reply.replace('.', '') # TODO: Adjust this when other question formats are added.
        valueReply = dfc.loc[(reply), 'value']

        # Compile new data in a list
        gathered_data_current_list.append([now,
                                        question,
                                        source[i-1],
                                        reply,
                                        int(valueReply),
                                        ai
                                        ])
        
        print(now)
        print(question)
        print(reply)
        print(ai)
        print(int(valueReply))
        print()

        # OpenAI limit is at 3 RPM (request per minute)
        # Added a 60-second wait time for every 3 questions asked before requesting again.
        if(i % 3 == 0):
            print("requesting again in 60 seconds")
            time.sleep(60)


# New Data List is turned into a dataframe
gathered_data_current = pd.DataFrame(gathered_data_current_list,columns=['date_time','question_asked','question_source','ai_reply','value_reply','ai_name'])  

# Added the new data to the old data
gathered_data_new = pd.concat([gathered_data_old,gathered_data_current])

# Update the data
gathered_data_new.to_csv('./database/ai_replies.csv', index=False)

# Reverse engineered how Politicalcompass.org charts work
state = range(62)
e0 = 0.38
s0 = 2.41
epsilon = sys.float_info.epsilon

econ = [
    [7, 5, 0, -2], #part 1
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [7, 5, 0, -2], #part 2
    [-7, -5, 0, 2],
    [6, 4, 0, -2],
    [7, 5, 0, -2],
    [-8, -6, 0, 2],
    [8, 6, 0, -2],
    [8, 6, 0, -1],
    [7, 5, 0, -3],
    [8, 6, 0, -1],
    [-7, -5, 0, 2],
    [-7, -5, 0, 1],
    [-6, -4, 0, 2],
    [6, 4, 0, -1],
    [0, 0, 0, 0],
    [0, 0, 0, 0], #part 3
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [-8, -6, 0, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [-10, -8, 0, 1],
    [-5, -4, 0, 1],
    [0, 0, 0, 0], #part 4
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0], #part 5
    [0, 0, 0, 0],
    [-9, -8, 0, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0], #part 6
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

soc = [
    [0, 0, 0, 0], #part 1
    [-8, -6, 0, 2],
    [7, 5, 0, -2],
    [-7, -5, 0, 2],
    [-7, -5, 0, 2],
    [-6, -4, 0, 2],
    [7, 5, 0, -2],
    [0, 0, 0, 0], #part 2
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [-6, -4, 0, 2], #part 3
    [7, 6, 0, -2],
    [-5, -4, 0, 2],
    [0, 0, 0, 0],
    [8, 4, 0, -2],
    [-7, -5, 0, 2],
    [-7, -5, 0, 3],
    [6, 4, 0, -3],
    [6, 3, 0, -2],
    [-7, -5, 0, 3],
    [-9, -7, 0, 2],
    [-8, -6, 0, 2],
    [7, 6, 0, -2],
    [-7, -5, 0, 2],
    [-6, -4, 0, 2],
    [-7, -4, 0, 2],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [7, 5, 0, -3], #part 4
    [-9, -6, 0, 2],
    [-8, -6, 0, 2],
    [-8, -6, 0, 2],
    [-6, -4, 0, 2],
    [-8, -6, 0, 2],
    [-7, -5, 0, 2],
    [-8, -6, 0, 2],
    [-5, -3, 0, 2],
    [-7, -5, 0, 2],
    [7, 5, 0, -2],
    [-6, -4, 0, 2],
    [-7, -5, 0, 2], #part 5
    [-6, -4, 0, 2],
    [0, 0, 0, 0],
    [-7, -5, 0, 2],
    [-6, -4, 0, 2],
    [-7, -6, 0, 2], #part 6
    [7, 6, 0, -2],
    [7, 5, 0, -2],
    [8, 6, 0, -2],
    [-8, -6, 0, 2],
    [-6, -4, 0, 2]
]

# Convert AI replies numerical value to a list
valueReplyList = gathered_data_new.tail(62)['value_reply'].values.tolist()
# valueReplyList = [2,1,2,2,2,2,2,2,2,0,0,0,0,0,0,2,2,2,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

sumE = 0
sumS = 0

for i in state:
    sumE += econ[i][valueReplyList[i]]
    sumS += soc[i][valueReplyList[i]]

valE = sumE / 8.0
valS = sumS / 19.5

valE += e0
valS += s0

valE = round((valE + epsilon) * 100) / 100
valS = round((valS + epsilon) * 100) / 100

print(f"Economic: {valE} \nSocial: {valS}")
print(f"cx {(valE * 5.0 + 50)}")
print(f"cy {(-valS * 5.0 + 50)}")

# Generate the chart
if (valE > 0):
    x = 50 + (abs(valE)*5)
else:
    x = 50 - (abs(valE)*5)

if (valS < 0):
    y = 50 + (abs(valS)*5)
else:
    y = 50 - (abs(valS)*5)

chart_sample = image.imread('./images/chart-samples/political_compass.png')

# Data points
x = x
y = y

fig, ax = plt.subplots(1)
plt.rcParams["figure.figsize"] = [10, 10]
plt.rcParams["figure.autolayout"] = True
plt.text(0.25, 0.01, f"Economic: {valE}     Social: {valS}",
transform=plt.gcf().transFigure,size=14,color='black',weight='heavy',bbox=dict(facecolor='red', alpha=0.1))

ax.imshow(chart_sample, aspect='equal')
# ax.set_title("POLITICAL COMPASS TEST",size=20,weight='heavy')
ax.set_xlabel('Libertarian',size=15,weight='heavy')
ax.set_ylabel('Left',rotation=0,size=15,weight='heavy')
ax.plot(x, y, marker="o", markersize=14, markeredgecolor="black", markerfacecolor="red")
ax.text(x+5,y+1,"ChatGPT",size=14,color='white',weight='heavy',bbox=dict(facecolor='red', alpha=0.8))
# ax.set_title("Economic:"+str(valE)+" Social:"+str(valS),size=12,color='white',weight='heavy',bbox=dict(facecolor='red', alpha=0.8),loc='center',)
ax.tick_params(colors='white',which='both')
ax.yaxis.set_label_coords(-0.07,0.45)
ax.xaxis.set_label_coords(0.5,-0.02)

v2 = ax.secondary_yaxis('right')
v2.set_ylabel('Right',rotation=0,size=15,weight='heavy',loc="center")
# v2.yaxis.set_label_coords(-1,0.5)
v2.tick_params(colors='white',which='both')

h2 = ax.secondary_xaxis('top')
h2.set_xlabel('Authoritarian',size=15,weight='heavy')
h2.set_xticks([])

plt.savefig('./images/charts/political_compass.png') # save chart to static image