# Created by Alexander Röst 5th of May 2022
# Please contact me on Github should you have any questions.

import discord

TOKEN = 'hidden'

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

client.run(TOKEN)

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}, {user_message}, {channel}')

    if message.author == client.user:
        return

    if message.channel.name == 'general':
        if user_message.lower == 'hello':
            await message.channel.send(f'Hello {username}')
            return
        elif user_message.lower == '!random':
            response = f'this is your random number: 1. f you'
            await message.channel.send(response)
            return

