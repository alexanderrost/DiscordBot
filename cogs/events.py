import discord
from discord.ext import commands


class Events(commands.Cog):
    # Do this so we can access the client, big innit fam
    def __init__(self, client):
        self.client = client

    # new name for events when using cogs
    @commands.Cog.listener()
    # This will be the function run once the bot is ready to use
    async def on_ready(self):
        await self.client.wait_until_ready()
        print('We have logged in as {0.user}'.format(self.client))

    @commands.Cog.listener()
    # on_message deals with incoming messages and commands
    async def on_message(self, message):
        # This gives us just the name. zer0#2569 -> zer0
        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        channel = str(message.channel.name)
        print('{}, {}, {}'.format(username, user_message, channel))

        # This prevents the bot from replying to itself, that could lead to some issues!
        if message.author == self.client.user:
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

        # This is needed or else the bot gets stuck looking for messages instead of commands
        # await self.client.process_commands(message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        embed = discord.Embed(title="Welcome to the party", description="{} has just joined!".format(member.mention))
        embed.set_author(name=member, icon_url=member.avatar_url)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system.channel
        embed = discord.Embed(title="It was fun while it lasted",
                              description="{} has left the server. Member since: {}".format(member, member.joined_at))
        embed.set_author(name=member, icon_url=member.avatar_url)
        await channel.send(embed=embed)


def setup(client):
    client.add_cog(Events(client))
