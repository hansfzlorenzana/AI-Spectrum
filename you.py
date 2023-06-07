# from youdotcom import Chat # import all the classes

# chat = Chat.send_message(message="how is your day?", api_key="KS9A1SMPFZHW45WC9OD0I2OLJBFVIRULP69") # send a message to YouChat. passing the message and your api key.

# # you can get an api key form the site: https://api.betterapi.net/ (with is also made by me)

# print(chat)  # returns the message and some other data

# 👋 Hello! My name is YouChat. I’m an AI that can answer general questions, explain things, suggest ideas, translate, summarize text, compose emails, and write code for you.
import requests # import requests for the api call

API_KEY = "KS9A1SMPFZHW45WC9OD0I2OLJBFVIRULP69" # your api key

inputs = 'hi there'
url = f"https://api.betterapi.net/youchat?inputs={inputs}&key=" + API_KEY # set api url
json = requests.get(url).json() # load json form api
print(json["generated_text"]) # print message response