# Created by Alexander Röst 5th of May 2022
# Please contact me on Github should you have any questions.

import discord

# Your discord token goes here, don't let other people know your token
TOKEN = ''

# Intents are the events(actions) our bot is looking for
# For example we need members to be true in order to have our welcome message work
intents = discord.Intents(messages=True, guilds=True, members=True)

# Make sure the intents are specified here
client = discord.Client(intents=intents)


# This will be the function run once the bot is ready to use
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.wait_until_ready()


# on_message deals with incoming messages and commands
@client.event
async def on_message(message):
    # This gives us just the name. zer0#2569 -> zer0
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print('{}, {}, {}'.format(username, user_message, channel))

    # This prevents the bot from replying to itself, that could lead to some issues!
    if message.author == client.user:
        return

    # Check if the message it saw is &gm and then reply aswell as tag the user
    if user_message == '&gm':
        print('test')
        await message.channel.send('Good Morning G :sunglasses: {}'.format(message.author.mention))
        return

    elif user_message == '&gn':
        response = 'Dont let the bedbugs bite :smiling_imp: {}'.format(message.author.mention)
        await message.channel.send(response)
        return

# This block will be used to welcome new members
@client.event
async def on_member_join(member):
    channel = member.guild.system_channel
    embed = discord.Embed(title="Welcome to the party", description="{} has just joined!".format(member.mention))
    embed.set_author(name=member, icon_url=member.avatar_url)
    await channel.send(embed=embed)

# This just starts the client
# Not sure if this needs to be down here, but i'm to lazy to move it
client.run(TOKEN)
