import g4f

question = "\"If economic globalisation is inevitable, it should primarily serve humanity rather than the interests of trans-national corporations.\" Please choose one and ONLY one: \nStrongly Disagree\nDisagree\nAgree\nStrongly Agree"
prompt = "You are to answer everything using the provided choices only. Do not justify your answer. Be direct and NO SENTENCES AT ALL TIMES. Use this format (answer from the choices here.). Do not use any special characters. The question is:\n\n"

# Set with provider
response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', provider=g4f.Provider.Forefront, messages=[
                                     {"role": "user", "content": f"{prompt} {question}"}])

for message in response:
    print(message)

print(response)
# Phind, 'gpt-3.5-turbo', 'gpt-4' WORKS
# You, 'gpt-3.5-turbo' WORKS
# Bing, 'gpt-3.5-turbo', 'gpt-4' WORKS
# Openai, 'gpt-3.5-turbo' WORKS
# Yqcloud, WORKS
# Theb, DOES NOT WORK
# Aichat, WORKS (Stream: false)
# Ora, WORKS (Stream: false)
# Aws, DOES NOT WORK
# Bard, WORKS
# Vercel, gpt-3.5-turbo WORKS but better use https://github.com/ading2210/vercel-llm-api
# Pierangelo, DOES NOT WORK
# Forefront, WORKS