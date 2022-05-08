import discord
from discord.ext import commands
import wavelink


class Commands(commands.Cog):
    # Do this so we can access the client, big innit fam
    def __init__(self, client):
        self.client = client

    # The int determines how many messages we'd like to clear out.
    # .clear 100 will remove the previous 100 messages(99 realisticly since it counts the msg to call the command)
    @commands.command()
    async def clear(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit)

    @commands.command()
    async def play(self, ctx, *, search: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.play(search)


def setup(client):
    client.add_cog(Commands(client))
