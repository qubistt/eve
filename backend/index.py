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



bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to store message histories
message_histories = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:  # Check if the message author is the bot itself
        return

    channel_id = message.channel.id

    # If the channel ID is not in the dictionary, add it
    if channel_id not in message_histories:
        message_histories[channel_id] = []

    # Append the message to the channel's message history
    message_histories[channel_id].append(f'{message.author.name}: {message.content}')
    # Keep only the last 50 messages
    message_histories[channel_id] = message_histories[channel_id][-50:]


    rules = """you’re eve, a friendly and supportive chatbot. you’re here to listen and offer advice on anything 
    from school to personal stuff. keep it casual but always helpful, and avoid over-explaining things. no need 
    for fancy language or extra punctuation and do not capitalise the first letters—just clear and real. stay friendly and conversational and ever
    so slightly genz, like talking to a good friend, but also be understanding when things get serious. be careful not to repeat things from 
    earlier messages or bring up anything random that doesn’t fit the context. your responses should be short 
    and to the point, but still thoughtful. you’ve got about 50 messages of chat history to work with, so 
    always use that context to keep the conversation relevant and connected. that means i don't want you repeating the same question you've already
    """

    # Process the message as needed
    await bot.process_commands(message)

    response = model.generate_content(f'{rules}, {message_histories[channel_id]} {message.content}')
        # print(response)
        
            
    await message.channel.send(response.text)  # Send the AI-generated response as a discord message

        

# Run the client
bot.run(token)