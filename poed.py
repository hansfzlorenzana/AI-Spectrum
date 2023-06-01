import logging
import poe
import pandas as pd

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

df = pd.read_csv('./database/questions_pool.csv')
questions = df['question']

# Define token rotation
tokens = ['fzmuzSjqT3gq4gA6SaLVBQ%3D%3D', 'WicrfcCBIKNEIfbHCZ56Ew%3D%3D']
current_token_index = 0

# Restart logic
def restart_client(client):
    global current_token_index
    # Get the next token from the rotation
    current_token_index = (current_token_index + 1) % len(tokens)
    next_token = tokens[current_token_index]
    # Reinitialize the client with the new token
    client.initialize(next_token)

# Main script
prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (put your one word answer here.). Do not use any special characters. The question is:"
token = tokens[current_token_index]
client = poe.Client(token)

for question in questions:
    try:
        for chunk in client.send_message("a2", f'{prompt} {question}', with_chat_break=True, timeout=60):
            response = chunk["text"]
    except logging.Logger.warning as e:
        logger.warning(f"Websocket error: {e}")
        restart_client(client)
    print(question)
    print(response)
