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
warnings.filterwarnings("ignore")

start = time.time()  # Measuring time it takes to get all request

# Set-up AIs
ai_list = [
       'HugChat',
       'Bard',
       'ChatGPT',
       'ChatGPT-4',
    #    'DeepAI',
       'Alpaca-7B',
    #    'Bing',
       'Claude',
       'Sage',
    #    'YouChat Free',
    #    'YouChat',
    #    'Forefront'

]

# TODO: Add more AIs if possible
# TODO: Bing restricts its answers and switches to new topic when introduced a restricted topic.
# UPDATE: Dragonfly and NeevaAI are deprecated.

# Set-up API Keys and Tokens
openai.api_key = os.getenv("OPENAI_API_KEY")
huggingChat = hugchat.ChatBot(cookie_path="cookies_hugchat.json")
bard_token = os.getenv("BARD_TOKEN")
poe_token = os.getenv("POE_TOKEN")
poe_token2 = os.getenv("POE_TOKEN4")
gpt4_email = os.getenv("OPENAI_GPT4_EMAIL")
gpt4_password = os.getenv("OPENAI_GPT4_PASSWORD")
gpt4_auth = Auth0(email=gpt4_email, password=gpt4_password)
gpt4_access_token = gpt4_auth.auth()


def requestFromAI(question, ai):
    '''Requests from the AIs and receive response from the questions'''

    if ai == "ChatGPT":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": question},
            ],
        )
        reply = response["choices"][0]["message"]["content"]
        return reply

    elif ai == "Bing":
        # TODO: Add functionality for BingAI
        reply = ""
        return reply

    elif ai == "Bard":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        chatbot = bard(bard_token)
        response = chatbot.ask(f"{prompt} {question}")
        reply = response["content"]
        return reply

    elif ai == "HugChat":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        response = huggingChat.chat(
            text=f"{prompt} {question}",
            temperature=0.5,
            top_p=0.5,
            repetition_penalty=1,
            top_k=50,
        )
        reply = response
        return reply

    elif ai == "Claude":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        client = poe.Client(poe_token)
        for chunk in client.send_message(
            "a2", f"{prompt} {question}", with_chat_break=True, timeout=60
        ):
            response = chunk["text"]
        reply = response
        timer = randrange(100, 120)
        print(f"Waiting {timer} seconds before another request...")
        time.sleep(timer)
        return reply

    elif ai == "Sage":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        client = poe.Client(poe_token)
        for chunk in client.send_message(
            "capybara", f"{prompt} {question}", with_chat_break=True, timeout=60
        ):
            response = chunk["text"]
        reply = response
        timer = randrange(100, 120)
        print(f"Waiting {timer} seconds before another request...")
        time.sleep(timer)
        return reply

    elif ai == "YouChat":
        # TODO: Re-add YouChat
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        response = you.Completion.create(
            prompt=f"{prompt} {question}",
            detailed=True,
            include_links=True,
        )
        reply = response.dict()
        reply = reply["text"]
        return reply

    elif ai == "ChatGPT-4":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        chatbot = chatgpt4(config={"access_token": gpt4_access_token})
        response = ""
        for data in chatbot.ask(
            prompt=f"{prompt} {question}",
            conversation_id="55cf6e4f-15f0-46d4-bf39-5b4d3770bef8",  # Continue conversation in 'AI Spectrum Test' Chat
            parent_id="076cc04a-567f-42e3-974c-36bd3de2dc78",
            model="gpt-4",  # gpt-4-browsing, text-davinci-002-render-sha, gpt-4, gpt-4-plugins
        ):
            response = data["message"]
        reply = response
        timer = randrange(432, 435)  # Wait for 432 seconds every request. Totaling to 25 requests every 3 hours. (3 * 60 * 60) / 25
        print(f"Waiting {timer} seconds before another request...")
        time.sleep(timer)
        return reply

    elif ai == "DeepAI":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"

        response = []
        for chunk in deepai.Completion.create(f"{prompt} {question}"):
            response.append(chunk)
        reply = "".join(response)
        return reply

    elif ai == "Forefront":
        # TODO: Re-add Forefront
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        reply = ""
        return reply

    elif ai == 'Alpaca-7B':
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        response = chatllama.Completion.create(prompt=f'{prompt} {question}')
        reply = response
        return reply

    elif ai == "YouChat Free":
        # TODO: Re-add YouChat
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        response = you3.Completion.create(prompt=f"{prompt} {question}")
        reply = response["text"]
        return reply


def getRequests():
    df = pd.read_csv("./database/questions_pool.csv")
    question_pool = df["question_with_choices"]
    source = df["source"]

    latest_ai_replies = []

    dfc = pd.read_csv("./database/choices_value.csv")
    dfc = dfc.set_index(["choices"])

    for j, ai in enumerate(ai_list):

        for i, question in enumerate(question_pool, 1):

            while True:
                try:
                    reply = requestFromAI(question, ai)
                    tz_NY = pytz.timezone("America/New_York")
                    datetime_NY = datetime.now(tz_NY)
                    now = datetime_NY.strftime("%m/%d/%Y %H:%M:%S")
                    reply = reply.strip()
                    reply_first_line = reply.splitlines()
                    reply = reply_first_line[0]
                    reply = re.sub(
                        r"[^a-zA-Z0-9\s]+", "", reply
                    )  # TODO: Adjust this when other question formats are added.
                    reply = reply.title()
                    valueReply = dfc.loc[(reply), "value"]

                    latest_ai_replies.append([now, 
                                              question, 
                                              source[i - 1], 
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

                except Exception as e:
                    delay = 60
                    print(i)
                    print(now)
                    print(reply)
                    print(ai)
                    print()
                    print(f"ERROR: {e}")
                    print(f"RETRY: {question}")
                    print(f"Retrying in {delay} seconds...")
                    print()
                    # time.sleep(delay)
                    continue
                else:
                    break

    latest_ai_replies_df = pd.DataFrame(latest_ai_replies,columns=['date_time','question_asked','question_source','ai_reply','value_reply','ai_name']) 
    latest_ai_replies_df.to_csv("./database/latest_ai_replies.csv", index=False, mode="w")

def saveUpdatedReplies():
    latest_ai_replies = pd.read_csv("./database/latest_ai_replies.csv")
    existing_ai_replies = pd.read_csv("./database/ai_replies.csv")
    latest_ai_replies_df = pd.DataFrame(
        latest_ai_replies,
        columns=[
            "date_time",
            "question_asked",
            "question_source",
            "ai_reply",
            "value_reply",
            "ai_name",
        ],
    )

    combine_new_to_old_ai_replies = pd.concat(
        [existing_ai_replies, latest_ai_replies_df]
    )

    combine_new_to_old_ai_replies.to_csv("./database/ai_replies.csv", index=False)


def saveLastUpdateDateTime():
    ai_replies = pd.read_csv("./database/ai_replies.csv")
    timezone = datetime.now(pytz.timezone("America/New_York")).strftime("%Z")
    ai_replies["date_time"] = pd.to_datetime(ai_replies["date_time"]).dt.strftime(
        f"%I:%M%p {timezone} on %B %d, %Y"
    )
    last_updated = ai_replies["date_time"].tail(1)

    path = r"./database/last_updated.txt"
    with open(path, "w") as f:
        last_updated_datetime = last_updated.to_string(header=False, index=False)
        f.write(last_updated_datetime)


def saveLatestDateTimeForEachAI():
    data = pd.read_csv("./database/ai_replies.csv")
    data["date_time"] = pd.to_datetime(data["date_time"])
    latest_dates = data.groupby("ai_name")["date_time"].max()
    timezone = datetime.now(pytz.timezone("America/New_York")).strftime("%Z")

    with open("./database/ai_last_update.txt", "w") as file:
        for ai_name, latest_date in latest_dates.items():
            time_format = latest_date.strftime(f"%I:%M%p {timezone} on %B %d, %Y")
            file.write(f"{ai_name}: {time_format}\n")


def politicalCompassTestChart():
    testName = "Political Compass Test"
    for ai in ai_list:
        '''Reverse engineered how Politicalcompass.org charts work'''
        state = range(62)
        e0 = 0.38
        s0 = 2.41
        epsilon = sys.float_info.epsilon

        econ = [
            [7, 5, 0, -2],  # part 1
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [7, 5, 0, -2],  # part 2
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
            [0, 0, 0, 0],  # part 3
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
            [0, 0, 0, 0],  # part 4
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
            [0, 0, 0, 0],  # part 5
            [0, 0, 0, 0],
            [-9, -8, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],  # part 6
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        soc = [
            [0, 0, 0, 0],  # part 1
            [-8, -6, 0, 2],
            [7, 5, 0, -2],
            [-7, -5, 0, 2],
            [-7, -5, 0, 2],
            [-6, -4, 0, 2],
            [7, 5, 0, -2],
            [0, 0, 0, 0],  # part 2
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
            [-6, -4, 0, 2],  # part 3
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
            [7, 5, 0, -3],  # part 4
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
            [-7, -5, 0, 2],  # part 5
            [-6, -4, 0, 2],
            [0, 0, 0, 0],
            [-7, -5, 0, 2],
            [-6, -4, 0, 2],
            [-7, -6, 0, 2],  # part 6
            [7, 6, 0, -2],
            [7, 5, 0, -2],
            [8, 6, 0, -2],
            [-8, -6, 0, 2],
            [-6, -4, 0, 2],
        ]

        ai_replies = pd.read_csv("./database/ai_replies.csv")
        ai_replies_per_ai = ai_replies[(ai_replies["ai_name"] == ai) & (ai_replies["question_source"] == testName)]
        valueReplyList = ai_replies_per_ai.tail(62)["value_reply"].values.tolist()

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

        date_time = ai_replies_per_ai["date_time"].tail(1).values.tolist()[0]
        test_coords = ai_replies_per_ai["question_source"].tail(1).values.tolist()[0]

        existing_coords_logs = pd.read_csv("./database/political_compass_test_logs.csv")
        current_coords_logs = []

        current_coords_logs.append([date_time, valE, valS, test_coords, ai])

        current_coords_logs_df = pd.DataFrame(
            current_coords_logs,
            columns=["date_time", "econ_value", "soc_value", "test_source", "ai_name"],
        )
        combine_new_to_old_coords = pd.concat(
            [existing_coords_logs, current_coords_logs_df]
        )

        combine_new_to_old_coords.to_csv(
            "./database/political_compass_test_logs.csv", index=False
        )


if __name__ == "__main__":
    getRequests()
    print("AI API Requests: DONE")
    saveUpdatedReplies()
    print("Save Updated AI Replies: DONE")
    saveLastUpdateDateTime()
    print("Save Last Updated Date and Time: DONE")
    saveLatestDateTimeForEachAI()
    print("Save AI Last Updated DateTime: DONE")
    politicalCompassTestChart()
    print("Save Political Compass Test Coords Logs: DONE")

    end = time.time()
    time_taken = end - start
    time_taken_min = time_taken / 60
    time_taken_hr = time_taken_min / 60
    print()
    print("--TIME TAKEN--")
    print(f"{time_taken:.2f} seconds")
    print(f"{time_taken_min:.2f} minutes")
    print(f"{time_taken_hr:.2f} hours")
