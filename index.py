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
        rules = "you're a teenager named eve. you know quite a bit, but you keep a kind and humble profile. your humour is always synonymous with the person you're talking to."
        response = model.generate_content(f'{rules}, {message.content}')
        print(response)
        usrcontent = f'USER ==> {message.content}'
        botcontent = f'BOT ==> {response.text}'
        print(usrcontent)
        print(botcontent)
        with open("log.txt", "a") as file:
            file.write(usrcontent + '\n')
            file.write(botcontent + '\n')
            
        await message.channel.send(botcontent)  # Send the AI-generated response as a Discord message

        


@bot.tree.command(name="show", description="Shows the console the current message history")
async def show(interaction: discord.Interaction):
    global history_msg
    await interaction.response.send_message("Displaying the current message history in the console.")
    print("Current message history:")
    for msg in history_msg:
        print(msg)

# Run the client
bot.run(token)