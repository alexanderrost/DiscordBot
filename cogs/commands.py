import math

import discord
from discord import Embed
from discord.ext import commands
import wavelink
import mysql.connector
import lavalink
from mysql.connector import errorcode


class Commands(commands.Cog):
    # Do this so we can access the client, big innit fam
    def __init__(self, client):
        self.client = client

    async def db_stats(self, stats):
        # More database stuff because I might've messed up? whoopsie
        cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='discord_stats')
        mycursor = cnx.cursor()
        query = "UPDATE stats SET count = count + 1 WHERE name = '{}'".format(stats)
        mycursor.execute(query)
        cnx.commit()
        cnx.close()

    # The int determines how many messages we'd like to clear out.
    # .clear 100 will remove the previous 100 messages(99 realisticly since it counts the msg to call the command)
    @commands.command()
    async def clear(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await self.db_stats("commands_run")
        embed = Embed()
        embed = discord.Embed(title=f'Used clear command',
                              description=f'Removed {limit} messages!')

        await ctx.channel.send(embed=embed)

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
        await vc.play(search)
        embed = Embed()
        embed = discord.Embed(title=f'Playing {search.title}',
                              description='Enjoy the song!')

        await ctx.channel.send(embed=embed)
        await self.db_stats("songs_played")
        await self.db_stats("commands_run")

    # Use this command to pause the music
    @commands.command()
    async def pause(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        embed = Embed()
        embed = discord.Embed(title=f'Paused song',
                              description='')

        await ctx.channel.send(embed=embed)
        await vc.set_pause(True)
        await self.db_stats("commands_run")

    # This function unpauses the music
    @commands.command()
    async def unpause(self, ctx):
        vc: wavelink.Player = ctx.voice_client

        embed = Embed()
        embed = discord.Embed(title=f'Unpaused song',
                              description='')

        await ctx.channel.send(embed=embed)
        await vc.set_pause(False)
        await self.db_stats("commands_run")

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
        embed = Embed()
        embed = discord.Embed(title=f'Stopped playing',
                              description='')

        await ctx.channel.send(embed=embed)
        await self.db_stats("commands_run")


def setup(client):
    client.add_cog(Commands(client))
