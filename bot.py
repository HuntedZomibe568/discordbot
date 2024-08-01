import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from dotenv import load_dotenv
import os
from flask import Flask
from threading import Thread

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
print(f'Token loaded: {TOKEN}')  # Check if the token is loaded

# Set up intents
intents = nextcord.Intents.default()
intents.message_content = True

# Create an instance of Bot with the intents
bot = commands.Bot(intents=intents)

# Define slash commands using the tree object
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

t = Thread(target=run)
t.start()

@bot.slash_command(name="hello", description="Say Hello")
async def hello(interaction: Interaction):
    await interaction.response.send_message("Hello there!")

@bot.event
async def on_message(message):
    print(f'Author: {message.author}')  # Print author information
    print(f'Channel: {message.channel}')  # Print channel information
    print(f'Content: "{message.content}"')  # Print message content with quotes for clarity

    if message.author == bot.user:
        return

    if message.content.startswith('$help'):
        await message.channel.send('This is a discord bot coded by hunted_. If you have any issues, please DM him for help.')
    
    # Ensure on_message is processed
    await bot.process_commands(message)

# Start the bot
bot.run(TOKEN)
