import discord
import os
from discord.ext import commands
from activeAlertsCogs.Config.activeAlertsConfig import *

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

#

async def start():
    await client.wait_until_ready()
    client.db = await aiosqlite.connect("activeAlerts.db")

async def SetUpDB():
    await client.db.execute(f"CREATE TABLE IF NOT EXISTS moveBlacklist (guildID int, channelID int)")
    await client.db.execute(f"CREATE TABLE IF NOT EXISTS channelsBlacklist (guildID int, channelID int)")
    await client.db.execute(f"CREATE TABLE IF NOT EXISTS membersBlacklist (guildID int, memberID int)")
    await client.db.execute(f"CREATE TABLE IF NOT EXISTS activeTextChannels (guildID int, channelID int, categoryID int)")
    await client.db.execute(f"CREATE TABLE IF NOT EXISTS activeVoiceChannels (guildID int, channelID int, categoryID int)")
    await client.db.execute(f"CREATE TABLE IF NOT EXISTS active (guildID int, categoryID int, channelID int, messages text, timer text, remove text)")
    await client.db.execute(
        f"CREATE TABLE IF NOT EXISTS categories_channels (guildID int, categoryID int, channelID int, position int)")
    await client.db.execute(
        f"CREATE TABLE IF NOT EXISTS pingME (guildID int, channelID int, memberID int)")
    await client.db.execute("CREATE TABLE IF NOT EXISTS bannedCategories (guildID int, categoryID int)")
    await client.db.execute("CREATE TABLE IF NOT EXISTS servers (guildID int)")
    await client.db.commit()

@bot.event
async def on_ready():
    await client.wait_until_ready()
    client.db = await aiosqlite.connect("activeAlerts.db")

    await SetUpDB()
    DeActiveTextChannels.start()
    print(f"{client.user.name} is ready!")

@tasks.loop(seconds=60)
async def DeActiveTextChannels():
    await client.wait_until_ready()
    print("Starting")
    for guild in client.guilds:


        async with client.db.execute(f"SELECT * FROM active WHERE guildID = ?", (guild.id,)) as cursor:
            listOfAllItems = await cursor.fetchone()


        # times = db.child("remove_active").child(guild.id).get().val()

        if listOfAllItems == None:

            pass
        else:
            timer = int(listOfAllItems[5])
            move_blacklist = []
            async with client.db.execute(f"SELECT * FROM moveBlacklist WHERE guildID = ?",
                                              (guild.id,)) as cursor:
                listOfAllItems = await cursor.fetchall()

            if len(listOfAllItems) > 0:
                for i in listOfAllItems:
                    move_blacklist.append(int(i[0]))

            async with client.db.execute(f"SELECT * FROM activeTextChannels WHERE guildID = ?", (guild.id,)) as cursor:
                listOfAllItems = await cursor.fetchall()


            # activeChannels = db.child("is_active").get().val()
            activeChannelsList = []
            if len(listOfAllItems) > 0:
                for activeChannel in listOfAllItems:
                    activeChannelsList.append(activeChannel[1])

                for channelID in activeChannelsList:
                    channel = client.get_channel(int(channelID))

                    if channel is not None:


                        try:
                            message = await client.get_channel(channel.id).fetch_message(
                                channel.last_message_id)

                        except Exception:
                            message = None

                        if message is not None:

                            minutes = message.created_at.strftime('%M')
                            seconds = message.created_at.strftime('%S')
                            hours = message.created_at.strftime("%H")
                            days = message.created_at.strftime("%d")
                            month = message.created_at.strftime("%m")
                            year = message.created_at.strftime("%Y")
                            a = datetime(int(year), int(month), int(days), int(hours),
                                         int(minutes), int(seconds))
                            today = datetime.utcnow()
                            today_second = today.strftime("%S")
                            today_year = today.strftime("%Y")
                            today_month = today.strftime("%m")
                            today_day = today.strftime("%d")
                            today_hour = today.strftime("%H")
                            today_minute = today.strftime("%M")
                            b = datetime(int(today_year), int(today_month), int(today_day), int(today_hour),
                                         int(today_minute), int(today_second))

                            c = b - a
                            x = c.total_seconds()

                            if x > timer:


                                async with client.db.execute(
                                        f"SELECT categoryID FROM activeTextChannels WHERE channelID = ? AND guildID = ?", (channel.id, guild.id)) as cursor:
                                    listOfAllItems = await cursor.fetchone()
                                if listOfAllItems is not None:
                                    category_ID = listOfAllItems[0]

                                    old_channel_name = channel.name
                                    old_name = old_channel_name.split("-")

                                    category = client.get_channel(category_ID)
                                    for r in old_name:
                                        if r == "active":
                                            old_name.remove(r)
                                    name = ""
                                    for r in old_name:
                                        name += f"{r} "

                                    await client.db.execute(
                                        f'DELETE FROM activeTextChannels WHERE channelID = ? AND guildID = ?',
                                        (channel.id, guild.id))

                                    await client.db.commit()

                                    async with client.db.execute(
                                            f"SELECT * FROM categories_channels WHERE categoryID = ? AND guildID = ?",
                                            (category.id, guild.id)) as cursor:
                                        listOfAllItems = await cursor.fetchall()

                                        # db.child("categories&channels").child(
                                    # category.id).get().val()
                                    positionsss = []

                                    await channel.edit(name=name)

                                    if len(listOfAllItems) > 0:

                                        for i in listOfAllItems:
                                            positionsss.append((int(i[2]), int(i[3])))

                                        sorted_positions = sorted(positionsss, key=lambda t: t[1],
                                                                  reverse=False)

                                        for key, value in sorted_positions:
                                            channel2 = client.get_channel(int(key))
                                            if channel2 == None:
                                                continue
                                            else:
                                                if channel2.type == "category":
                                                    continue
                                                else:

                                                    if channel.id == int(key):
                                                        await channel.edit(position=int(value),
                                                                           category=category)
                                                    elif int(channel2.id) not in activeChannelsList:

                                                        await channel2.edit(position=int(value),
                                                                            category=category)
                        else:
                            async with client.db.execute(
                                    f"SELECT categoryID FROM activeTextChannels WHERE channelID = ? AND guildID = ?",
                                    (channel.id, guild.id)) as cursor:
                                listOfAllItems = await cursor.fetchone()
                            if listOfAllItems is not None:
                                category_ID = listOfAllItems[0]

                                old_channel_name = channel.name
                                old_name = old_channel_name.split("-")

                                category = client.get_channel(category_ID)
                                for r in old_name:
                                    if r == "active":
                                        old_name.remove(r)
                                name = ""
                                for r in old_name:
                                    name += f"{r} "

                                await client.db.execute(
                                    f'DELETE FROM activeTextChannels WHERE channelID = ? AND guildID = ?',
                                    (channel.id, guild.id))

                                await client.db.commit()

                                async with client.db.execute(
                                        f"SELECT * FROM categories_channels WHERE categoryID = ? AND guildID = ?",
                                        (category.id, guild.id)) as cursor:
                                    listOfAllItems = await cursor.fetchall()

                                # db.child("categories&channels").child(
                                # category.id).get().val()
                                positionsss = []

                                await channel.edit(name=name)

                                if len(listOfAllItems) > 0:

                                    for i in listOfAllItems:
                                        positionsss.append((int(i[2]), int(i[3])))

                                    sorted_positions = sorted(positionsss, key=lambda t: t[1],
                                                              reverse=False)

                                    for key, value in sorted_positions:
                                        channel2 = client.get_channel(int(key))
                                        if channel2 == None:
                                            continue
                                        else:
                                            if channel2.type == "category":
                                                continue
                                            else:

                                                if channel.id == int(key):
                                                    await channel.edit(position=int(value),
                                                                       category=category)
                                                elif int(channel2.id) not in activeChannelsList:

                                                    await channel2.edit(position=int(value),
                                                                        category=category)


@bot.command()
async def approve(ctx, guild: Guild = None):
    if guild is None:
        embed0 = Embed(title="How to use this command?", description=f"`{prefix}approve <serverID>`",
                       color=random_color())
        await ctx.send(embed=embed0)
        return
    embed = Embed(title="Approved",
                  color=random_color())
    await ctx.send(embed=embed)
    await client.db.execute("INSERT INTO servers VALUES (?)", (guild.id,))
    await client.db.commit()

    return


@bot.command()
async def deny(ctx, guild: Guild = None):
    if guild is None:
        embed0 = Embed(title="How to use this command?", description=f"`{prefix}deny <serverID>`",
                       color=random_color())
        await ctx.send(embed=embed0)
        return
    embed = Embed(title="Denied",
                  color=random_color())
    await ctx.send(embed=embed)
    await client.db.execute("DELETE FROM servers WHERE guildID = ?", (guild.id,))
    await client.db.commit()

    return

@bot.event
async def on_guild_join(guild):
    async with client.db.execute("SELECT * FROM servers") as cursor:
        allServers = await cursor.fetchall()
    servers = []
    for server in allServers:
        servers.append(server[0])
    if guild.id in servers or guild.id in [578268506999750656, 756513497411616888]:
        #(guildID int, categoryID int, channelID int, messages text, timer text, remove text)
        await client.db.execute("INSERT INTO active VALUES (?, ?, ?, ?, ?, ?)", (guild.id, 0, 0, 3, 600, 900))
        await client.db.commit()
        return
    else:
        channel = client.get_channel(796606534599704606)
        owner_id = guild.owner_id
        owner = guild.get_member(owner_id)
        embed = Embed(
            description=f"{owner} / ({owner.id}) has tried to invite me to their server `{guild.name} /  ({guild.id})` without being approved",
            color=random_color())
        embed.set_thumbnail(url=owner.avatar_url)
        await channel.send(embed=embed)

        await guild.leave()
        return

bot.remove_command("help")
@bot.command()
async def help(ctx, word=None):
    pass

async def load_extensions():
  for filename in os.listdir('./activeAlertsCogs'):
      if filename.endswith(".py"):
          await bot.load_extension(f'activeAlertsCogs.{filename[:-3]}')

if __name__ == "__main__":

    async def main():
        # await load_extensions()
        await bot.start(TOKEN)

    asyncio.run(main())
    
    # bot.loop.create_task(start())
    # bot.run(os.getenv('TOKEN'))
    # # client.run(TOKEN)
    # #client.run("ODQ2Mjc1Mjk1ODc0MjUyODMw.YKtJSQ.RBTu8uBAUh2l5WH2x4-pvuidn8E") #Main Bot
    # asyncio.run(client.db.close())