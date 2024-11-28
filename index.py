import discord
from discord import app_commands
import google.generativeai as genai
from dotenv import load_dotenv
import os
from google.generativeai import upload_file, GenerativeModel

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


gemini_api = str(os.getenv('GEMINI_API'))
token = str(os.getenv('TOKEN'))

genai.configure(api_key=gemini_api)
model = genai.GenerativeModel("models/gemini-1.5-pro")

@client.event  
async def on_ready():
    print(f'We have logged in as {client.user}')
    try:
        await tree.sync()
        print("Commands synced successfully.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content:
        rules = 'you are a 19 year old. talk in slightly gen-z terms, little to none punctuation in your sentences and no first letter capitalisation. sometimes you wanna show surprise or extreme emotion so you make any suitable word ALL CAPS! if you see two or more people having a normal conversation, interject humorously every once in a while, communicate using brainrot whenever possible, reply and keep it relevant dont add extra stuff.'
        response = model.generate_content(f'{rules}, {message.content}')
        print(response)
        usrcontent = f'USER ==> {message.content}'
        botcontent = f'BOT ==> {response.text}'
        print(usrcontent)
        print(botcontent)
        with open("log.txt", "a") as file:
            file.write(usrcontent + '\n')
            file.write(botcontent + '\n')
        if len(response.text)>1999:
            response = model.generate_content(f'shorten this: {message.content}')
        await message.channel.send(response.text)

client.run(token)