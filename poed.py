import poe
import json


question = "If economic globalisation is inevitable, it should primarily serve humanity rather than the interests of trans-national corporations. Please choose one and ONLY one: \nStrongly Disagree\nDisagree\nAgree\nStrongly Agree"
prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (put your one word answer here.). Do not use any special characters. The question is:"
token="fzmuzSjqT3gq4gA6SaLVBQ%3D%3D"
client = poe.Client(token)

for chunk in client.send_message("a2", f'{prompt} {question}', with_chat_break=True, timeout=60):
    response = chunk["text_new"]
    print(response)

print(response)

#delete the 3 latest messages, including the chat break
