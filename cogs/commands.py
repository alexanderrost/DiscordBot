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

    # Play a song with .play url
    @commands.command()
    async def play(self, ctx, *, search: wavelink.YouTubeTrack):
        # If we're not connected to vc, connect
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            # If we're connected to vc, set vc to our client
            vc: wavelink.Player = ctx.voice_client
        # Play the requested song
        print(vc.volume)
        await vc.play(search)

    # Use this command to pause the music
    @commands.command()
    async def pause(self, ctx):
        vc: wavelink.Player = ctx.voice_client

        await vc.set_pause(True)

    # This function unpauses the music
    @commands.command()
    async def unpause(self, ctx):
        vc: wavelink.Player = ctx.voice_client

        await vc.set_pause(False)

    # Stop playing the current song
    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            vc: wavelink.Player = ctx.voice_client
            if vc.is_playing():
                await vc.stop()
            else:
                return
        else:
            return



def setup(client):
    client.add_cog(Commands(client))
