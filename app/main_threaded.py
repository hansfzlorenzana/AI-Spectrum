import multiprocessing

def process_question(question, ai):
    reply = requestFromAI(question, ai)
    tz_NY = pytz.timezone("America/New_York")
    datetime_NY = datetime.now(tz_NY)
    now = datetime_NY.strftime("%m/%d/%Y %H:%M:%S")
    reply = reply.strip()
    reply_first_line = reply.splitlines()
    reply = reply_first_line[0]
    reply = re.sub(r"[^a-zA-Z0-9\s]+", "", reply)
    reply = reply.title()
    valueReply = dfc.loc[(dfc.index == reply) & (dfc["source"] == source[i-1]), "value"].values[0]

    return [now, question, source[i - 1], reply, valueReply, ai]


def getRequests():
    df = pd.read_csv(DB_PATH + "questions_pool.csv")
    question_pool = df["question_with_choices"]
    source = df["source"]

    latest_ai_replies = []

    dfc = pd.read_csv(DB_PATH + "choices_value.csv")
    dfc = dfc.set_index(["choices"])

    # Create a multiprocessing.Pool with the number of desired processes
    pool = multiprocessing.Pool(processes=len(ai_list))

    for j, ai in enumerate(ai_list):
        ignore_ai_responses = False
        question_number = 0
        prev_source = None

        # Define a partial function with the ai parameter fixed
        partial_func = functools.partial(process_question, ai=ai)

        results = []

        for i, question in enumerate(question_pool, 1):
            # If source is not the same as previous, then restart question number count
            if prev_source is None or source[i - 1] != prev_source:
                question_number = 0
            prev_source = source[i - 1]

            if ignore_ai_responses:
                break

            results.append(pool.apply_async(partial_func, args=(question,)))

        # Get the results from the asynchronous calls
        for result in results:
            try:
                latest_ai_replies.append(result.get())

            except Exception as e:
                print(f"ERROR: {e}")

    latest_ai_replies_df = pd.DataFrame(
        latest_ai_replies,
        columns=["date_time", "question_asked", "question_source", "ai_reply", "value_reply", "ai_name"],
    )
    latest_ai_replies_df.to_csv(DB_PATH + "latest_ai_replies.csv", index=False, mode="w")
