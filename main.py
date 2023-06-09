from datetime import datetime
from random import randrange
from dotenv import load_dotenv
from matplotlib import image
import matplotlib.pyplot as plt
import pandas as pd

from Bard import Chatbot as bard
from hugchat import hugchat
import poe
import openai
from g4f import you
from g4f import deepai
from g4f import forefront
from revChatGPT.V1 import Chatbot as chatgpt4
from OpenAIAuth import Auth0
from freeGPT import gpt3 as you3
from freeGPT import gpt4 as forefront3
from freeGPT import alpaca_7b as chatllama

import os, sys, time, warnings, pytz, re

load_dotenv()
warnings.filterwarnings('ignore')

start = time.time() # Measuring time it takes to get all request

# Set-up AIs
ai_list = ['Bard',
           'HugChat',
           'ChatGPT',
           'ChatGPT-4',
           'Deep AI',
           'Alpaca 7B'
        #    'Claude',
        #    'Sage',
        #    'YouChat Free',
        #    'YouChat',
        #    'Forefront'
           ] 

# TODO: Add more AIs if possible
# TODO: Bing restricts its answers and switches to new topic when introduced a restricted topic.
# UPDATE: Dragonfly and NeevaAI are deprecated.

# Set-up API Keys and Tokens
openai.api_key = os.getenv('OPENAI_API_KEY')
huggingChat = hugchat.ChatBot(cookie_path="cookies_hugchat.json")
bard_token = os.getenv('BARD_TOKEN')
poe_token = os.getenv('POE_TOKEN')
poe_token2 = os.getenv('POE_TOKEN4')
gpt4_email = os.getenv('OPENAI_GPT4_EMAIL')
gpt4_password = os.getenv('OPENAI_GPT4_PASSWORD')
gpt4_auth = Auth0(email=gpt4_email, password=gpt4_password)
gpt4_access_token = gpt4_auth.auth()

def requestFromAI(question,ai):

    if ai == "ChatGPT":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo", 
            temperature = 0,
            max_tokens = 1000,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0,
            messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return reply
    
    elif ai == "Bing Chat":
        # TODO: Add functionality for BingAI
        reply = ""
        print(reply)

    elif ai == "Bard":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        chatbot = bard(bard_token)
        response = chatbot.ask(f'{prompt} {question}')
        reply = response['content']
        return reply
    
    elif ai == "HugChat":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        response = huggingChat.chat(
            text=f'{prompt} {question}',
            temperature=0.5,
            top_p=0.5,
            repetition_penalty=1,
            top_k=50
            )
        reply=response
        return reply
    
    elif ai == "Claude":        
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        client = poe.Client(poe_token)
        for chunk in client.send_message("a2", f'{prompt} {question}', with_chat_break=True, timeout=60):
            response = chunk["text"]
        reply=response
        timer = randrange(100, 120)
        print(f'Waiting {timer} seconds before another request...')
        time.sleep(timer)
        return reply

    elif ai == "Sage":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        client = poe.Client(poe_token)
        for chunk in client.send_message("capybara", f'{prompt} {question}', with_chat_break=True, timeout=60):
            response = chunk["text"]
        reply=response
        timer = randrange(100, 120)
        print(f'Waiting {timer} seconds before another request...')
        time.sleep(timer)
        return reply
    
    elif ai == "YouChat":
    # TODO: Re-add YouChat
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        response = you.Completion.create(
            prompt=f'{prompt} {question}',
            detailed=True,
            include_links=True, )
        reply = response.dict()
        reply = reply['text']
        return reply
    
    elif ai == "ChatGPT-4":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        chatbot = chatgpt4(config={
            "access_token": gpt4_access_token
            })
        response = ""
        for data in chatbot.ask(prompt=f'{prompt} {question}',
                                conversation_id='55cf6e4f-15f0-46d4-bf39-5b4d3770bef8', # Continue conversation in 'AI Spectrum Test' Chat
                                parent_id='076cc04a-567f-42e3-974c-36bd3de2dc78',
                                model='gpt-4', # gpt-4-browsing, text-davinci-002-render-sha, gpt-4, gpt-4-plugins
                                ):
            response = data["message"]
        reply = response
        timer = randrange(432,435) # Wait for 432 seconds every request. Totaling to 25 requests every 3 hours.
        print(f'Waiting {timer} seconds before another request...')
        time.sleep(timer)
        return reply

    elif ai == 'Deep AI':
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"

        response = []
        for chunk in deepai.Completion.create(f'{prompt} {question}'):
            response.append(chunk)
        reply = ''.join(response)
        return reply
    
    elif ai == 'Forefront':
    # TODO: Re-add Forefront
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        print('Not yet implemented')

    elif ai == 'Alpaca 7B':
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        response = chatllama.Completion.create(prompt=f'{prompt} {question}')
        reply = response
        return reply
    
    elif ai == 'YouChat Free':
    # TODO: Re-add YouChat
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        response = you3.Completion.create(prompt=f'{prompt} {question}')
        reply = response['text']
        return reply

# Main AI request code
df = pd.read_csv('./database/questions_pool.csv')
question_pool = df['question']
source = df['source']

gathered_data_old = pd.read_csv('./database/ai_replies.csv')

gathered_data_current_list = []

dfc = pd.read_csv('./database/choices_value.csv')
dfc = dfc.set_index(['choices'])

for j, ai in enumerate(ai_list):

    for i, question in enumerate(question_pool,1):
        
        while True:
            try:
                reply = requestFromAI(question,ai)

                # Log Date and Time
                tz_NY = pytz.timezone('America/New_York') 
                datetime_NY = datetime.now(tz_NY)
                now = datetime_NY.strftime("%m/%d/%Y %H:%M:%S")

                reply = reply.strip()
                reply = re.sub(r"[^a-zA-Z0-9\s]+", "", reply) # TODO: Adjust this when other question formats are added.
                reply = reply.title()

                valueReply = dfc.loc[(reply), 'value']

                # Compile new data in a list
                gathered_data_current_list.append([now,
                                                   question,
                                                   source[i-1],
                                                   reply,
                                                   int(valueReply),
                                                   ai
                                                   ])
                print(i)
                print(now)
                print(question)
                print(reply)
                print(ai)
                print(int(valueReply))
                print()

                # # Added a 60-second wait time for every 3 questions asked before requesting again to prevent timeout error.
                # if(i % 3 == 0):
                #     print("Requesting again in 60 seconds")
                #     time.sleep(60)

            except Exception as e:
                delay = 60
                print(f"ERROR: {e}")
                print(f"RETRY: {question}")
                print(f"Retrying in {delay} seconds...")
                print()
                time.sleep(delay)
                continue
            else:
                break

print("AI API Requests: DONE")

# New Data List is turned into a dataframe
gathered_data_current = pd.DataFrame(gathered_data_current_list,columns=['date_time','question_asked','question_source','ai_reply','value_reply','ai_name'])  

# Added the new data to the old data
gathered_data_new = pd.concat([gathered_data_old,gathered_data_current])

# Update the data
gathered_data_new.to_csv('./database/ai_replies.csv', index=False)

print("Update AI Replies: DONE")

# Get last update date and time; changed dataframe name to not be confused with gathered_data_new
df_last_update = pd.read_csv('./database/ai_replies.csv')
timezone = datetime_NY.strftime("%Z")
df_last_update['date_time'] = pd.to_datetime(df_last_update['date_time']).dt.strftime(f'%I:%M%p {timezone} on %B %d, %Y')
last_updated = df_last_update['date_time'].tail(1)

# Save to txt file
path = r'./last_updated.txt'
with open(path, 'w') as f:
    df_string = last_updated.to_string(header=False, index=False)
    f.write(df_string)

print("Update Last Updated DateTime: DONE")

# Get latest update date and time for each AI
ai_latest_updates = []
for ai in ai_list:
    df_ai_update = pd.read_csv('./database/ai_replies.csv')
    df_ai_updates = df_ai_update[df_ai_update["ai_name"] == ai]
    df_ai_updates['date_time'] = pd.to_datetime(df_ai_updates['date_time']).dt.strftime(f'%I:%M%p {timezone} on %B %d, %Y')
    last_updated = df_ai_updates['date_time'].tail(1).to_string(header=False, index=False)
    ai_latest_updates.append(f'{ai}: {last_updated}')

# Save the latest updates to ai_last_update.txt
path = r'./ai_last_update.txt'
with open(path, 'w') as f:
    f.write('\n'.join(ai_latest_updates))

print("Update AI Last Updated DateTime: DONE")

# Political Compass Chart
data_point_list = []

for ai in ai_list:

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
    filtered_gathered_data_new = gathered_data_new[(gathered_data_new['ai_name'] == ai)]
    valueReplyList = filtered_gathered_data_new.tail(62)['value_reply'].values.tolist()
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

    # Generate the chart
    if (valE > 0):
        x = 50 + (abs(valE)*5)
    else:
        x = 50 - (abs(valE)*5)

    if (valS < 0):
        y = 50 + (abs(valS)*5)
    else:
        y = 50 - (abs(valS)*5)

    # Data points
    x = x
    y = y

    # Save new coords to coords log. It is used for the time series chart
    df_coord = pd.read_csv('./database/ai_replies.csv')
    df_coords = df_coord[df_coord["ai_name"]==ai]
    date_time_coords = df_coords['date_time'].tail(1).values.tolist()[0]
    test_coords = df_coords['question_source'].tail(1).values.tolist()[0]
    ai_name_coords = ai

    coords_data_old = pd.read_csv('./database/coordinates_logs.csv')
    coords_data_current_list = []

    coords_data_current_list.append([date_time_coords,
                                    valE,
                                    valS,
                                    test_coords,
                                    ai_name_coords
                                    ])

    coords_data_current = pd.DataFrame(coords_data_current_list, columns=['date_time','econ_value','soc_value','test_source','ai_name'])
    coords_data_new = pd.concat([coords_data_old, coords_data_current])

    coords_data_new.to_csv('./database/coordinates_logs.csv', index=False)

    print("Update Coords Logs: DONE")

    data_point_list.append([valE,
                            valS,
                            x,
                            y,
                            ai
                            ])
    

chart_data_points = pd.DataFrame(data_point_list, columns=['valE','valS','x','y','ai_name'])

chart_sample = image.imread('./images/chart-samples/political_compass.png')

fig, ax = plt.subplots(1)
plt.rcParams["figure.figsize"] = [10, 10]
plt.rcParams["figure.autolayout"] = True
# plt.text(0.25, 0.01, f"Economic: {valE}     Social: {valS}",
#          transform=plt.gcf().transFigure,size=14,color='black',weight='heavy',bbox=dict(facecolor='red', alpha=0.1))

ax.imshow(chart_sample, aspect='equal')
# ax.set_title("POLITICAL COMPASS TEST",size=20,weight='heavy')
ax.set_xlabel('Libertarian',size=15,weight='heavy')
ax.set_ylabel('Left',rotation=0,size=15,weight='heavy')

#Plot CHATGPT
ax.plot(chart_data_points[(chart_data_points['ai_name']=='ChatGPT')]['x'].values.tolist()[0],
        chart_data_points[(chart_data_points['ai_name']=='ChatGPT')]['y'].values.tolist()[0],
        marker="o", markersize=10, markeredgecolor="black", markerfacecolor="green")
# ax.text(chart_data_points[(chart_data_points['ai_name']=='ChatGPT')]['x'].values.tolist()[0]+5,
#         chart_data_points[(chart_data_points['ai_name']=='ChatGPT')]['y'].values.tolist()[0]+1,
#         chart_data_points[(chart_data_points['ai_name']=='ChatGPT')]['ai_name'].values.tolist()[0],
#         size=14,color='white',weight='heavy',bbox=dict(facecolor='green', alpha=0.8))
ax.annotate(chart_data_points[(chart_data_points['ai_name']=='ChatGPT')]['ai_name'].values.tolist()[0],
            xy=(chart_data_points[(chart_data_points['ai_name']=='ChatGPT')]['x'].values.tolist()[0],
                chart_data_points[(chart_data_points['ai_name']=='ChatGPT')]['y'].values.tolist()[0]),
            xycoords='data',
            xytext=(chart_data_points[(chart_data_points['ai_name']=='ChatGPT')]['x'].values.tolist()[0]+20, 
                    chart_data_points[(chart_data_points['ai_name']=='ChatGPT')]['y'].values.tolist()[0]-10), 
            textcoords='data',
            size=14, 
            va="center", 
            ha="center",
            color='w',
            weight='heavy',
            bbox=dict(boxstyle="round4", 
                      fc="g"),
            arrowprops=dict(arrowstyle="simple",
                            connectionstyle="arc3,rad=0",
                            fc='g'),
            )

#Plot Bard
ax.plot(chart_data_points[(chart_data_points['ai_name']=='Bard')]['x'].values.tolist()[0],
        chart_data_points[(chart_data_points['ai_name']=='Bard')]['y'].values.tolist()[0],
        marker="o", markersize=10, markeredgecolor="black", markerfacecolor="red")
# ax.text(chart_data_points[(chart_data_points['ai_name']=='Bard')]['x'].values.tolist()[0]+5,
#         chart_data_points[(chart_data_points['ai_name']=='Bard')]['y'].values.tolist()[0]+1,
#         chart_data_points[(chart_data_points['ai_name']=='Bard')]['ai_name'].values.tolist()[0],
#         size=14,color='white',weight='heavy',bbox=dict(facecolor='red', alpha=0.8))

ax.annotate(chart_data_points[(chart_data_points['ai_name']=='Bard')]['ai_name'].values.tolist()[0],
            xy=(chart_data_points[(chart_data_points['ai_name']=='Bard')]['x'].values.tolist()[0],
                chart_data_points[(chart_data_points['ai_name']=='Bard')]['y'].values.tolist()[0]),
            xycoords='data',
            xytext=(chart_data_points[(chart_data_points['ai_name']=='Bard')]['x'].values.tolist()[0]-15, 
                    chart_data_points[(chart_data_points['ai_name']=='Bard')]['y'].values.tolist()[0]+5), 
            textcoords='data',
            size=14, 
            va="center", 
            ha="center",
            color='w',
            weight='heavy',
            bbox=dict(boxstyle="round4", 
                      fc="r"),
            arrowprops=dict(arrowstyle="simple",
                            connectionstyle="arc3,rad=0",
                            fc='r'),
            )

#Plot HugChat
ax.plot(chart_data_points[(chart_data_points['ai_name']=='HugChat')]['x'].values.tolist()[0],
        chart_data_points[(chart_data_points['ai_name']=='HugChat')]['y'].values.tolist()[0],
        marker="o", markersize=10, markeredgecolor="black", markerfacecolor="orange")
# ax.text(chart_data_points[(chart_data_points['ai_name']=='HugChat')]['x'].values.tolist()[0]+5,
#         chart_data_points[(chart_data_points['ai_name']=='HugChat')]['y'].values.tolist()[0]+1,
#         chart_data_points[(chart_data_points['ai_name']=='HugChat')]['ai_name'].values.tolist()[0],
#         size=14,color='white',weight='heavy',bbox=dict(facecolor='orange', alpha=0.8))

ax.annotate(chart_data_points[(chart_data_points['ai_name']=='HugChat')]['ai_name'].values.tolist()[0],
            xy=(chart_data_points[(chart_data_points['ai_name']=='HugChat')]['x'].values.tolist()[0],
                chart_data_points[(chart_data_points['ai_name']=='HugChat')]['y'].values.tolist()[0]),
            xycoords='data',
            xytext=(chart_data_points[(chart_data_points['ai_name']=='HugChat')]['x'].values.tolist()[0]+20, 
                    chart_data_points[(chart_data_points['ai_name']=='HugChat')]['y'].values.tolist()[0]+5), 
            textcoords='data',
            size=14, 
            va="center", 
            ha="center",
            color='w',
            weight='heavy',
            bbox=dict(boxstyle="round4", 
                      fc="orange"),
            arrowprops=dict(arrowstyle="simple",
                            connectionstyle="arc3,rad=0",
                            fc='orange'),
            )

# #Plot Claude
# ax.plot(chart_data_points[(chart_data_points['ai_name']=='Claude')]['x'].values.tolist()[0],
#         chart_data_points[(chart_data_points['ai_name']=='Claude')]['y'].values.tolist()[0],
#         marker="o", markersize=10, markeredgecolor="black", markerfacecolor="brown")
# # ax.text(chart_data_points[(chart_data_points['ai_name']=='Claude')]['x'].values.tolist()[0]-2,
# #         chart_data_points[(chart_data_points['ai_name']=='Claude')]['y'].values.tolist()[0]-10,
# #         chart_data_points[(chart_data_points['ai_name']=='Claude')]['ai_name'].values.tolist()[0],
# #         size=14,color='white',weight='heavy',bbox=dict(facecolor='brown', alpha=0.8))

# ax.annotate(chart_data_points[(chart_data_points['ai_name']=='Claude')]['ai_name'].values.tolist()[0],
#             xy=(chart_data_points[(chart_data_points['ai_name']=='Claude')]['x'].values.tolist()[0],
#                 chart_data_points[(chart_data_points['ai_name']=='Claude')]['y'].values.tolist()[0]),
#             xycoords='data',
#             xytext=(chart_data_points[(chart_data_points['ai_name']=='Claude')]['x'].values.tolist()[0]-10, 
#                     chart_data_points[(chart_data_points['ai_name']=='Claude')]['y'].values.tolist()[0]-20), 
#             textcoords='data',
#             size=14, 
#             va="center", 
#             ha="center",
#             color='w',
#             weight='heavy',
#             bbox=dict(boxstyle="round4", 
#                       fc="brown"),
#             arrowprops=dict(arrowstyle="simple",
#                             connectionstyle="arc3,rad=0",
#                             fc='brown'),
#             )

# #Plot Sage
# ax.plot(chart_data_points[(chart_data_points['ai_name']=='Sage')]['x'].values.tolist()[0],
#         chart_data_points[(chart_data_points['ai_name']=='Sage')]['y'].values.tolist()[0],
#         marker="o", markersize=10, markeredgecolor="black", markerfacecolor="violet")
# # ax.text(chart_data_points[(chart_data_points['ai_name']=='Sage')]['x'].values.tolist()[0]-20,
# #         chart_data_points[(chart_data_points['ai_name']=='Sage')]['y'].values.tolist()[0]+1,
# #         chart_data_points[(chart_data_points['ai_name']=='Sage')]['ai_name'].values.tolist()[0],
# #         size=14,color='white',weight='heavy',bbox=dict(facecolor='violet', alpha=0.8))

# ax.annotate(chart_data_points[(chart_data_points['ai_name']=='Sage')]['ai_name'].values.tolist()[0],
#             xy=(chart_data_points[(chart_data_points['ai_name']=='Sage')]['x'].values.tolist()[0],
#                 chart_data_points[(chart_data_points['ai_name']=='Sage')]['y'].values.tolist()[0]),
#             xycoords='data',
#             xytext=(chart_data_points[(chart_data_points['ai_name']=='Sage')]['x'].values.tolist()[0]-20, 
#                     chart_data_points[(chart_data_points['ai_name']=='Sage')]['y'].values.tolist()[0]+5), 
#             textcoords='data',
#             size=14, 
#             va="center", 
#             ha="center",
#             color='w',
#             weight='heavy',
#             bbox=dict(boxstyle="round4", 
#                       fc="violet"),
#             arrowprops=dict(arrowstyle="simple",
#                             connectionstyle="arc3,rad=0",
#                             fc='violet'),
#             )

# #Plot YouChat
# ax.plot(chart_data_points[(chart_data_points['ai_name']=='YouChat')]['x'].values.tolist()[0],
#         chart_data_points[(chart_data_points['ai_name']=='YouChat')]['y'].values.tolist()[0],
#         marker="o", markersize=10, markeredgecolor="black", markerfacecolor="blue")
# # ax.text(chart_data_points[(chart_data_points['ai_name']=='Sage')]['x'].values.tolist()[0]-20,
# #         chart_data_points[(chart_data_points['ai_name']=='Sage')]['y'].values.tolist()[0]+1,
# #         chart_data_points[(chart_data_points['ai_name']=='Sage')]['ai_name'].values.tolist()[0],
# #         size=14,color='white',weight='heavy',bbox=dict(facecolor='violet', alpha=0.8))

# ax.annotate(chart_data_points[(chart_data_points['ai_name']=='YouChat')]['ai_name'].values.tolist()[0],
#             xy=(chart_data_points[(chart_data_points['ai_name']=='YouChat')]['x'].values.tolist()[0],
#                 chart_data_points[(chart_data_points['ai_name']=='YouChat')]['y'].values.tolist()[0]),
#             xycoords='data',
#             xytext=(chart_data_points[(chart_data_points['ai_name']=='YouChat')]['x'].values.tolist()[0]-20, 
#                     chart_data_points[(chart_data_points['ai_name']=='YouChat')]['y'].values.tolist()[0]+5), 
#             textcoords='data',
#             size=14, 
#             va="center", 
#             ha="center",
#             color='w',
#             weight='heavy',
#             bbox=dict(boxstyle="round4", 
#                       fc="blue"),
#             arrowprops=dict(arrowstyle="simple",
#                             connectionstyle="arc3,rad=0",
#                             fc='blue'),
#             )

#Plot ChatGPT-4
ax.plot(chart_data_points[(chart_data_points['ai_name']=='ChatGPT-4')]['x'].values.tolist()[0],
        chart_data_points[(chart_data_points['ai_name']=='ChatGPT-4')]['y'].values.tolist()[0],
        marker="o", markersize=10, markeredgecolor="black", markerfacecolor="blue")
# ax.text(chart_data_points[(chart_data_points['ai_name']=='Sage')]['x'].values.tolist()[0]-20,
#         chart_data_points[(chart_data_points['ai_name']=='Sage')]['y'].values.tolist()[0]+1,
#         chart_data_points[(chart_data_points['ai_name']=='Sage')]['ai_name'].values.tolist()[0],
#         size=14,color='white',weight='heavy',bbox=dict(facecolor='violet', alpha=0.8))

ax.annotate(chart_data_points[(chart_data_points['ai_name']=='ChatGPT-4')]['ai_name'].values.tolist()[0],
            xy=(chart_data_points[(chart_data_points['ai_name']=='ChatGPT-4')]['x'].values.tolist()[0],
                chart_data_points[(chart_data_points['ai_name']=='ChatGPT-4')]['y'].values.tolist()[0]),
            xycoords='data',
            xytext=(chart_data_points[(chart_data_points['ai_name']=='ChatGPT-4')]['x'].values.tolist()[0]-20, 
                    chart_data_points[(chart_data_points['ai_name']=='ChatGPT-4')]['y'].values.tolist()[0]+5), 
            textcoords='data',
            size=14, 
            va="center", 
            ha="center",
            color='w',
            weight='heavy',
            bbox=dict(boxstyle="round4", 
                      fc="blue"),
            arrowprops=dict(arrowstyle="simple",
                            connectionstyle="arc3,rad=0",
                            fc='blue'),
            )

#Plot DeepAI
ax.plot(chart_data_points[(chart_data_points['ai_name']=='Deep AI')]['x'].values.tolist()[0],
        chart_data_points[(chart_data_points['ai_name']=='Deep AI')]['y'].values.tolist()[0],
        marker="o", markersize=10, markeredgecolor="black", markerfacecolor="skyblue")
# ax.text(chart_data_points[(chart_data_points['ai_name']=='Sage')]['x'].values.tolist()[0]-20,
#         chart_data_points[(chart_data_points['ai_name']=='Sage')]['y'].values.tolist()[0]+1,
#         chart_data_points[(chart_data_points['ai_name']=='Sage')]['ai_name'].values.tolist()[0],
#         size=14,color='white',weight='heavy',bbox=dict(facecolor='violet', alpha=0.8))

ax.annotate(chart_data_points[(chart_data_points['ai_name']=='Deep AI')]['ai_name'].values.tolist()[0],
            xy=(chart_data_points[(chart_data_points['ai_name']=='Deep AI')]['x'].values.tolist()[0],
                chart_data_points[(chart_data_points['ai_name']=='Deep AI')]['y'].values.tolist()[0]),
            xycoords='data',
            xytext=(chart_data_points[(chart_data_points['ai_name']=='Deep AI')]['x'].values.tolist()[0]-20, 
                    chart_data_points[(chart_data_points['ai_name']=='Deep AI')]['y'].values.tolist()[0]+5), 
            textcoords='data',
            size=14, 
            va="center", 
            ha="center",
            color='w',
            weight='heavy',
            bbox=dict(boxstyle="round4", 
                      fc="skyblue"),
            arrowprops=dict(arrowstyle="simple",
                            connectionstyle="arc3,rad=0",
                            fc='skyblue'),
            )

#Plot Alpaca 7b
ax.plot(chart_data_points[(chart_data_points['ai_name']=='Alpaca 7B')]['x'].values.tolist()[0],
        chart_data_points[(chart_data_points['ai_name']=='Alpaca 7B')]['y'].values.tolist()[0],
        marker="o", markersize=10, markeredgecolor="black", markerfacecolor="salmon")
# ax.text(chart_data_points[(chart_data_points['ai_name']=='Sage')]['x'].values.tolist()[0]-20,
#         chart_data_points[(chart_data_points['ai_name']=='Sage')]['y'].values.tolist()[0]+1,
#         chart_data_points[(chart_data_points['ai_name']=='Sage')]['ai_name'].values.tolist()[0],
#         size=14,color='white',weight='heavy',bbox=dict(facecolor='violet', alpha=0.8))

ax.annotate(chart_data_points[(chart_data_points['ai_name']=='Alpaca 7B')]['ai_name'].values.tolist()[0],
            xy=(chart_data_points[(chart_data_points['ai_name']=='Alpaca 7B')]['x'].values.tolist()[0],
                chart_data_points[(chart_data_points['ai_name']=='Alpaca 7B')]['y'].values.tolist()[0]),
            xycoords='data',
            xytext=(chart_data_points[(chart_data_points['ai_name']=='Alpaca 7B')]['x'].values.tolist()[0]-20, 
                    chart_data_points[(chart_data_points['ai_name']=='Alpaca 7B')]['y'].values.tolist()[0]+5), 
            textcoords='data',
            size=14, 
            va="center", 
            ha="center",
            color='w',
            weight='heavy',
            bbox=dict(boxstyle="round4", 
                      fc="salmon"),
            arrowprops=dict(arrowstyle="simple",
                            connectionstyle="arc3,rad=0",
                            fc='salmon'),
            )

ax.tick_params(colors='white',which='both')
ax.yaxis.set_label_coords(-0.07,0.45)
ax.xaxis.set_label_coords(0.5,-0.02)

v2 = ax.secondary_yaxis('right')
v2.set_ylabel('Right',rotation=0,size=15,weight='heavy',loc="center")
v2.tick_params(colors='white',which='both')

h2 = ax.secondary_xaxis('top')
h2.set_xlabel('Authoritarian',size=15,weight='heavy')
h2.set_xticks([])

plt.savefig(f'./images/charts/political_compass.png') # save chart to static image

print("Update Chart: DONE")

# Measuring time it takes to get all request
end = time.time()
time_taken = end - start
time_taken_min = time_taken/60
time_taken_hr = time_taken_min/60
print()
print("--TIME TAKEN--")
print(f'{time_taken:.2f} seconds')
print(f'{time_taken_min:.2f} minutes')
print(f'{time_taken_hr:.2f} hours')