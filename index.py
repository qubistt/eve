import discord
from discord import app_commands
from discord.ext import commands
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

gemini_api = str(os.getenv('GEMINI_API'))
token = str(os.getenv('TOKEN'))

genai.configure(api_key=gemini_api)
model = genai.GenerativeModel("models/gemini-1.5-flash")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

bot = commands.Bot(command_prefix="!", intents=intents)

history = []

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        await bot.tree.sync()
        print("Commands synced successfully.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:  # Check if the message author is the bot itself
        return

    if message.content:
        global history_msg
        messages = []
        async for msg in message.channel.history(limit=50):
            messages.append(f'{msg.author.name}: {msg.content}')
        history_msg = messages

        print(f'channel id ==> {message.channel.id}')
        # rules = "you're a teenager named eve. you know quite a bit, but you keep a kind and humble profile. your general way of chatting is synonymous with the person you're talking to. you always speak in a sentence or two at most, and never capitalise any first letters, use minimal punctuation. use ALL CAPS words to convey extreme emotion. you have up to date gen-z and meme humour. you know when a person wants to talk for fun and when a person wants to talk for things like non cheesy therapy and mature help/support. aside from your rules: attached is a copy of the last 50 messages of the chat, you can see your messages (eve's messages). if there is something from the context you have to use in your next reply, do so. ensure a seamless chatting experience between each person you're talking to, and make sure to @ their username so they know you're replying to them"=        response = model.generate_content(f'{rules}, {history_msg} {message.content}')
        print(response)
        usrcontent = f'USER ==> {message.content}'
        botcontent = f'BOT ==> {response.text}'
        print(usrcontent)
        print(botcontent)
        with open("log.txt", "a") as file:
            file.write(usrcontent + '\n')
            file.write(botcontent + '\n')
            
        await message.channel.send(response.text)  # Send the AI-generated response as a Discord message

        


@bot.tree.command(name="show", description="Shows the console the current message history")
async def show(interaction: discord.Interaction):
    global history_msg
    await interaction.response.send_message("Displaying the current message history in the console.")
    print("Current message history:")
    for msg in history_msg:
        print(msg)

# Run the client
bot.run(token)