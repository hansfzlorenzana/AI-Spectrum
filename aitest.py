from g4f import you

prompt = "Hi"
response = you.Completion.create(
    prompt=f'{prompt}',
    detailed=True,
    include_links=True, )
reply = response.dict()
reply = reply['text']

print(reply)