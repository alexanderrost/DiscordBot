# Created by Alexander Röst 5th of May 2022
# Please contact me on Github should you have any questions.

# TODO add media playing, trivia/quiz & statistics. polling? (mostly statistics)
import os
import discord
from discord.ext import commands

# Extracting token from seperate file(sneaky)
with open("./data/token.0", "r", encoding="utf-8") as f:
    # Your discord token goes here, don't let other people know your token
    TOKEN = f.read()

# Intents are the events(actions) our bot is looking for
# For example we need members to be true in order to have our welcome message work
intents = discord.Intents.default()
intents.members = True

# Make sure the intents are specified here
# This also adds our prefix for commands
client = commands.Bot(command_prefix='.', intents=intents, case_insensitive=True)


# Used for loading cogs
@client.command()
async def load(ctx, extensions):
    client.load_extension('cogs.{}'.format(extensions))


# Used for unloading cogs
@client.command()
async def unload(ctx, extensions):
    client.unload_extension('cogs.{}'.format(extensions))


# List all the files in cogs for us to load them
for filename in os.listdir('./cogs'):
    # Make sure the file we pick are using the .py format
    if filename.endswith('.py'):
        # Here we splice the filename to remove the .py in our string
        client.load_extension(f'cogs.{filename[:-3]}')

# This just starts the client
# Not sure if this needs to be down here, but i'm to lazy to move it
client.run(TOKEN)
