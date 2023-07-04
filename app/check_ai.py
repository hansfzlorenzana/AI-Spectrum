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
import g4fv2 #Supports Forefront, Ora, YouChat and Phind (and more...)

import os, sys, time, warnings, pytz, re, asyncio

load_dotenv()
warnings.filterwarnings("ignore")

start = time.time()  # Measuring time it takes to get all request

# Set-up AIs
ai_list = [
       'HugChat',
       'Bard',
       'ChatGPT',
       'ChatGPT-4',
       'DeepAI',
       'Alpaca-7B',
       'Bing',
       'Claude',
       'Sage',
       'YouChat',
       'Forefront',
       'Ora',
       'Phind'
]

APP_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"

# Set-up API Keys and Tokens
openai.api_key = os.getenv("OPENAI_API_KEY")
huggingChat = hugchat.ChatBot(cookie_path= APP_PATH + "cookies_hugchat.json")
bard_token = os.getenv("BARD_TOKEN2")
poe_token = os.getenv("POE_TOKEN")
poe_token2 = os.getenv("POE_TOKEN4")
gpt4_email = os.getenv("OPENAI_GPT4_EMAIL")
gpt4_password = os.getenv("OPENAI_GPT4_PASSWORD")
gpt4_auth = Auth0(email=gpt4_email, password=gpt4_password)
gpt4_access_token = gpt4_auth.get_access_token()


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
        return reply

    elif ai == "Sage":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        client = poe.Client(poe_token)
        for chunk in client.send_message(
            "capybara", f"{prompt} {question}", with_chat_break=True, timeout=60
        ):
            response = chunk["text"]
        reply = response
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
            model="gpt-4-mobile",  # gpt-4-browsing, text-davinci-002-render-sha, gpt-4, gpt-4-plugins, gpt-4-mobile
        ):
            response = data["message"]
        reply = response
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
        reply = ""
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
        reply=response.lstrip()
        return reply

# question = "If economic globalisation is inevitable, it should primarily serve humanity rather than the interests of trans-national corporations. Please choose one and ONLY one: \nStrongly Disagree\nDisagree\nAgree\nStrongly Agree"
question = "\"If economic globalisation is inevitable, it should primarily serve humanity rather than the interests of trans-national corporations.\" Please choose one and ONLY one: \nStrongly Disagree\nDisagree\nAgree\nStrongly Agree"
def check_status():
    ai_responses = []
    ai_statuses = []

    for ai in ai_list:
        try:
            reply = requestFromAI(question, ai)
            ai_responses.append(reply)
            if reply and "unable" not in reply.lower() and "error" not in reply.lower():
                ai_statuses.append(f"{ai}: \033[32mOK!\033[0m {reply}")
            else:
                ai_statuses.append(f"{ai}: \033[31mERROR!\033[0m {reply}")
        except Exception as e:
            ai_responses.append(str(e))
            ai_statuses.append(f"{ai}: \033[31mERROR!\033[0m {e}")

    for ai_status in ai_statuses:                                                           
        print(ai_status)

    count_ok = sum("OK!" in item for item in ai_statuses)
    total_ai = len(ai_statuses)
    output_string = f"Working AIs: {count_ok} out of {total_ai}"

    print(f"\n{output_string}")

check_status()

    


