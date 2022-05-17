import discord
from discord.ext import commands
import wavelink
import mysql.connector
from mysql.connector import errorcode


class Events(commands.Cog):
    # Do this so we can access the client, big innit fam

    def __init__(self, client):
        self.client = client

    # Database stuff
    try:
        # Try to connect to the database
        cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='discord_stats')
    # If it can't find the database, we go here and create one! how nice
    except mysql.connector.Error as err:
        cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1')
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist, creating...')
            mycursor = cnx.cursor()
            mycursor.execute("CREATE DATABASE discord_stats")
            # Tables and db name
            # Here we add all the statistics we want to keep track off
            DB_NAME = "discord_stats"
            TABLES = {'stats': (
                "CREATE TABLE `stats` ("
                "  `name` char(100),"
                "  `count` bigint(14) ,"
                "  `id` bigint(14)  NOT NULL AUTO_INCREMENT ,"
                "  PRIMARY KEY (`id`)"
                ") ENGINE=InnoDB")}

            # Not sure if we need another connection here, ive done so in the past?? nvm its because of the database arg
            # How have I not figured that out until now. Welp
            cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='discord_stats')
            # Cursor is a database handler, it helps us execute all commands
            cursor = cnx.cursor(buffered=True)
            cursor.execute("USE {}".format(DB_NAME))
            # Use a for-loop to create the tables using the information in TABLES[]
            for table_name in TABLES:
                table_description = TABLES[table_name]
                try:
                    print("Creating table {}: ".format(table_name), end='')
                    cursor.execute(table_description)
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        print("Table already exists")
                    else:
                        print(err.msg)
                else:
                    print("OK")

            cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='discord_stats')
            query1 = "insert into `stats`(`name`,`count`) values (%s, %s) "
            val = ("messages_in_chat", 0)
            query2 = "insert into `stats`(`name`,`count`) values (%s, %s) "
            val2 = ("commands_run", 0)
            query3 = "insert into `stats`(`name`,`count`) values (%s, %s) "
            val3 = ("songs_played", 0)

            cnx.cursor().execute(query1, val)
            cnx.cursor().execute(query2, val2)
            cnx.cursor().execute(query3, val3)

            cnx.commit()

        else:
            print(err)



    async def db_stats(self, stats):
        # More database stuff because I might've messed up? whoopsie
        cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='discord_stats')
        mycursor = cnx.cursor()
        query = "UPDATE stats SET count = count + 1 WHERE name = '{}'".format(stats)
        mycursor.execute(query)
        cnx.commit()
        cnx.close()

    # new name for events when using cogs
    @commands.Cog.listener()
    # This will be the function run once the bot is ready to use
    async def on_ready(self):
        await self.client.wait_until_ready()
        await self.client.change_presence(status=discord.Status.dnd, activity=discord.Game('Beep Boop I am Robot'))
        print('We have logged in as {0.user}'.format(self.client))
        self.client.loop.create_task(self.node_connect())

    @commands.Cog.listener()
    # connect to a free open node
    async def node_connect(self):
        await self.client.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.client, host='lavalinkinc.ml', port=443, password='incognito',
                                            https=True)

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node {node.identifier} is connected.')

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
        await self.db_stats("messages_in_chat")

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
