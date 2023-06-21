from datetime import datetime
from random import randrange
from dotenv import load_dotenv
from matplotlib import image
import matplotlib.pyplot as plt
import pandas as pd

from Bard import Chatbot as bard
from hugchat import hugchat
import poe # For Poe and Sage. Claude and OpenAI are handled by different libraries.
import openai # For ChatGPT3. GPT4 is handled by different library.
from g4f import you 
from g4f import deepai
from revChatGPT.V1 import Chatbot as chatgpt4 
from OpenAIAuth import Auth0
from freeGPT import gpt3 as you3 # Alternative YouChat API
from freeGPT import alpaca_7b as chatllama
import g4fv2 # Alternative G4F API. Supports Forefront, Ora, YouChat and Phind (and more...)

import os, sys, time, warnings, pytz, re

load_dotenv()
warnings.filterwarnings("ignore")

start = time.time()  # Measuring time it takes to get all request

# Set-up AIs
ai_list = [
       'HugChat',
       'Bards',
       'ChatGPT',
       'ChatGPT-4',
       'DeepAIs',
       'Alpaca-7Bs',
       'Bing',
       'Claude',
       'Sage',
    #    'YouChat FreeGPT',
    #    'YouChat',
       'Forefront',
       'Ora',
       'YouChat', #GF4V2 lib
       'Phind',
]

APP_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"
DB_PATH = APP_PATH + "/database/"

# Set-up API Keys and Tokens
openai.api_key = os.getenv("OPENAI_API_KEY")
huggingChat = hugchat.ChatBot(cookie_path= APP_PATH + "cookies_hugchat.json")
bard_token = os.getenv("BARD_TOKEN2")
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
    
    elif ai == 'YouChat FreeGPT':
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        proxy = "145.239.85.58:9300" # Poland
        response = you3.Completion.create(prompt=f'{prompt} {question}',chat=[], proxies={"https": "http://" + proxy})
        reply = response['text']
        return reply

    elif ai == "ChatGPT-4":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        chatbot = chatgpt4(config={"access_token": gpt4_access_token})
        response = ""
        for data in chatbot.ask(
            prompt=f"{prompt} {question}",
            conversation_id="55cf6e4f-15f0-46d4-bf39-5b4d3770bef8",  # Continue conversation in 'AI Spectrum Test' Chat
            parent_id="076cc04a-567f-42e3-974c-36bd3de2dc78",
            model="gpt-4",  # gpt-4-browsing, text-davinci-002-render-sha, gpt-4, gpt-4-plugins, gpt-4-mobile
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
    
    elif ai == 'Alpaca-7B':
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        response = chatllama.Completion.create(prompt=f'{prompt} {question}')
        reply = response
        return reply

    elif ai == "Forefront":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        response = g4fv2.ChatCompletion.create(model='gpt-4', provider=g4fv2.Provider.Forefront, messages=[
                                     {"role": "user", "content": f"{prompt} {question}"}])
        reply=response
        return reply
    
    elif ai == 'Ora':
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        response = g4fv2.ChatCompletion.create(model='gpt-4', provider=g4fv2.Provider.Ora, messages=[
                                     {"role": "user", "content": f"{prompt} {question}"}])
        reply=response
        return reply
    
    elif ai == 'Phind':
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        response = g4fv2.ChatCompletion.create(model='gpt-4', provider=g4fv2.Provider.Phind, messages=[
                                     {"role": "user", "content": f"{prompt} {question}"}])
        reply=response
        return reply
    
    elif ai == 'YouChat G4FV2':
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        response = g4fv2.ChatCompletion.create(model='gpt-4', provider=g4fv2.Provider.You, messages=[
                                     {"role": "user", "content": f"{prompt} {question}"}])
        reply=response
        return reply


def getRequests():
    df = pd.read_csv(DB_PATH +"questions_pool.csv")
    question_pool = df["question_with_choices"]
    source = df["source"]

    latest_ai_replies = []

    dfc = pd.read_csv(DB_PATH + "choices_value.csv")
    dfc = dfc.set_index(["choices"])

    for j, ai in enumerate(ai_list):
        retry_count = 0

        if ai != "ChatGPT-4":
            max_retries = 20
        else:
            max_retries = 200

        ignore_ai_responses = False
        question_number = 0
        prev_source = None

        for i, question in enumerate(question_pool, 1):

            # If source is not the same as previous, then restart question number count
            if prev_source is None or source[i - 1] != prev_source:
                question_number = 0
            prev_source = source[i - 1]

            if ignore_ai_responses:
                break

            while True:
                try:
                    if retry_count >= max_retries:
                        print(f"ERROR: Maximum retries exceeded for {ai}. Moving to the next AI.")
                        print()
                        ignore_ai_responses = True
                        break

                    if not ignore_ai_responses:
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
                        valueReply = dfc.loc[(dfc.index == reply) & (dfc["source"] == source[i-1]), "value"].values[0]

                        latest_ai_replies.append([now, 
                                                  question, 
                                                  source[i - 1], 
                                                  reply, 
                                                  valueReply, 
                                                  ai
                                                  ])
                    question_number += 1
                    print(question_number)
                    print(now)
                    print(question)
                    print(reply)
                    print(ai)
                    print(source[i-1])
                    print(valueReply)
                    print()

                except Exception as e:
                    retry_count += 1

                    if retry_count >= max_retries:
                        print(f'{question_number} | {ai}')
                        print(f"ERROR: Maximum retries exceeded for {ai}. Moving to the next AI.")
                        print()
                        ignore_ai_responses = True
                        break

                    delay = 2
                    print(f'{question_number} | {ai}')
                    print(f"ERROR: {e}")
                    print(f"RETRY: {question}")
                    print(f"Retrying in {delay} seconds...")
                    print()
                    time.sleep(delay)
                    continue

                else:
                    retry_count = 0
                    break

    latest_ai_replies_df = pd.DataFrame(latest_ai_replies,columns=['date_time','question_asked','question_source','ai_reply','value_reply','ai_name']) 
    latest_ai_replies_df.to_csv(DB_PATH + "latest_ai_replies.csv", index=False, mode="w")

def saveUpdatedReplies():
    latest_ai_replies = pd.read_csv(DB_PATH + "latest_ai_replies.csv")
    existing_ai_replies = pd.read_csv(DB_PATH + "ai_replies.csv")
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

    combine_new_to_old_ai_replies.to_csv(DB_PATH + "ai_replies.csv", index=False)


def saveLastUpdateDateTime():
    ai_replies = pd.read_csv(DB_PATH + "ai_replies.csv")
    timezone = datetime.now(pytz.timezone("America/New_York")).strftime("%Z")
    ai_replies["date_time"] = pd.to_datetime(ai_replies["date_time"]).dt.strftime(
        f"%I:%M%p {timezone} on %B %d, %Y"
    )
    last_updated = ai_replies["date_time"].tail(1)

    path = DB_PATH + "last_updated.txt"
    with open(path, "w") as f:
        last_updated_datetime = last_updated.to_string(header=False, index=False)
        f.write(last_updated_datetime)


def saveLatestDateTimeForEachAI():
    data = pd.read_csv(DB_PATH + "ai_replies.csv")
    data["date_time"] = pd.to_datetime(data["date_time"])
    latest_dates = data.groupby("ai_name")["date_time"].max()
    timezone = datetime.now(pytz.timezone("America/New_York")).strftime("%Z")

    with open(DB_PATH + "ai_last_update.txt", "w") as file:
        for ai_name, latest_date in latest_dates.items():
            time_format = latest_date.strftime(f"%I:%M%p {timezone} on %B %d, %Y")
            file.write(f"{ai_name}: {time_format}\n")


def politicalCompassTestChart():
    testName = "Political Compass Test"
    columns = ["date_time", "econ_value", "soc_value", "test_source", "ai_name"]
    numberofQuestions = 62

    for ai in ai_list:
        '''Reverse engineered how Politicalcompass.org charts work'''
        try:
            state = range(numberofQuestions)
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

            ai_replies = pd.read_csv(DB_PATH + "latest_ai_replies.csv")
            ai_replies_per_ai = ai_replies[(ai_replies["ai_name"] == ai) & (ai_replies["question_source"] == testName)]
            valueReplyList = ai_replies_per_ai.tail(numberofQuestions)["value_reply"].values.tolist()

            sumE = 0
            sumS = 0

            for i in state:
                sumE += econ[int(i)][int(valueReplyList[int(i)])]
                sumS += soc[int(i)][int(valueReplyList[int(i)])]

            valE = sumE / 8.0
            valS = sumS / 19.5

            valE += e0
            valS += s0

            valE = round((valE + epsilon) * 100) / 100
            valS = round((valS + epsilon) * 100) / 100

            date_time = ai_replies_per_ai["date_time"].tail(1).values.tolist()[0]
            test_coords = ai_replies_per_ai["question_source"].tail(1).values.tolist()[0]

            existing_coords_logs = pd.read_csv(DB_PATH + "political_compass_test_logs.csv")
            current_coords_logs = []

            current_coords_logs.append([date_time, valE, valS, test_coords, ai])

            current_coords_logs_df = pd.DataFrame(
                current_coords_logs,
                columns=columns,
            )
            combine_new_to_old_coords = pd.concat(
                [existing_coords_logs, current_coords_logs_df]
            )

            combine_new_to_old_coords.to_csv(
                DB_PATH + "political_compass_test_logs.csv", index=False
            )

        except Exception as e:
            print(f'ERROR: {e}')
            continue

def eightValuesTestChart():
    testName = "8Values Political Test"
    columns = ["date_time","equality","peace","liberty","progress","wealth","might","authority","tradition","test_source","ai_name"]
    numberofQuestions = 70

    questions = [
        {
            "question": "Oppression by corporations is more of a concern than oppression by governments.",
            "effect": {
                "econ": 10,
                "dipl": 0,
                "govt": -5,
                "scty": 0
            }
        },
        {
            "question": "It is necessary for the government to intervene in the economy to protect consumers.",
            "effect": {
                "econ": 10,
                "dipl": 0,
                "govt": 0,
                "scty": 0
            }
        },
        {
            "question": "The freer the markets, the freer the people.",
            "effect": {
                "econ": -10,
                "dipl": 0,
                "govt": 0,
                "scty": 0
            }
        },
        {
            "question": "It is better to maintain a balanced budget than to ensure welfare for all citizens.",
            "effect": {
                "econ": -10,
                "dipl": 0,
                "govt": 0,
                "scty": 0
            }
        },
        {
            "question": "Publicly-funded research is more beneficial to the people than leaving it to the market.",
            "effect": {
                "econ": 10,
                "dipl": 0,
                "govt": 0,
                "scty": 10
            }
        },
        {
            "question": "Tariffs on international trade are important to encourage local production.",
            "effect": {
                "econ": 5,
                "dipl": 0,
                "govt": -10,
                "scty": 0
            }
        },
        {
            "question": "From each according to his ability, to each according to his needs.",
            "effect": {
                "econ": 10,
                "dipl": 0,
                "govt": 0,
                "scty": 0
            }
        },
        {
            "question": "It would be best if social programs were abolished in favor of private charity.",
            "effect": {
                "econ": -10,
                "dipl": 0,
                "govt": 0,
                "scty": 0
            }
        },
        {
            "question": "Taxes should be increased on the rich to provide for the poor.",
            "effect": {
                "econ": 10,
                "dipl": 0,
                "govt": 0,
                "scty": 0
            }
        },
        {
            "question": "Inheritance is a legitimate form of wealth.",
            "effect": {
                "econ": -10,
                "dipl": 0,
                "govt": 0,
                "scty": -5
            }
        },
        {
            "question": "Basic utilities like roads and electricity should be publicly owned.",
            "effect": {
                "econ": 10,
                "dipl": 0,
                "govt": 0,
                "scty": 0
            }
        },
        {
            "question": "Government intervention is a threat to the economy.",
            "effect": {
                "econ": -10,
                "dipl": 0,
                "govt": 0,
                "scty": 0
            }
        },
        {
            "question": "Those with a greater ability to pay should receive better healthcare.",
            "effect": {
                "econ": -10,
                "dipl": 0,
                "govt": 0,
                "scty": 0
            }
        },
        {
            "question": "Quality education is a right of all people.",
            "effect": {
                "econ": 10,
                "dipl": 0,
                "govt": 0,
                "scty": 5
            }
        },
        {
            "question": "The means of production should belong to the workers who use them.",
            "effect": {
                "econ": 10,
                "dipl": 0,
                "govt": 0,
                "scty": 0
            }
        },
        {
            "question": "The United Nations should be abolished.",
            "effect": {
                "econ": 0,
                "dipl": -10,
                "govt": -5,
                "scty": 0
            }
        },
        {
            "question": "Military action by our nation is often necessary to protect it.",
            "effect": {
                "econ": 0,
                "dipl": -10,
                "govt": -10,
                "scty": 0
            }
        },
        {
            "question": "I support regional unions, such as the European Union.",
            "effect": {
                "econ": -5,
                "dipl": 10,
                "govt": 10,
                "scty": 5
            }
        },
        {
            "question": "It is important to maintain our national sovereignty.",
            "effect": {
                "econ": 0,
                "dipl": -10,
                "govt": -5,
                "scty": 0
            }
        },
        {
            "question": "A united world government would be beneficial to mankind.",
            "effect": {
                "econ": 0,
                "dipl": 10,
                "govt": 0,
                "scty": 0
            }
        },
        {
            "question": "It is more important to retain peaceful relations than to further our strength.",
            "effect": {
                "econ": 0,
                "dipl": 10,
                "govt": 0,
                "scty": 0
            }
        },
        {
            "question": "Wars do not need to be justified to other countries.",
            "effect": {
                "econ": 0,
                "dipl": -10,
                "govt": -10,
                "scty": 0
            }
        },
        {
            "question": "Military spending is a waste of money.",
            "effect": {
                "econ": 0,
                "dipl": 10,
                "govt": 10,
                "scty": 0
            }
        },
        {
            "question": "International aid is a waste of money.",
            "effect": {
                "econ": -5,
                "dipl": -10,
                "govt": 0,
                "scty": 0
            }
        },
        {
            "question": "My nation is great.",
            "effect": {
                "econ": 0,
                "dipl": -10,
                "govt": 0,
                "scty": 0
            }
        },
        {
            "question": "Research should be conducted on an international scale.",
            "effect": {
                "econ": 0,
                "dipl": 10,
                "govt": 0,
                "scty": 10
            }
        },
        {
            "question": "Governments should be accountable to the international community.",
            "effect": {
                "econ": 0,
                "dipl": 10,
                "govt": 5,
                "scty": 0
            }
        },
        {
            "question": "Even when protesting an authoritarian government, violence is not acceptable.",
            "effect": {
                "econ": 0,
                "dipl": 5,
                "govt": -5,
                "scty": 0
            }
        },
        {
            "question": "My religious values should be spread as much as possible.",
            "effect": {
                "econ": 0,
                "dipl": -5,
                "govt": -10,
                "scty": -10
            }
        },
        {
            "question": "Our nation's values should be spread as much as possible.",
            "effect": {
                "econ": 0,
                "dipl": -10,
                "govt": -5,
                "scty": 0
            }
        },
        {
            "question": "It is very important to maintain law and order.",
            "effect": {
                "econ": 0,
                "dipl": -5,
                "govt": -10,
                "scty": -5
            }
        },
        {
            "question": "The general populace makes poor decisions.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": -10,
                "scty": 0
            }
        },
        {
            "question": "Physician-assisted suicide should be legal.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": 10,
                "scty": 0
            }
        },
        {
            "question": "The sacrifice of some civil liberties is necessary to protect us from acts of terrorism.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": -10,
                "scty": 0
            }
        },
        {
            "question": "Government surveillance is necessary in the modern world.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": -10,
                "scty": 0
            }
        },
        {
            "question": "The very existence of the state is a threat to our liberty.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": 10,
                "scty": 0
            }
        },
        {
            "question": "Regardless of political opinions, it is important to side with your country.",
            "effect": {
                "econ": 0,
                "dipl": -10,
                "govt": -10,
                "scty": -5
            }
        },
        {
            "question": "All authority should be questioned.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": 10,
                "scty": 5
            }
        },
        {
            "question": "A hierarchical state is best.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": -10,
                "scty": 0
            }
        },
        {
            "question": "It is important that the government follows the majority opinion, even if it is wrong.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": 10,
                "scty": 0
            }
        },
        {
            "question": "The stronger the leadership, the better.",
            "effect": {
                "econ": 0,
                "dipl": -10,
                "govt": -10,
                "scty": 0
            }
        },
        {
            "question": "Democracy is more than a decision-making process.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": 10,
                "scty": 0
            }
        },
        {
            "question": "Environmental regulations are essential.",
            "effect": {
                "econ": 5,
                "dipl": 0,
                "govt": 0,
                "scty": 10
            }
        },
        {
            "question": "A better world will come from automation, science, and technology.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": 0,
                "scty": 10
            }
        },
        {
            "question": "Children should be educated in religious or traditional values.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": -5,
                "scty": -10
            }
        },
        {
            "question": "Traditions are of no value on their own.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": 0,
                "scty": 10
            }
        },
        {
            "question": "Religion should play a role in government.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": -10,
                "scty": -10
            }
        },
        {
            "question": "Churches should be taxed the same way other institutions are taxed.",
            "effect": {
                "econ": 5,
                "dipl": 0,
                "govt": 0,
                "scty": 10
            }
        },
        {
            "question": "Climate change is currently one of the greatest threats to our way of life.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": 0,
                "scty": 10
            }
        },
        {
            "question": "It is important that we work as a united world to combat climate change.",
            "effect": {
                "econ": 0,
                "dipl": 10,
                "govt": 0,
                "scty": 10
            }
        },
        {
            "question": "Society was better many years ago than it is now.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": 0,
                "scty": -10
            }
        },
        {
            "question": "It is important that we maintain the traditions of our past.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": 0,
                "scty": -10
            }
        },
        {
            "question": "It is important that we think in the long term, beyond our lifespans.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": 0,
                "scty": 10
            }
        },
        {
            "question": "Reason is more important than maintaining our culture.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": 0,
                "scty": 10
            }
        },
        {
            "question": "Drug use should be legalized or decriminalized.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": 10,
                "scty": 2
            }
        },
        {
            "question": "Same-sex marriage should be legal.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": 10,
                "scty": 10
            }
        },
        {
            "question": "No cultures are superior to others.",
            "effect": {
                "econ": 0,
                "dipl": 10,
                "govt": 5,
                "scty": 10
            }
        },
        {
            "question": "Sex outside marriage is immoral.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": -5,
                "scty": -10
            }
        },
        {
            "question": "If we accept migrants at all, it is important that they assimilate into our culture.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": -5,
                "scty": -10
            }
        },
        {
            "question": "Abortion should be prohibited in most or all cases.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": -10,
                "scty": -10
            }
        },
        {
            "question": "Gun ownership should be prohibited for those without a valid reason.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": -10,
                "scty": 0
            }
        },
        {
            "question": "I support single-payer, universal healthcare.",
            "effect": {
                "econ": 10,
                "dipl": 0,
                "govt": 0,
                "scty": 0
            }
        },
        {
            "question": "Prostitution should be illegal.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": -10,
                "scty": -10
            }
        },
        {
            "question": "Maintaining family values is essential.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": 0,
                "scty": -10
            }
        },
        {
            "question": "To chase progress at all costs is dangerous.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": 0,
                "scty": -10
            }
        },
        {
            "question": "Genetic modification is a force for good, even on humans.",
            "effect": {
                "econ": 0,
                "dipl": 0,
                "govt": 0,
                "scty": 10
            }
        },
        {
            "question": "We should open our borders to immigration.",
            "effect": {
                "econ": 0,
                "dipl": 10,
                "govt": 10,
                "scty": 0
            }
        },
        {
            "question": "Governments should be as concerned about foreigners as they are about their own citizens.",
            "effect": {
                "econ": 0,
                "dipl": 10,
                "govt": 0,
                "scty": 0
            }
        },
        {
            "question": "All people - regardless of factors like culture or sexuality - should be treated equally.",
            "effect": {
                "econ": 10,
                "dipl": 10,
                "govt": 10,
                "scty": 10
            }
        },
        {
            "question": "It is important that we further my group's goals above all others.",
            "effect": {
                "econ": -10,
                "dipl": -10,
                "govt": -10,
                "scty": -10
            }
        }
    ]

    for ai in ai_list:
        '''Reverse engineered how https://www.idrlabs.com/8-values-political/test.php charts work'''
        try:
            max_econ = max_dipl = max_govt = max_scty = 0
            econ_array = [None] * len(questions)
            dipl_array = [None] * len(questions)
            govt_array = [None] * len(questions)
            scty_array = [None] * len(questions)
            qn = 0

            for i, question in enumerate(questions):
                max_econ += abs(questions[i]["effect"]["econ"])
                max_dipl += abs(questions[i]["effect"]["dipl"])
                max_govt += abs(questions[i]["effect"]["govt"])
                max_scty += abs(questions[i]["effect"]["scty"])

            def calc_score(score, max):
                return f"{(100 * (max + score) / (2 * max)):.1f}"

            ai_replies = pd.read_csv(DB_PATH + "latest_ai_replies.csv")
            ai_replies_per_ai = ai_replies[(ai_replies["ai_name"] == ai) & (ai_replies["question_source"] == testName)]
            valueReplyList = ai_replies_per_ai.tail(numberofQuestions)["value_reply"].values.tolist()

            for mult in valueReplyList:
                econ_array[qn] = mult * questions[qn]["effect"]["econ"]
                dipl_array[qn] = mult * questions[qn]["effect"]["dipl"]
                govt_array[qn] = mult * questions[qn]["effect"]["govt"]
                scty_array[qn] = mult * questions[qn]["effect"]["scty"]
                qn += 1
            
            final_econ = sum(econ_array)
            final_dipl = sum(dipl_array)
            final_govt = sum(govt_array)
            final_scty = sum(scty_array)
            econ=calc_score(final_econ, max_econ)
            dipl=calc_score(final_dipl, max_dipl)
            govt=calc_score(final_govt, max_govt)
            scty=calc_score(final_scty, max_scty)

            equality  = float(econ)
            peace     = float(dipl)
            liberty   = float(govt)
            progress  = float(scty)
            wealth    = round((100 - equality), 1)
            might     = round((100 - peace), 1)
            authority = round((100 - liberty), 1)
            tradition = round((100 - progress), 1)

            date_time = ai_replies_per_ai["date_time"].tail(1).values.tolist()[0]
            test_coords = ai_replies_per_ai["question_source"].tail(1).values.tolist()[0]

            existing_coords_logs = pd.read_csv(DB_PATH + "8values_political_test_logs.csv")
            current_coords_logs = []

            current_coords_logs.append([date_time, 
                                        equality, 
                                        peace, 
                                        liberty, 
                                        progress,
                                        wealth,
                                        might,
                                        authority,
                                        tradition,
                                        test_coords, 
                                        ai
                                        ])

            current_coords_logs_df = pd.DataFrame(
                current_coords_logs,
                columns=columns,
            )
            combine_new_to_old_coords = pd.concat(
                [existing_coords_logs, current_coords_logs_df]
            )

            combine_new_to_old_coords.to_csv(
                DB_PATH + "8values_political_test_logs.csv", index=False
            )
        
        except Exception as e:
            print(f'ERROR: {e}')
            continue

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
    eightValuesTestChart()
    print("Save 8Values Political Test Coords Logs: DONE")

    end = time.time()
    time_taken = end - start
    time_taken_min = time_taken / 60
    time_taken_hr = time_taken_min / 60
    print()
    print("--TIME TAKEN--")
    print(f"{time_taken:.2f} seconds")
    print(f"{time_taken_min:.2f} minutes")
    print(f"{time_taken_hr:.2f} hours")
