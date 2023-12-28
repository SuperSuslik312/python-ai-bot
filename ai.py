import g4f
from postgresql import *
from config import Config
import json

max_questions = Config.MAX_CONTEXT_QUESTIONS
max_tokens = Config.MAX_TOKENS
temperature = Config.TEMPERATURE
frequency_penalty = Config.FREQUENCY_PENALTY
presence_penalty = Config.PRESENCE_PENALTY


async def start_conversation(instructions):
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": "Привет! Кто ты?"}
    ]

    completion = g4f.ChatCompletion.create(
        provider=g4f.Provider.GeekGpt,
        model=g4f.models.gpt_4_32k,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1.0,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    return completion


async def update(instructions, user_id, new_question):
    messages = [
        {"role": "system", "content": instructions},
    ]

    history = await read_history(user_id)
    previous_questions_and_answers = json.loads(history) if history else []

    for question, answer in previous_questions_and_answers[-max_questions:]:
        messages.append({"role": "user", "content": question})
        messages.append({"role": "assistant", "content": answer})
    messages.append({"role": "user", "content": new_question})

    completion = g4f.ChatCompletion.create(
        provider=g4f.Provider.GeekGpt,
        model=g4f.models.gpt_4_32k,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1.0,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    previous_questions_and_answers.append((new_question, completion))
    history = json.dumps(previous_questions_and_answers)
    await edit_history(history, user_id)
    return completion
