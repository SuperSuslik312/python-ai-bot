import openai

from config import Config

openai.api_key = Config.API_KEY
max_questions = Config.MAX_CONTEXT_QUESTIONS
max_tokens = Config.MAX_TOKENS
temperature = Config.TEMPERATURE
frequency_penalty = Config.FREQUENCY_PENALTY
presence_penalty = Config.PRESENCE_PENALTY

def start_conversation(instructions):
    messages = [
        { "role": "system", "content": instructions },
        { "role": "user", "content": "Привет! Кто ты?" }
    ]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1.0,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    return completion['choices'][0]['message']['content']

def update(instructions, previous_questions_and_answers, new_question):
    messages = [
        { "role": "system", "content": instructions },
    ]

    for question, answer in previous_questions_and_answers[-max_questions:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    messages.append({"role": "user", "content": new_question})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1.0,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    return completion['choices'][0]['message']['content']