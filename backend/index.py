import discord
from discord import app_commands
from discord.ext import commands, tasks
import google.generativeai as genai
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables from .env file
load_dotenv()

gemini_api = str(os.getenv('GEMINI_API'))
token = str(os.getenv('TOKEN'))

genai.configure(api_key=gemini_api)
model = genai.GenerativeModel("models/gemini-1.5-flash")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to store message histories and pet data
channel_data = {}

@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print(f'Logged in as {bot.user}')
        pet_status_update.start()  # Start the background task
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:  # Check if the message author is the bot itself
        return

    channel_id = message.channel.id

    # If the channel ID is not in the dictionary, add it
    if channel_id not in channel_data:
        channel_data[channel_id] = {'messages': [], 'pet': None}

    # Append the message to the channel's message history
    channel_data[channel_id]['messages'].append(f'{message.author.name}: {message.content}')
    # Keep only the last 50 messages
    channel_data[channel_id]['messages'] = channel_data[channel_id]['messages'][-50:]

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

    response = model.generate_content(f'{rules}, {channel_data[channel_id]["messages"]} {message.content}')
        
    await message.channel.send(response.text)  # Send the AI-generated response as a discord message

# Background task to update pet status
@tasks.loop(minutes=10)  # Adjust the interval as needed
async def pet_status_update():
    for channel_id, data in channel_data.items():
        pet = data.get('pet')
        if pet:
            pet['food'] -= 10  # Decrease food level
            if pet['food'] < 0:
                pet['food'] = 0
                pet['health'] -= 10  # Decrease health if food is 0
                if pet['health'] < 0:
                    pet['health'] = 0

# Slash command to create a pet
@bot.tree.command(name="create_pet", description="Create a pet (dog or cat)")
async def create_pet(interaction: discord.Interaction, pet_type: str):
    channel_id = interaction.channel_id

    # Ensure the channel ID is in the dictionary
    if channel_id not in channel_data:
        channel_data[channel_id] = {'messages': [], 'pet': None}

    if pet_type.lower() not in ["dog", "cat"]:
        await interaction.response.send_message("Invalid pet type! Please choose either 'dog' or 'cat'.")
        return

    channel_data[channel_id]['pet'] = {
        'type': pet_type.lower(),
        'health': 100,
        'food': 100
    }
    await interaction.response.send_message(f"A {pet_type.lower()} has been created!")

# Slash command to check pet status
@bot.tree.command(name="pet_status", description="Check the status of your pet")
async def pet_status(interaction: discord.Interaction):
    channel_id = interaction.channel_id
    pet = channel_data[channel_id].get('pet')

    if not pet:
        await interaction.response.send_message("No pet found in this channel. Create one using /create_pet.")
        return

    await interaction.response.send_message(f"Your {pet['type']} has {pet['health']} health and {pet['food']} food.")

# Slash command to feed the pet
@bot.tree.command(name="feed_pet", description="Feed your pet")
async def feed_pet(interaction: discord.Interaction):
    channel_id = interaction.channel_id
    pet = channel_data[channel_id].get('pet')

    if not pet:
        await interaction.response.send_message("No pet found in this channel. Create one using /create_pet.")
        return

    pet['food'] = min(pet['food'] + 20, 100)
    await interaction.response.send_message(f"You fed your {pet['type']}. Its food level is now {pet['food']}.")

# Run the bot
bot.run(token)