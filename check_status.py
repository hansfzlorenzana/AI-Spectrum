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
import gpt4free
from gpt4free import Provider
from revChatGPT.V1 import Chatbot as gpt4
from OpenAIAuth import Auth0

import os, sys, time, warnings, pytz, re

load_dotenv()
warnings.filterwarnings('ignore')

# Set-up AIs
ai_list = ['YouChat',
           'Claude',
           'Bard',
           'HugChat',
           'Sage',
           'ChatGPT',
           'ChatGPT-4'
           ] 
# TODO: Add more AIs if possible
# TODO: Bing restricts its answers and switches to new topic when introduced a restricted topic.
# UPDATE: Dragonfly and NeevaAI are deprecated.

# Set-up API Keys and Tokens
openai.api_key = os.getenv('OPENAI_API_KEY')
huggingChat = hugchat.ChatBot(cookie_path="cookies_hugchat.json")
bard_token = os.getenv('BARD_TOKEN')
poe_token = os.getenv('POE_TOKEN3')
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
    
    # elif ai == "Bing Chat":
    #     # TODO: Add functionality for BingAI
    #     reply = ""
    #     return reply

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
        return reply

    elif ai == "Sage":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        client = poe.Client(poe_token2)
        for chunk in client.send_message("capybara", f'{prompt} {question}', with_chat_break=True, timeout=60):
            response = chunk["text"]
            
        reply=response
        return reply
    
    elif ai == "YouChat":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        response = gpt4free.Completion.create(Provider.You, prompt=f'{prompt} {question}')
        reply = response
        return reply
    
    elif ai == "ChatGPT-4":
        prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"
        chatbot = gpt4(config={
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
        return reply
    
    # TODO: 25 requests every 3 hours. If limit reached within timeframe, wait for 3 hours or run other AIs

    # else:
    #     reply = ""
    #     return reply

def check_ai_responses(ai_names, responses):
    ai_statuses = []

    for ai, response in zip(ai_names, responses):
        ai_status = "Okay" if is_ai_response_okay(response) else "Not okay"
        ai_statuses.append(f"{ai}: {response} {ai_status}")

    return ai_statuses

def is_ai_response_okay(response):
    return response is not None and ('error' not in response or isinstance(response, Exception))

question = "If economic globalisation is inevitable, it should primarily serve humanity rather than the interests of trans-national corporations. Please choose one and ONLY one: \nStrongly Disagree\nDisagree\nAgree\nStrongly Agree"

def main():
    ai_responses = []
    ai_statuses = []

    for ai in ai_list:
        try:
            reply = requestFromAI(question, ai)
            ai_responses.append(reply)
            ai_statuses.append(f"{ai}: Okay")
        except Exception as e:
            ai_responses.append(str(e))
            ai_statuses.append(f"{ai}: Error")

    for ai_status in ai_statuses:
        print(ai_status)

main()

    


