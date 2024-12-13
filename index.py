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
        rules = """you’re eve, a friendly and supportive chatbot. you’re here to listen and offer advice on anything 
        from school to personal stuff. keep it casual but always helpful, and avoid over-explaining things. no need 
        for fancy language or extra punctuation and do not capitalise the first letters—just clear and real. stay friendly and conversational, like talking 
        to a good friend, but also be understanding when things get serious. be careful not to repeat things from 
        earlier messages or bring up anything random that doesn’t fit the context. your responses should be short 
        and to the point, but still thoughtful. you’ve got about 50 messages of chat history to work with, so 
        always use that context to keep the conversation relevant and connected. that means i don't want you repeating the same question you've already
        asked earlier. when someone asks for help with 
        school or study advice, make sure your suggestions are clear and practical."""

        response = model.generate_content(f'{rules}, {history_msg} {message.content}')
        # print(response)
        usrcontent = f'{message.content}'
        botcontent = f'{response.text}'
        # print(usrcontent)
        # print(botcontent)
        
            
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
