import openai
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token= 'YOUR TOKEN HERE')
dp = Dispatcher(bot)

openai.api_key = "YOUR API KEY HERE"

@dp.message_handler(commands = ['start', 'help'])
async def welcome(message: types.Message):
    await message.reply('Hello! I am your buddy. Feel free to chat with me.')

history = []

def BasicGeneration(userPrompt):
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=userPrompt,
        temperature=0.8,
        max_tokens=50,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    result = completion.choices[0].text
    print("\nFULL RESPONSE: ", result, "\n")
    return result



@dp.message_handler()
async def gpt(message: types.Message):

    prompt_request = "You are a counsellor and chatting with me. " \
                     "There are 3 emotions: Positive, Negative, Neutral. " \
                     "Analysis my current emotion and only return the emotion classification in this template: {emotion}." \
                     "Don't include any explanation, just the emotion. of the following content: "

    prompt_happy = "You are happy with me and encourage me to share more happy things or express how happy I am."
    prompt_comfort = "I am in a negative emotion now. Find a way to comfort me and make me feel happy again with 2 to 3 sentences. " \
                     "It can be showing support or other positive things."
    prompt_neutral = "You fail to detect my mood or my emotion. " \
                     "So you now have to encourage me to talk more without telling me you missed my mood or emotion in 1 to 2 sentences. " \
                     "You also cannot assume I am either in a good or bad mood. You should not return a history-liked response." \
                     "The conversation history is not a template for your response." \
                     "You may start by asking random neutral question about my work or life, etc, something that is not so directly related to my mood."
    prompt_general = "Continue to chat with me. If I ask a question, answer it and also consider my current mood. " \
                     "If I greet you, then you greet me back. But only need to greet once. If you have greeted me before, you do not need to greet me again." \
                     "Remember you are a consellor. Your response should like a human, chatting with me. " \
                     "The conversation history is not a template for your response."

    myinput = message.text
    history.append({"role": "user", "content": myinput})
    emotionDetected = BasicGeneration(prompt_request + str(history))
    print("\n EMOTION: ", emotionDetected, "\n")

    response = []
    if "Positive" in emotionDetected:
        response = BasicGeneration(prompt_general + prompt_happy + str(history))

    elif "Negative" in emotionDetected:
        response = BasicGeneration(prompt_general + prompt_comfort + str(history))

    else:
        response = BasicGeneration(prompt_general + prompt_neutral + str(history))

    print("\n==== Response ==== ")
    print(response)
    print("==== ==== ==== \n")
    history.append({"role": "system", "content": response})
    await message.reply(response)

if __name__ == "__main__":
    executor.start_polling(dp)
