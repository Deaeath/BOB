from activeAlertsCogs.Config.activeAlertsConfig import *


class Active(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):

        print('Active is ready')

    @commands.command()
    async def pingme(self, ctx, *, channels=None):
        if channels == None:
            embed0 = Embed(title="How to use this command?",
                           description=f"`{ctx.message.content} <#channel1> [#channel2] [#channel3]",
                           color=random_color())
            embed0.add_field(name="Note", value="Please make sure to separate the channels with spaces", inline=False)
            await ctx.send(embed=embed0)
            return
        else:
            list_of_channels = channels.split(" ")
            failed = ""
            success = ""
            already_subscribed_to = ""
            try:
                async with self.client.db.execute(
                        f"SELECT * FROM pingME WHERE memberID = ? AND guildID = ?", (ctx.author.id, ctx.guild.id)) as cursor:
                    listOfAllItems = await cursor.fetchall()
            except Exception:
                pass
            PingMeInThere = []
            if len(listOfAllItems) > 0:

                for i in listOfAllItems:
                    PingMeInThere.append(int(i[1]))

            for channel_name in list_of_channels:
                channel_ID = re.sub('[<>&!@#$]', '', channel_name)
                channel = self.client.get_channel(int(channel_ID))

                if channel == None:
                    failed += f"{channel_name}\n"
                else:

                    if channel.id not in PingMeInThere:
                        await self.client.db.execute(
                            f'INSERT INTO pingME VALUES (?, ?, ?)', (ctx.guild.id, channel.id, ctx.author.id))
                        await self.client.db.commit()
                        success += f"{channel.mention}\n"
                    else:

                        already_subscribed_to += f"{channel.mention}\n"

            embed = Embed(color=random_color())
            if success == "":
                success = "None"
            embed.add_field(name="Success", value=success or "None", inline=True)
            if failed == "":
                failed = "None"
            embed.add_field(name="Failed", value=failed or "None", inline=True)
            if already_subscribed_to == "":
                already_subscribed_to = "None"
            embed.add_field(name="Already Subscribed to", value=already_subscribed_to, inline=False)
            await ctx.send(embed=embed)


    @commands.command()
    async def unpingme(self, ctx, *, channels=None):
        if channels == None:
            embed0 = Embed(title="How to use this command?",
                           description=f"`{ctx.message.content} <#channel1> [#channel2] [#channel3]",
                           color=random_color())
            embed0.add_field(name="Note", value="Please make sure to separate the channels with spaces", inline=False)
            await ctx.send(embed=embed0)
            return
        else:
            list_of_channels = channels.split(" ")
            failed = ""
            success = ""
            not_subscribed_to = ""
            try:
                async with self.client.db.execute(
                        f"SELECT * FROM pingME WHERE memberID = ? AND guildID = ?", (ctx.author.id, ctx.guild.id)) as cursor:
                    listOfAllItems = await cursor.fetchall()
            except Exception:
                pass

            if len(listOfAllItems) == 0:
                text = "You haven't subscribed to any channel yet!"

                embed0 = Embed(title=text, color=random_color())
                await ctx.send(embed=embed0)
                return
            PingMeInThere = []
            for i in listOfAllItems:
                PingMeInThere.append(int(i[1]))

            for channel_name in list_of_channels:
                channel_ID = re.sub('[<>&!@#$]', '', channel_name)
                channel = self.client.get_channel(int(channel_ID))
                if channel == None:
                    failed += f"{channel_name}\n"
                else:

                    if channel.id not in PingMeInThere:
                        not_subscribed_to += f"{channel.mention}\n"


                    else:
                        exists = False
                        for key in PingMeInThere:
                            if key == channel.id:
                                exists = True
                        if exists == True:
                            await self.client.db.execute(
                                f'DELETE FROM pingME WHERE memberID = ? AND channelID = ? AND guildID = ?', (ctx.author.id, channel.id, ctx.guild.id))

                            await self.client.db.commit()
                            success += f"{channel.mention}\n"
                        else:
                            not_subscribed_to += f"{channel.mention}\n"
            embed = Embed(color=random_color())
            if success == "":
                success = "None"
            embed.add_field(name="Success", value=success or "None", inline=True)
            if failed == "":
                failed = "None"
            embed.add_field(name="Failed", value=failed or "None", inline=True)
            if not_subscribed_to == "":
                not_subscribed_to = "None"
            embed.add_field(name="Not Subscribed to", value=not_subscribed_to, inline=False)
            await ctx.send(embed=embed)

    @commands.command(aliases=["subscribed-channels", "subscribed"])
    async def subscribed_channels(self, ctx, member: Member = None):
        if member == None:
            member = ctx.author


        async with self.client.db.execute(f"SELECT * FROM pingME WHERE memberID = ? AND guildID = ?", (ctx.author.id, ctx.guild.id)) as cursor:
            listOfAllItems = await cursor.fetchall()


        if len(listOfAllItems) == 0:
            if member.id == ctx.author.id:
                text = "You haven't subscribed to any channel yet!"
            else:
                text = f"{member.mention} hasn't subscribed to any channel yet!"
            embed0 = Embed(title=text, color=random_color())
            await ctx.send(embed=embed0)
            return
        PingMeInThere = []

        for i in listOfAllItems:
            PingMeInThere.append(int(i[1]))
        else:
            channels = ""
            for key in PingMeInThere:
                channel = self.client.get_channel(int(key))
                if channel is not None:
                    
                    channels += f"{channel.mention} - "
            if len(channels) > 2000:
                if member.id == ctx.author.id:
                    channels = f"You are subscribed to **{len(channels)}** channels"
                else:
                    channels = f"{member.mention} is subscribed to **{len(channels)}** channels"
            else:
                channels = channels[:-3]
            embed = Embed(title="Subscribed Channels", description=channels, color=random_color())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            if member.id != ctx.author.id:
                embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return

    @commands.command(aliases=["subscribed-members"])
    async def subscribed_members(self, ctx, channel: TextChannel = None):
        if channel == None:
            embed0 = Embed(title="How to use this command?", description=f"`{ctx.message.content} <#channel>`",
                           color=random_color())
            await ctx.send(embed=embed0)
            return
        try:
            async with self.client.db.execute(f"SELECT * FROM pingME WHERE channelID = ? AND guildID = ?", (channel.id, ctx.guild.id)) as cursor:
                listOfAllItems = await cursor.fetchall()
        except Exception:
            pass

        if len(listOfAllItems) == 0:
            embed0 = Embed(title="This channel has no subscribers!", color=random_color())
            await ctx.send(embed=embed0)
            return
        PingMeInThere = []
        list_of_members = []
        for i in listOfAllItems:
            PingMeInThere.append((int(i[2]), int(i[1])))
        for key, value in PingMeInThere:
            member = ctx.guild.get_member(int(key))
            if member is not None:
               
                list_of_members.append(member.id)
       
        if len(list_of_members) == 1:
            msg = f"Only {len(list_of_members)} member is subscribed to {channel.mention}"
        else:
            msg = f"A total of {len(list_of_members)} members are subscribed to {channel.mention}"
        embed = Embed(description=msg, color=random_color())
        await ctx.send(embed=embed)
        return

    @commands.command(aliases=["return-positions"])
    async def return_positions(self, ctx, category_ID=None):
        async with self.client.db.execute("SELECT * FROM bannedCategories WHERE guildID = ?",
                                          (ctx.guild.id,)) as cursor:
            banned_categories = await cursor.fetchall()
        bannedCategories = []
        for bCategory in banned_categories:
            bannedCategories.append(bCategory[1])
        if category_ID == None:
            embed1 = Embed(title="Re-arranging all categories according to the Database",
                           description="Please wait...", color=random_color())
            e = await ctx.send(embed=embed1)
            await asyncio.sleep(5)
            embed = Embed(title="Finished re-arranging all categories", color=random_color())
            
            
            for category in ctx.guild.categories:

                if category.id in bannedCategories:
                    continue
                else:
                    m = ""
                    async with self.client.db.execute(
                            f"SELECT * FROM categories_channels WHERE categoryID = ?", (category.id,)) as cursor:
                        listOfAllItems = await cursor.fetchall()
                    positionsss = []
                    if len(listOfAllItems) == 0:
                        embed0 = Embed(title="There is no positions stored in the database!", color=random_color())
                        await ctx.send(embed=embed0)
                        return
                    for i in listOfAllItems:
                        positionsss.append((int(i[2]), int(i[3])))

                    sorted_positions = sorted(positionsss, key=lambda t: t[1], reverse=False)
                    for key, value in sorted_positions:
                        channel2 = self.client.get_channel(int(key))
                        if channel2 == None:
                            continue
                        else:
                            if channel2.type == "category":
                                continue
                            else:
                                await channel2.edit(position=value, category=category)
                                m += f"{channel2.name} - {channel2.type} - #{value}\n"

                                if len(m) < 2000:
                                    embed2 = Embed(title=f"Resetting {category.name}", description=f"{m}",
                                                   color=random_color())
                                    await e.edit(embed=embed2)
                                else:
                                    m = "Text exceeded the **2024** characters"
                                    embed2 = Embed(title=f"Resetting {category.name}", description=f"{m}",
                                                   color=random_color())
                                    await e.edit(embed=embed2)
                    if m != "":
                        if len(m) < 1024:
                            embed.add_field(name=category.name, value=m, inline=True)
                        else:
                            m = "Text exceeded the **1024** characters"
                            embed.add_field(name=category.name, value=m, inline=True)
            await ctx.send(embed=embed)
            await e.delete()
            return
        else:
            exists = False
            for category in ctx.guild.categories:
                if category.id in bannedCategories:
                    continue
                else:
                    if category.id == int(category_ID):
                        exists = True
            if exists == True:
                category = self.client.get_channel(int(category_ID))
                embed1 = Embed(title=f"Re-arranging in {category.name} according to the Database",
                               description="Please wait...", color=random_color())
                e = await ctx.send(embed=embed1)
                await asyncio.sleep(5)
                embed = Embed(title=f"Finished re-arranging in {category.name}", color=random_color())
                m = ""
                async with self.client.db.execute(
                        f"SELECT * FROM categories_channels WHERE categoryID = ?", (category.id,)) as cursor:
                    listOfAllItems = await cursor.fetchall()
                if len(listOfAllItems) == 0:
                    embed0 = Embed(title="There is no positions stored in the database!", color=random_color())
                    await ctx.send(embed=embed0)
                    return
                positionsss = []

                for i in listOfAllItems:
                    positionsss.append((int(i[2]), int(i[3])))

                sorted_positions = sorted(positionsss, key=lambda t: t[1], reverse=False)
                for key, value in sorted_positions:
                    channel2 = self.client.get_channel(int(key))
                    if channel2 == None:
                        continue
                    else:
                        if channel2.type == "category":
                            continue
                        else:
                            await channel2.edit(position=value)
                            m += f"{channel2.name} - {channel2.type} - #{value}\n"

                            if len(m) < 2000:
                                embed2 = Embed(title=f"{category.name}", description=f"{m}",
                                               color=random_color())
                                await e.edit(embed=embed2)
                            else:
                                m = "Text exceeded the **2024** characters"
                                embed2 = Embed(title=f"{category.name}", description=f"{m}",
                                               color=random_color())
                                await e.edit(embed=embed2)

                await asyncio.sleep(5)
                if m != "":
                    if len(m) < 1024:
                        embed.add_field(name=category.name, value=m, inline=True)
                    else:
                        m = "Text exceeded the **1024** characters"
                        embed.add_field(name=category.name, value=m, inline=True)

                await ctx.send(embed=embed)
                await e.delete()
                return
            else:
                if int(category_ID) in bannedCategories:
                    embed0 = Embed(title="This category can't be changed!", color=random_color())
                    await ctx.send(embed=embed0)
                    return
                else:
                    embed0 = Embed(title="No category was found with such ID", color=random_color())
                    await ctx.send(embed=embed0)
                    return

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        await self.client.wait_until_ready()
        if not member.bot:
            async with self.client.db.execute("SELECT * FROM categories_channels WHERE guildID = ?", (member.guild.id,)) as cursor:
                guildSetUp = await cursor.fetchall()
            if len(guildSetUp) == 0:
                return
            async with self.client.db.execute("SELECT * FROM bannedCategories WHERE guildID = ?",
                                              (member.guild.id,)) as cursor:
                banned_categories = await cursor.fetchall()
            bannedCategories = []
            for bCategory in banned_categories:
                bannedCategories.append(bCategory[1])
    
            async with self.client.db.execute("SELECT categoryID FROM active WHERE guildID = ?", (member.guild.id,)) as cursor:
                activeCategory = await cursor.fetchone()
            arenaCategoryID = activeCategory[0]
            if arenaCategoryID != 0:
                if before.channel != None and after.channel != None:

                    if after.channel.category.id != arenaCategoryID:

                        voice_channel = self.client.get_channel(after.channel.id)
                        if voice_channel == None:
                            print("it is none")
                            return

                        move_blacklist = []
                        channels_blacklist = []
                        members_blacklist = []

                        async with self.client.db.execute(f"SELECT * FROM moveBlacklist WHERE guildID = ?",
                                                          (member.guild.id,)) as cursor:
                            listOfAllItems = await cursor.fetchall()

                        if len(listOfAllItems) > 0:
                            for i in listOfAllItems:
                                move_blacklist.append(int(i[0]))
                        async with self.client.db.execute(f"SELECT * FROM channelsBlacklist WHERE guildID = ?",
                                                          (member.guild.id,)) as cursor:
                            listOfAllItems = await cursor.fetchall()

                        if len(listOfAllItems) > 0:
                            for i in listOfAllItems:
                                channels_blacklist.append(int(i[0]))

                        async with self.client.db.execute(f"SELECT * FROM membersBlacklist WHERE guildID = ?",
                                                          (member.guild.id,)) as cursor:
                            listOfAllItems = await cursor.fetchall()

                        if len(listOfAllItems) > 0:
                            for i in listOfAllItems:
                                members_blacklist.append(int(i[0]))

                        if voice_channel.id in channels_blacklist or voice_channel.id in move_blacklist:
                            return
                        if member.id in members_blacklist:
                            return
                        if after.channel.members != None:
                            pass
                        all_members = voice_channel.members  # finds members connected to the channel
                        members = []

                        if len(all_members) > 0:
                            for m in all_members:
                                if m.bot == False:
                                    members.append(m)

                        if 2 > len(members) > 0:

                            if voice_channel.category == None:
                                return

                            elif voice_channel.category.id in bannedCategories:
                                return
                            else:

                                arena_cagetory = self.client.get_channel(arenaCategoryID)
                                await self.client.db.execute(
                                    f'INSERT INTO activeVoiceChannels VALUES (?, ?, ?)',
                                    (member.guild.id, voice_channel.id, voice_channel.category.id))
                                await self.client.db.commit()
                                await voice_channel.edit(position=0, category=arena_cagetory)



                elif before.channel == None:
                    if after.channel == None:
                        print("after.channel is none")
                        return
                    voice_channel = self.client.get_channel(after.channel.id)
                    if voice_channel == None:
                        print("it is none")
                        return

                    move_blacklist = []
                    channels_blacklist = []
                    members_blacklist = []
                    async with self.client.db.execute(f"SELECT * FROM moveBlacklist WHERE guildID = ?",
                                                      (member.guild.id,)) as cursor:
                        listOfAllItems = await cursor.fetchall()

                    if len(listOfAllItems) > 0:
                        for i in listOfAllItems:
                            move_blacklist.append(int(i[0]))
                    async with self.client.db.execute(f"SELECT * FROM channelsBlacklist WHERE guildID = ?",
                                                      (member.guild.id,)) as cursor:
                        listOfAllItems = await cursor.fetchall()

                    if len(listOfAllItems) > 0:
                        for i in listOfAllItems:
                            channels_blacklist.append(int(i[0]))

                    async with self.client.db.execute(f"SELECT * FROM membersBlacklist WHERE guildID = ?",
                                                      (member.guild.id,)) as cursor:
                        listOfAllItems = await cursor.fetchall()

                    if len(listOfAllItems) > 0:
                        for i in listOfAllItems:
                            members_blacklist.append(int(i[0]))

                    if voice_channel.id in channels_blacklist or voice_channel.id in move_blacklist:
                        return
                    if member.id in members_blacklist:
                        return
                    if after.channel.members != None:
                        pass
                    all_members = voice_channel.members  # finds members connected to the channel
                    members = []

                    if len(all_members) > 0:
                        for m in all_members:
                            if m.bot == False:
                                members.append(m)

                    if len(members) > 0:

                        if voice_channel.category == None:
                            return

                        elif voice_channel.category.id in bannedCategories:
                            return
                        else:

                            arena_cagetory = self.client.get_channel(arenaCategoryID)
                            await self.client.db.execute(
                                f'INSERT INTO activeVoiceChannels VALUES (?, ?, ?)',
                                (member.guild.id, voice_channel.id, voice_channel.category.id))
                            await self.client.db.commit()
                            await voice_channel.edit(position=0, category=arena_cagetory)




                elif after.channel == None:
                    if before.channel == None:
                        print("before.channel is none")
                        return
                    voice_channel = self.client.get_channel(before.channel.id)
                    if voice_channel == None:
                        print("voice channel in after_voice_channel is none")
                        return

                    activeChannelsList = []

                    async with self.client.db.execute(f"SELECT * FROM activeVoiceChannels WHERE guildID = ?", (member.guild.id,)) as cursor:
                        listOfAllItems = await cursor.fetchall()

                    if len(listOfAllItems) > 0:
                        for activeChannel in listOfAllItems:
                            activeChannelsList.append(int(activeChannel[0]))

                        if voice_channel.id in activeChannelsList:

                            async with self.client.db.execute(f"SELECT categoryID FROM activeVoiceChannels WHERE channelID = ? AND guildID = ?",
                                                              (voice_channel.id, member.guild.id)) as cursor:
                                category_ID = await cursor.fetchone()


                            if category_ID is None:

                                return
                            else:

                                category = self.client.get_channel(category_ID[0])

                                await self.client.db.execute(f'DELETE FROM activeVoiceChannels WHERE channelID = ? AND guildID = ?',
                                                             (voice_channel.id, member.guild.id))

                                await self.client.db.commit()

                                async with self.client.db.execute(
                                        f"SELECT * FROM categories_channels WHERE categoryID = ? AND guildID = ?",
                                        (category.id, member.guild.id)) as cursor:
                                    listOfAllItems = await cursor.fetchall()
                                    # db.child("categories&channels").child(
                                # category.id).get().val()
                                positionsss = []

                                if len(listOfAllItems) > 0:
                                    # print(categorieschannels)
                                    for i in listOfAllItems:
                                        positionsss.append((int(i[1]), int(i[2])))

                                    sorted_positions = sorted(positionsss, key=lambda t: t[1], reverse=False)

                                    for key, value in sorted_positions:
                                        channel2 = self.client.get_channel(int(key))

                                        if channel2 == None:
                                            continue
                                        else:

                                            if str(channel2.type) == "category":
                                                continue
                                            else:

                                                if voice_channel.id == int(key):
                                                    await voice_channel.edit(position=int(value), category=category)
                                                elif not channel2.id in activeChannelsList:
                                                    await channel2.edit(position=int(value), category=category)





    @commands.command(aliases=["active-channels"])
    #@commands.has_any_role(owner, head_staff)
    async def active_channels(self, ctx):
        channels = ""

        async with self.client.db.execute(f"SELECT * FROM activeTextChannels WHERE guildID = ?", (ctx.guild.id,)) as cursor:
            listOfAllItems = await cursor.fetchall()


        # activeChannels = db.child("is_active").get().val()
        activeChannelsList = []
        if len(listOfAllItems) > 0:
            for activeChannel in listOfAllItems:
                activeChannelsList.append(activeChannel[1])
            for channelID in activeChannelsList:
                channel = self.client.get_channel(int(channelID))
                if channel is not None:
                    channels += channel.name + " | " + str(channel.type) + "\n"

            embed = Embed(title="Active channels", description=channels, color=random_color())
            await ctx.send(embed=embed)
            return
        else:
            embed0 = Embed(description=f"No Active Channels in\n**{ctx.guild.name}**", color=random_color())
            await ctx.send(embed=embed0)
            return

    @commands.command()
    #@commands.has_any_role(owner, head_staff)
    async def blacklist(self, ctx):
        move_blacklists = []
        channels_blacklists = []
        members_blacklists = []

        async with self.client.db.execute(f"SELECT * FROM moveBlacklist WHERE guildID = ?", (ctx.guild.id,)) as cursor:
            listOfAllItems = await cursor.fetchall()



        if len(listOfAllItems) > 0:
            for i in listOfAllItems:
                move_blacklists.append(int(i[0]))

        async with self.client.db.execute(f"SELECT * FROM channelsBlacklist WHERE guildID = ?", (ctx.guild.id,)) as cursor:
            listOfAllItems = await cursor.fetchall()


        if len(listOfAllItems) > 0:
            for i in listOfAllItems:
                channels_blacklists.append(int(i[0]))

        async with self.client.db.execute(f"SELECT * FROM membersBlacklist WHERE guildID = ?", (ctx.guild.id,)) as cursor:
            listOfAllItems = await cursor.fetchall()


        if len(listOfAllItems) > 0:
            for i in listOfAllItems:
                members_blacklists.append(int(i[0]))

        members_blacklist = ""
        if len(members_blacklists) == 0:
            members_blacklist = "None"
        else:
            for key in members_blacklists:
                members_blacklist += f"<@{key}>\n"

        channels_blacklist = ""
        if len(channels_blacklists) == 0:
            channels_blacklist = "None"
        else:
            for key in channels_blacklists:
                channels_blacklist += f"<#{key}>\n"

        move_text_blacklist = ""
        move_voice_blacklist = ""
        if len(move_blacklists) == 0:
            move_text_blacklist = "None"
            move_voice_blacklist = "None"
        else:
            for key in move_blacklists:
                channel = self.client.get_channel(int(key))
                if channel == None:
                    await self.client.db.execute(
                        f'DELETE FROM moveBlacklist WHERE channelID = {key}')
                    await self.client.db.commit()
                elif str(channel.type) == "voice":
                    move_voice_blacklist += f"{channel.name}\n"
                else:
                    move_text_blacklist += f"<#{key}>\n"

        embed = Embed(title="Active Blacklists", color=random_color())
        embed.add_field(name="Members", value=members_blacklist or "None", inline=True)
        embed.add_field(name="Channels", value=channels_blacklist or "None", inline=True)
        embed.add_field(name="Moving Text Channels", value=move_text_blacklist or "None", inline=False)
        embed.add_field(name="Moving Voice Channels", value=move_voice_blacklist or "None", inline=True)
        await ctx.send(embed=embed)
        return

    '''@commands.command()
    #@commands.has_any_role(owner, head_staff)
    async def position(self, ctx, type=None, channel=None):
        if type == None:
            embed0 = Embed(title="How to use this command?",
                           description=f"`{ctx.message.content} [db] <#channel>`", color=random_color())
            await ctx.send(embed=embed0)
            return
        else:
            if type == "db":
                if channel == None:
                    embed0 = Embed(title="How to use this command?",
                                   description=f"`{ctx.message.content} <#channel>`", color=random_color())
                    await ctx.send(embed=embed0)
                    return
                else:
                    channel_ID = ""
                    for i in channel:
                        if i.isdigit():
                            channel_ID += i
                    channel2 = self.client.get_channel(int(channel_ID))
                    if channel2 == None:
                        embed0 = Embed(title="No channel was found with this ID", color=random_color())
                        await ctx.send(embed=embed0)
                        return

                    async with self.client.db.execute(
                            f"""SELECT * FROM categories_channels WHERE channelID = {channel2.id}""") as cursor:
                        listOfAllItems = await cursor.fetchall()
                    positionsss = []

                    if len(listOfAllItems) == 0:
                        embed0 = Embed(title="This channel is not in my database", color=random_color())
                        await ctx.send(embed=embed0)
                        return
                    else:
                        for i in listOfAllItems:
                            positionsss.append((int(i[1]), int(i[2])))
                        post = 0
                        for key, value in positionsss:
                            if int(key) == channel2.id:
                                post = int(value)
                        embed = Embed(title=f"{channel2.category.name}", description=f"{channel2.mention} : {post}",
                                      color=random_color())
                        await ctx.send(embed=embed)
                        return
            else:
                channel_ID = ""
                for i in type:
                    if i.isdigit():
                        channel_ID += i

                channel2 = self.client.get_channel(int(channel_ID))
                if channel2 == None:
                    embed0 = Embed(title="No channel was found with this ID", color=random_color())
                    await ctx.send(embed=embed0)
                    return
                else:
                    embed = Embed(title=f"{channel2.category.name}",
                                  description=f"{channel2.mention} : {channel2.position}",
                                  color=random_color())
                    await ctx.send(embed=embed)
                    return

    @commands.command()
    #@commands.has_any_role(owner, head_staff)
    async def positions(self, ctx, type=None, categoryID=None):
        if type == None:
            embed1 = Embed(title="Collecting Channels & Categories", color=random_color())
            e = await ctx.send(embed=embed1)
            await asyncio.sleep(5)
            categories = ""
            embed = Embed(title="Finished resetting all categories", color=random_color())

            for category in ctx.guild.categories:

                if category.id in bannedCategories:
                    continue
                else:
                    m = ""
                    categories += f"{category.name}\n"
                    for channel in category.text_channels:
                        m += f"{channel.name} - #{channel.position}\n"
                        embed2 = Embed(title=f"Resetting {category.name}", description=f"{m}", color=random_color())
                        await e.edit(embed=embed2)
                    if m != "":
                        embed.add_field(name=category.name, value=m, inline=True)

            await ctx.send(embed=embed)
            await e.delete()
            return
        else:
            if type != "db":
                embed0 = Embed(title="How to use this command?",
                               description=f"`{pre}positions [db]`", color=random_color())
                await ctx.send(embed=embed0)
                return
            embed1 = Embed(title="Collecting Channels & Categories", color=random_color())
            e = await ctx.send(embed=embed1)
            await asyncio.sleep(5)
            categories = ""
            embed = Embed(title="Finished setting all categories", color=random_color())

            for category in ctx.guild.categories:

                if category.id in bannedCategories:
                    continue
                else:
                    m = ""

                    categories += f"{category.name}\n"
                    for channel in category.channels:

                        post = "**Not recorded**"
                        async with self.client.db.execute(
                                f"""SELECT * FROM categories_channels WHERE categoryID = {category.id}""") as cursor:
                            listOfAllItems = await cursor.fetchall()
                        positionsss = []

                        for i in listOfAllItems:
                            positionsss.append((int(i[1]), int(i[2])))
                        # posts = db.child("categories&channels").child(category.id).get().val()
                        if len(positionsss) > 0:
                            for key, value in positionsss:
                                if int(key) == channel.id:
                                    post = value

                        m += f"{channel.name} - #{post}\n"

                        embed2 = Embed(title=f"{category.name}", description=f"{m}", color=random_color())
                        await e.edit(embed=embed2)
                    if m != "":
                        embed.add_field(name=category.name, value=m, inline=True)

            await ctx.send(embed=embed)
            await e.delete()
            return'''

    @commands.command(aliases=["remove-blacklist"])
    #@commands.has_any_role(owner, head_staff)
    async def remove_blacklist(self, ctx, first_thing=None, second_thing=None):
        if first_thing == None:
            embed = Embed(title="How to use this command?", color=random_color())
            embed.add_field(name="__Members__", value=f"`{ctx.message.content} members <@member>`", inline=False)
            embed.add_field(name="__Channels__", value=f"`{ctx.message.content} channels <#channel>`", inline=False)
            embed.add_field(name="__Move__", value=f"`{ctx.message.content} move <#channel>`", inline=False)
            embed.add_field(name="__Note__", value="You can either mention the member/channel or use their ID",
                            inline=False)
            await ctx.send(embed=embed)
            return
        else:
            if first_thing == "members":
                if second_thing == None:
                    embed = Embed(title="How to use this command?", color=random_color())
                    embed.add_field(name="__Member__", value=f"`{ctx.message.content} member <@member>`",
                                    inline=False)
                    embed.add_field(name="__Note__", value="You can either mention the member/channel or use their ID",
                                    inline=False)
                    await ctx.send(embed=embed)
                    return
                else:

                    member_ID = ""
                    for m in second_thing:
                        if m.isdigit():
                            member_ID += m
                    member = ctx.guild.get_member(int(member_ID))
                    if member == None:
                        embed0 = Embed(description=f"No member was found with this ID, `{member_ID}`",
                                       color=random_color())
                        await ctx.send(embed=embed0)
                        return
                    else:

                        # members_blacklist = db.child("active_blacklist").child(ctx.guild.id).child(
                        #   "members").get().val()
                        members_blacklist = []

                        async with self.client.db.execute(f"SELECT * FROM membersBlacklist WHERE guildID = ? AND memberID = ?",
                                                          (ctx.guild.id, member.id)) as cursor:
                            memberBlackListed = await cursor.fetchone()





                        if memberBlackListed is not None:

                            await self.client.db.execute(
                                f'DELETE FROM membersBlacklist WHERE memberID = ? AND guildID = ?',
                                (member.id, ctx.guild.id))
                            await self.client.db.commit()
                            embed = Embed(description=f"I have removed {member.mention} from the blacklist",
                                          color=random_color())
                            await ctx.send(embed=embed)
                            return

                        else:
                            embed0 = Embed(description=f"This member is not in the blacklist", color=random_color())
                            await ctx.send(embed=embed0)
                            return
            elif first_thing == "channels":
                if second_thing == None:
                    embed = Embed(title="How to use this command?", color=random_color())
                    embed.add_field(name="__Channels__", value=f"`{ctx.message.content} channels <#channel>`",
                                    inline=False)
                    embed.add_field(name="__Note__", value="You can either mention the member/channel or use their ID",
                                    inline=False)
                    await ctx.send(embed=embed)
                    return
                else:
                    channel_ID = ""
                    is_in = "False"
                    for m in second_thing:
                        if m.isdigit():
                            channel_ID += m
                    channel = self.client.get_channel(int(channel_ID))
                    if channel == None:
                        embed0 = Embed(description=f"No channel was found with this ID, `{channel_ID}`",
                                       color=random_color())
                        await ctx.send(embed=embed0)
                        return
                    else:
                        channels_blacklist = []

                        async with self.client.db.execute(f"SELECT * FROM channelsBlacklist WHERE channelID = ? AND guildID = ?",
                                                          (channel.id, ctx.guild.id)) as cursor:
                            channelBlackisted = await cursor.fetchone()


                        if channelBlackisted is not None:
                            await self.client.db.execute(
                                f'DELETE FROM channelsBlacklist WHERE channelID = ? AND guildID = ?', (channel.id, ctx.guild.id))
                            await self.client.db.commit()
                            embed = Embed(description=f"I have removed {channel.mention} from the blacklist",
                                          color=random_color())
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed0 = Embed(description=f"This channel is not in the blacklist", color=random_color())
                            await ctx.send(embed=embed0)
                            return
            elif first_thing == "move":
                if second_thing == None:
                    embed = Embed(title="How to use this command?", color=random_color())
                    embed.add_field(name="__Move__", value=f"`{ctx.message.content} move <#channel>`", inline=False)
                    embed.add_field(name="__Note__", value="You can either mention the member/channel or use their ID",
                                    inline=False)
                    await ctx.send(embed=embed)
                    return
                else:
                    channel_ID = ""
                    is_in = "False"
                    for m in second_thing:
                        if m.isdigit():
                            channel_ID += m
                    channel = self.client.get_channel(int(channel_ID))
                    if channel == None:
                        embed0 = Embed(description=f"No channel was found with this ID, `{channel_ID}`",
                                       color=random_color())
                        await ctx.send(embed=embed0)
                        return
                    else:
                        channels_blacklist = []
                        async with self.client.db.execute(f"SELECT * FROM moveBlacklist WHERE channelID = ? AND guildID = ?",
                                                          (channel.id, ctx.guild.id)) as cursor:
                            moveBlacklisted = await cursor.fetchone()


                        if moveBlacklisted is not None:
                            await self.client.db.execute(
                                f'DELETE FROM moveBlacklist WHERE channelID = {channel.id}')
                            await self.client.db.commit()
                            embed = Embed(description=f"I have removed {channel.mention} from the blacklist",
                                          color=random_color())
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed0 = Embed(description=f"This channel is not in the blacklist", color=random_color())
                            await ctx.send(embed=embed0)
                            return

    @commands.command(aliases=["reset-positions"])
    #@commands.has_any_role(owner, head_staff)
    async def reset_positions(self, ctx):

        embed1 = Embed(title="Collecting Channels & Categories", color=random_color())
        e = await ctx.send(embed=embed1)
        await asyncio.sleep(5)
        categories = ""
        embed = Embed(title="Finished resetting all categories", color=random_color())
        n = 100
        categories_channels = {}
        cancelled_resetting = None
        cancelled_resetting1 = None
        async with self.client.db.execute("SELECT * FROM bannedCategories WHERE guildID = ?",
                                          (ctx.guild.id,)) as cursor:
            banned_categories = await cursor.fetchall()
        bannedCategories = []
        for bCategory in banned_categories:
            bannedCategories.append(bCategory[1])
        for category in ctx.guild.categories:

            if category.id in bannedCategories:
                continue
            else:
                m = ""

                categories += f"{category.name}\n"
                x = {}
                if cancelled_resetting1 == None:
                    for channel in category.channels:
                        if channel.type == "category":
                            continue
                        else:

                            if cancelled_resetting == None:
                                y = {channel.id: n}
                                x.update(y)
                                n += 1

                                m += f"{channel.name} - {channel.type} - #{n}\n"

                                if len(m) < 2000:
                                    embed2 = Embed(title=f"Resetting {category.name}", description=f"{m}",
                                                   color=random_color())
                                    await e.edit(embed=embed2)
                                else:
                                    m = "Text exceeded the **2024** characters"
                                    embed2 = Embed(title=f"Resetting {category.name}", description=f"{m}",
                                                   color=random_color())
                                    await e.edit(embed=embed2)
                            else:
                                break
                else:
                    break

                z = {category.id: x}

                categories_channels.update(z)

                if cancelled_resetting1 == None:
                    if m != "":
                        if len(m) < 1024:
                            embed.add_field(name=category.name, value=m, inline=True)
                        else:
                            m = "Text exceeded the **1024** characters"
                            embed.add_field(name=category.name, value=m, inline=True)
                    n += 100
        if cancelled_resetting == None or cancelled_resetting1 == None:
            q = await ctx.send(embed=embed)
            await e.delete()
            embed3 = Embed(title="Do you want to save these new positions?",
                           color=random_color())
            embed3.add_field(name="Yes",
                             value=f"React with {approve}", inline=True)
            embed3.add_field(name="No",
                             value=f"React with {deny}", inline=True)
            a = await ctx.send(ctx.author.mention, embed=embed3)
            await a.add_reaction(approve)
            await a.add_reaction(deny)

            def check(reaction, user):
                return user == ctx.author and (str(reaction) == approve or str(reaction) == deny)

            flag = True
            choice = ""
            while flag:
                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=300, check=check)
                except asyncio.TimeoutError:
                    embed0 = Embed(title="Time out",
                                   color=random_color())
                    await ctx.send(embed=embed0)
                    return
                else:
                    if str(reaction) == approve:
                        choice = "yes"
                        await a.delete()
                        flag = False
                    elif str(reaction) == deny:
                        choice = "no"
                        await a.delete()
                        flag = False
                    else:
                        continue
            if choice == "yes":
                await self.client.db.execute(f"DELETE FROM categories_channels WHERE guildID = ?", (ctx.guild.id,))

                # db.child("categories&channels").remove()
                await q.delete()
                embed5 = Embed(title="Saving the new positions",
                               description="Please wait...", color=random_color())
                f = await ctx.send(embed=embed5)
                await asyncio.sleep(5)

                for category in categories_channels.items():
                    new_dict = dict(category[1])
                    for channel, number in new_dict.items():
                        cate = self.client.get_channel(int(category[0]))
                        chan = self.client.get_channel(int(channel))
                        await chan.edit(position=number, category=cate)
                        # db.child("categories&channels").child(category[0]).update({channel: number})
                        # db.child("channel_positions").child(channel).update(
                        #           {"position": number, "category": category[0]})
                        await self.client.db.execute(
                            f'INSERT INTO categories_channels VALUES (?, ?, ?, ?)',
                            (ctx.guild.id, category[0], channel, number))
                        await self.client.db.commit()
                        await asyncio.sleep(2)

                embed4 = Embed(title="New positions have been saved", color=random_color())
                await f.edit(embed=embed4)
                return
            elif choice == "no":
                embed4 = Embed(title="New positions was not saved", color=random_color())
                await ctx.send(embed=embed4)
                return
        else:
            await e.delete()
            embed0 = Embed(title="Resetting has been cancelled", color=random_color())
            await ctx.send(embed=embed0)
            # db.child("cancel_resetting").child(ctx.guild.id).remove()
            return

    @commands.command()
    #@commands.has_any_role(owner, head_staff)
    async def active(self, ctx, first_thing=None, second_thing=None, *, third_thing=None):
        if first_thing == None:
            random_category = random.choice(ctx.guild.categories)
            embed = Embed(title="How to use this command?", color=random_color())
            embed.add_field(name="__Category__ (required)",
                            value=f"{usage}`{pre}active category <categoryID>`\n{example}{pre}active category {random_category.id}\n{note}To set where the active channels will be moved to",
                            inline=False)
            embed.add_field(name="__Channel__",
                            value=f"{usage}`{pre}active channel <channelID>`\nTo set up where tp mention the subscribed members when a channel becomes active",
                            inline=False)
            embed.add_field(name="__Timer__ ",
                            value=f"{usage}`{pre}active timer <time>`\n{example}{pre}active timer 3m\n{note}\n`s` -> seconds\n`m` -> minutes\n`h` -> hours\n`d` -> days",
                            inline=False)
            embed.add_field(name="__Messages__",
                            value=f"{usage}`{pre}active messages <time>`\n{example}{pre}active messages 5",
                            inline=False)
            embed.add_field(name="__Remove__",
                            value=f"{usage}`{pre}active remove <time>`\n{example}{pre}active remove 3m\n{note}\n`s` -> seconds\n`m` -> minutes\n`h` -> hours\n`d` -> days",
                            inline=False)

            embed.add_field(name="__Blacklist__", value=f"react with {forward} to see more details", inline=False)
            embed.set_footer(text=f"React with {cancel_emoji} to stop")

            e = await ctx.send(embed=embed)
            await e.add_reaction(backward)
            await e.add_reaction(forward)
            await e.add_reaction(cancel_emoji)

            embed1 = Embed(title="Blacklist",
                           description="Use this command to add blacklists whether members or channels",
                           color=random_color())
            embed1.add_field(name="__Members__",
                             value=f"{usage}`{pre}active blacklist members <@member>`\n{example}{pre}active blacklist members {ctx.author.mention}",
                             inline=False)
            embed1.add_field(name="__Channels__",
                             value=f"{usage}`{pre}active blacklist channels <#channel>`\n{example}{pre}active blacklist channels {ctx.channel.mention}",
                             inline=False)
            embed1.add_field(name="__Move__",
                             value=f"{usage}`{pre}active blacklist move <#channel>`\n{example}{pre}active blacklist move {ctx.channel.mention}",
                             inline=False)
            embed1.add_field(name="__Note__", value="You can either mention the member/channel or use their ID instead",
                             inline=False)
            embed1.set_footer(text=f"React with {cancel_emoji} to stop")
            embed_dict = {1: embed, 2: embed1}
            flag = True
            pn = 1

            def check(reaction, user):
                return user == ctx.author and (
                            str(reaction) == forward or str(reaction) == backward or str(reaction) == cancel_emoji)

            while flag:
                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=300, check=check)
                except asyncio.TimeoutError:
                    embed0 = Embed(description="Time out", color=random_color())
                    await ctx.send(embed=embed0)
                    await e.clear_reactions()
                    return
                else:
                    if str(reaction) == forward:
                        a = embed_dict.get(pn + 1)
                        await e.remove_reaction(reaction, ctx.author)
                        if a:
                            pn += 1
                            await e.edit(embed=a)

                    elif str(reaction) == backward:

                        a = embed_dict.get(pn - 1)
                        await e.remove_reaction(reaction, ctx.author)
                        if a:
                            pn -= 1
                            await e.edit(embed=a)

                    elif str(reaction) == cancel_emoji:
                        await e.clear_reactions()
                        return

        else:
            if second_thing == None:
                random_category = random.choice(ctx.guild.categories)
                embed = Embed(title="How to use this command?", color=random_color())
                embed.add_field(name="__Category__",
                                value=f"{usage}`{pre}active category <categoryID>`\n{example}{pre}active category {random_category.id}\n{note}To set where the active channels will be moved to",
                                inline=False)
                embed.add_field(name="__Messages__",
                                value=f"{usage}`{pre}active messages <time>`\n{example}{pre}active messages 5",
                                inline=False)
                embed.add_field(name="__Remove__",
                                value=f"{usage}`{pre}active remove <time>`\n{example}{pre}active remove 3m\n{note}\n`s` -> seconds\n`m` -> minutes\n`h` -> hours\n`d` -> days",
                                inline=False)
                embed.add_field(name="__Blacklist__", value=f"react with {forward} to see more details", inline=False)
                embed.set_footer(text=f"React with {cancel_emoji} to stop")

                e = await ctx.send(embed=embed)
                await e.add_reaction(backward)
                await e.add_reaction(forward)
                await e.add_reaction(cancel_emoji)

                embed1 = Embed(title="Blacklist",
                               description="Use this command to add blacklists whether members or channels",
                               color=random_color())
                embed1.add_field(name="__Members__",
                                 value=f"{usage}`{pre}active blacklist members <@member>`\n{example}{pre}active blacklist members {ctx.author.mention}",
                                 inline=False)
                embed1.add_field(name="__Channels__",
                                 value=f"{usage}`{pre}active blacklist channels <#channel>`\n{example}{pre}active blacklist channels {ctx.channel.mention}",
                                 inline=False)
                embed1.add_field(name="__Move__",
                                 value=f"{usage}`{pre}active blacklist move <#channel>`\n{example}{pre}active blacklist move {ctx.channel.mention}",
                                 inline=False)

                embed1.add_field(name="__Note__",
                                 value="You can either mention the member/channel or use their ID instead",
                                 inline=False)
                embed1.set_footer(text=f"React with {cancel_emoji} to stop")
                embed_dict = {1: embed, 2: embed1}
                flag = True
                pn = 1

                def check(reaction, user):
                    return user == ctx.author and (
                            str(reaction) == forward or str(reaction) == backward or str(reaction) == cancel_emoji)

                while flag:
                    try:
                        reaction, user = await self.client.wait_for("reaction_add", timeout=300, check=check)
                    except asyncio.TimeoutError:
                        embed0 = Embed(description="Time out", color=random_color())
                        await ctx.send(embed=embed0)
                        await e.clear_reactions()
                        return
                    else:
                        if str(reaction) == forward:
                            a = embed_dict.get(pn + 1)
                            await e.remove_reaction(reaction, ctx.author)
                            if a:
                                pn += 1
                                await e.edit(embed=a)

                        elif str(reaction) == backward:

                            a = embed_dict.get(pn - 1)
                            await e.remove_reaction(reaction, ctx.author)
                            if a:
                                pn -= 1
                                await e.edit(embed=a)
                        elif str(reaction) == cancel_emoji:
                            embed0 = Embed(description="Cancelled", color=random_color())
                            await ctx.send(embed=embed0)
                            await e.clear_reactions()
                            return

            else:
                if first_thing == "remove":

                    # timer = db.child("remove_active").child(ctx.guild.id).get().val()
                    times = ""
                    if third_thing != None:
                        times = second_thing + third_thing
                    else:
                        times = second_thing
                    if times.endswith(("d", "h", "m", "s")):
                        time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
                        total_time = 0
                        tim = times.split()
                        ti = [int(''.join(i for i in t if i.isdigit())) for t in tim]
                        tl = [(''.join(i for i in t if i.isdigit() == False)) for t in tim]
                        for t in range(0, len(tl)):
                            total_time += ti[t] * int(time_convert[tl[t]])
                        if total_time < 900:
                            embed0 = Embed(description="Minimum is **15 minutes**")
                            await ctx.send(ctx.author.mention, embed=embed0)
                            return
                        tomorrow = datetime.utcnow() + timedelta(seconds=total_time)
                        future_day = tomorrow.strftime("%d")
                        future_hour = tomorrow.strftime("%H")
                        future_minute = tomorrow.strftime("%M")
                        future_year = tomorrow.strftime("%Y")
                        future_month = tomorrow.strftime("%m")
                        future_second = tomorrow.strftime("%S")
                        today = datetime.utcnow()
                        today_second = today.strftime("%S")
                        today_year = today.strftime("%Y")
                        today_month = today.strftime("%m")
                        today_day = today.strftime("%d")
                        today_hour = today.strftime("%H")
                        today_minute = today.strftime("%M")
                        a = datetime(int(future_year), int(future_month), int(future_day), int(future_hour),
                                     int(future_minute), int(future_second))
                        b = datetime(int(today_year), int(today_month), int(today_day), int(today_hour),
                                     int(today_minute), int(today_second))
                        c = a - b
                        d = str(c).split()
                        expire_in = ""
                        try:
                            v = str(d[2]).split(":")
                        except Exception:
                            v = str(d[0]).split(":")

                            if int(v[0]) == 0 and int(v[1]) == 00 and int(v[2]) <= 10:
                                expire_in = "`10 seconds`"
                                pass

                            else:

                                if int(v[0]) == 0:
                                    expire_in = f"`{v[1]} minutes`"
                                    pass
                                if int(v[0]) != 0 and int(v[1]) > 0:
                                    expire_in = f"`{v[0]} hours {v[1]} minutes`"
                                    pass
                                if int(v[0]) != 0 and int(v[1]) == 0:
                                    expire_in = f"`{v[0]} hours`"
                                    pass


                        else:
                            if int(d[0]) == 0:
                                if int(v[0]) == 0:
                                    expire_in = f"`{v[1]} minutes`"
                                    pass
                                elif int(v[0]) != 0 and int(v[1]) != 0:
                                    expire_in = f"`{v[0]} hours {v[1]} minutes`"
                                    pass
                                elif int(v[0]) != 0 and int(v[1]) == 0:
                                    expire_in = f"`{v[0]} hours`"
                                    pass
                            else:
                                if int(v[0]) == 0 and int(v[1]) != 0:
                                    expire_in = f"`{d[0]} days, {v[1]} minutes`"
                                    pass
                                elif int(v[0]) == 0 and int(v[0]) == 0:
                                    expire_in = f"`{d[0]} days`"
                                elif int(v[0]) != 0 and int(v[1]) != 0:
                                    expire_in = f"`{d[0]} days, {v[0]} hours {v[1]} minutes`"
                                    pass
                                elif int(v[0]) != 0 and int(v[1]) == 0:
                                    expire_in = f"`{d[0]} days, {v[0]} hours`"
                                    pass
                                else:
                                    expire_in = f"`{d[0]} days`"
                                    pass
                        await self.client.db.execute(
                            'UPDATE active SET remove = ? WHERE guildID = ?', (total_time, ctx.guild.id))
                        await self.client.db.commit()
                        # db.child("remove_active").child(ctx.guild.id).update({"timer": total_time})
                        embed = Embed(description=f"The channel will go back to normal every `{expire_in}`",
                                      color=random_color())
                        await ctx.send(embed=embed)
                        return

                    else:
                        embed = Embed(title="How to use this command?", color=random_color())
                        embed.add_field(name="__Remove__",
                                        value=f"{usage}`{pre} remove <time>`\n{example}{pre} remove 3m",
                                        inline=False)

                        embed.add_field(name="__Note__",
                                        value=f"`s` -> seconds\n`m` -> minutes\n`h` -> hours\n`d` -> days")
                        await ctx.send(embed=embed)
                        return

                elif first_thing == "category":
                    if second_thing.isdigit():
                        category = self.client.get_channel(int(second_thing))
                        if category is not None:
                            if str(category.type) == "category":
                                embed = Embed(description=f"All active channels will be moved to {category.name}",
                                              color=random_color())
                                await ctx.send(embed=embed)
                                await self.client.db.execute("UPDATE active SET categoryID = ? WHERE guildID = ?",
                                                             (category.id, ctx.guild.id))
                                await self.client.db.commit()
                                return
                            else:
                                embed0 = Embed(title="Please send a valid category ID",
                                               color=random_color())
                                await ctx.send(ctx.author.mention, embed=embed0)
                                return
                        else:
                            embed0 = Embed(description=f"No category was found with this ID `{second_thing}`",
                                           color=random_color())
                            await ctx.send(ctx.author.mention, embed=embed0)
                            return
                    else:
                        embed0 = Embed(title="Please provide a valid category ID",
                                       color=random_color())
                        await ctx.send(ctx.author.mention, embed=embed0)
                        return

                elif first_thing == "channel":
                    channelID = ""
                    for i in second_thing:
                        if i.isdigit():
                            channelID += i

                    channel = self.client.get_channel(int(channelID))
                    if channel is not None:
                        if str(channel.type) == "text":
                            embed = Embed(description=f"Set up {channel.mention} as active alerts channel",
                                          color=random_color())
                            await ctx.send(embed=embed)
                            await self.client.db.execute("UPDATE active SET channelID = ? WHERE guildID = ?",
                                                         (channel.id, ctx.guild.id))
                            await self.client.db.commit()
                            return
                        else:
                            embed0 = Embed(title="Please send a valid channel ID",
                                           color=random_color())
                            await ctx.send(ctx.author.mention, embed=embed0)
                            return
                    else:
                        embed0 = Embed(description=f"No channel was found with this ID `{second_thing}`",
                                       color=random_color())
                        await ctx.send(ctx.author.mention, embed=embed0)
                        return


                elif first_thing == "timer":

                    # timer = db.child("active").child(ctx.guild.id).get().val()
                    times = ""
                    if third_thing != None:
                        times = second_thing + third_thing
                    else:
                        times = second_thing
                    if times.endswith(("d", "h", "m", "s")):
                        time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
                        total_time = 0

                        tim = times.split()

                        ti = [int(''.join(i for i in t if i.isdigit())) for t in tim]

                        tl = [(''.join(i for i in t if i.isdigit() == False)) for t in tim]

                        for t in range(0, len(tl)):
                            total_time += ti[t] * int(time_convert[tl[t]])
                        if total_time < 300:
                            embed0 = Embed(description="Minimum is **5 minutes**")
                            await ctx.send(ctx.author.mention, embed=embed0)
                            return
                        tomorrow = datetime.utcnow() + timedelta(seconds=total_time)

                        future = tomorrow.strftime('%Y-%m-%d %H-%M-%S %p')
                        future_day = tomorrow.strftime("%d")
                        future_hour = tomorrow.strftime("%H")
                        future_minute = tomorrow.strftime("%M")
                        future_year = tomorrow.strftime("%Y")
                        future_month = tomorrow.strftime("%m")
                        future_second = tomorrow.strftime("%S")
                        today = datetime.utcnow()
                        today_second = today.strftime("%S")
                        today_year = today.strftime("%Y")
                        today_month = today.strftime("%m")
                        today_day = today.strftime("%d")
                        today_hour = today.strftime("%H")
                        today_minute = today.strftime("%M")
                        a = datetime(int(future_year), int(future_month), int(future_day), int(future_hour),
                                     int(future_minute), int(future_second))
                        b = datetime(int(today_year), int(today_month), int(today_day), int(today_hour),
                                     int(today_minute), int(today_second))
                        c = a - b
                        d = str(c).split()
                        expire_in = ""
                        try:
                            v = str(d[2]).split(":")
                        except Exception:
                            v = str(d[0]).split(":")

                            if int(v[0]) == 0 and int(v[1]) == 00 and int(v[2]) <= 10:
                                expire_in = "`10 seconds`"
                                pass

                            else:

                                if int(v[0]) == 0:
                                    expire_in = f"`{v[1]} minutes`"
                                    pass
                                if int(v[0]) != 0 and int(v[1]) > 0:
                                    expire_in = f"`{v[0]} hours {v[1]} minutes`"
                                    pass
                                if int(v[0]) != 0 and int(v[1]) == 0:
                                    expire_in = f"`{v[0]} hours`"
                                    pass


                        else:
                            if int(d[0]) == 0:
                                if int(v[0]) == 0:
                                    expire_in = f"`{v[1]} minutes`"
                                    pass
                                elif int(v[0]) != 0 and int(v[1]) != 0:
                                    expire_in = f"`{v[0]} hours {v[1]} minutes`"
                                    pass
                                elif int(v[0]) != 0 and int(v[1]) == 0:
                                    expire_in = f"`{v[0]} hours`"
                                    pass
                            else:
                                if int(v[0]) == 0 and int(v[1]) != 0:
                                    expire_in = f"`{d[0]} days, {v[1]} minutes`"
                                    pass
                                elif int(v[0]) == 0 and int(v[0]) == 0:
                                    expire_in = f"`{d[0]} days`"
                                elif int(v[0]) != 0 and int(v[1]) != 0:
                                    expire_in = f"`{d[0]} days, {v[0]} hours {v[1]} minutes`"
                                    pass
                                elif int(v[0]) != 0 and int(v[1]) == 0:
                                    expire_in = f"`{d[0]} days, {v[0]} hours`"
                                    pass
                                else:
                                    expire_in = f"`{d[0]} days`"
                                    pass
                        await self.client.db.execute(
                            'UPDATE active SET timer = ? WHERE guildID = ?', (total_time, ctx.guild.id))
                        await self.client.db.commit()
                        embed = Embed(description=f"I have set the difference between messages to be `{expire_in}`",
                                      color=random_color())
                        await ctx.send(embed=embed)
                        return

                    else:
                        embed = Embed(title="How to use this command?", color=random_color())
                        embed.add_field(name="__Timer__", value=f"{usage}`{pre} timer <time>`\n{example}{pre} timer 3m",
                                        inline=False)

                        embed.add_field(name="__Note__",
                                        value=f"`s` -> seconds\n`m` -> minutes\n`h` -> hours\n`d` -> days")
                        await ctx.send(embed=embed)
                        return

                elif first_thing == "messages":

                    # messages = db.child("active").child(ctx.guild.id).get().val()
                    if second_thing.isdigit():

                        await self.client.db.execute(
                            'UPDATE active SET messages = ? WHERE guildID = ?', (second_thing, ctx.guild.id))
                        await self.client.db.commit()
                        # db.child("active").child(ctx.guild.id).update({"messages": second_thing})
                        embed = Embed(description=f"I have set up the number of messages to `{second_thing}`",
                                      color=random_color())
                        await ctx.send(embed=embed)
                        return

                    else:
                        embed = Embed(title="How to use this command?", color=random_color())

                        embed.add_field(name="__Messages__",
                                        value=f"{usage}`{pre} messages <time>`\n{example}{pre} messages 5",
                                        inline=False)

                        await ctx.send(embed=embed)
                        return

                elif first_thing == "blacklist":
                    if second_thing == None:
                        embed1 = Embed(title="Blacklist",
                                       description="Use this command to add blacklists whether members or channels",
                                       color=random_color())
                        embed1.add_field(name="__Members__",
                                         value=f"{usage}`{pre}active blacklist members <@member>`\n{example}{pre}active blacklist members {ctx.author.mention}",
                                         inline=False)
                        embed1.add_field(name="__Channels__",
                                         value=f"{usage}`{pre}active blacklist channels <#channel>`\n{example}{pre}active blacklist channels {ctx.channel.mention}",
                                         inline=False)
                        embed1.add_field(name="__Move__",
                                         value=f"{usage}`{pre}active blacklist move <#channel>`\n{example}{pre}active blacklist move {ctx.channel.mention}",
                                         inline=False)

                        embed1.add_field(name="__Note__",
                                         value="You can either mention the member/channel or use their ID instead",
                                         inline=False)
                        await ctx.send(embed=embed1)
                        return
                    elif third_thing == None:
                        embed1 = Embed(title="Blacklist",
                                       description="Use this command to add blacklists whether members or channels",
                                       color=random_color())
                        embed1.add_field(name="__Members__",
                                         value=f"{usage}`{pre}active blacklist members <@member>`\n{example}{pre}active blacklist members {ctx.author.mention}",
                                         inline=False)
                        embed1.add_field(name="__Channels__",
                                         value=f"{usage}`{pre}active blacklist channels <#channel>`\n{example}{pre}active blacklist channels {ctx.channel.mention}",
                                         inline=False)
                        embed1.add_field(name="__Move__",
                                         value=f"{usage}`{pre}active blacklist move <#channel>`\n{example}{pre}active blacklist move {ctx.channel.mention}",
                                         inline=False)

                        embed1.add_field(name="__Note__",
                                         value="You can either mention the member/channel or use their ID instead",
                                         inline=False)
                        await ctx.send(embed=embed1)
                        return
                    else:
                        if second_thing == "members":
                            member_ID = ""
                            for m in third_thing:
                                if m.isdigit():
                                    member_ID += m

                            member = ctx.guild.get_member(int(member_ID))
                            if member == None:
                                await ctx.send(f"No member was found with this ID {member_ID}")
                                return
                            else:
                                async with self.client.db.execute(f"SELECT * FROM membersBlacklist WHERE memberID = ? AND guildID = ?",
                                                                  (member.id, ctx.guild.id)) as cursor:
                                    memberBlacklisted = await cursor.fetchone()

                                if memberBlacklisted is not None:

                                        embed0 = Embed(description=f"This member is already blacklisted",
                                                           color=random_color())
                                        await ctx.send(embed=embed0)
                                        return

                                await self.client.db.execute(
                                    'INSERT INTO membersBlacklist VALUES (?, ?)', (ctx.guild.id, member.id))

                                await self.client.db.commit()

                                # db.child("active_blacklist").child(ctx.guild.id).child("members").update({member.id: member.id})
                                embed = Embed(description=f"I have added {member.mention} to the members blacklist",
                                              color=random_color())
                                await ctx.send(embed=embed)
                                return
                        elif second_thing == "channels":
                            channel_ID = ""
                            for m in third_thing:
                                if m.isdigit():
                                    channel_ID += m

                            channel = self.client.get_channel(int(channel_ID))
                            if channel == None:
                                await ctx.send(f"No channel was found with this ID {channel_ID}")
                                return
                            else:
                                async with self.client.db.execute(f"SELECT * FROM channelsBlacklist WHERE channelID = ? AND guildID = ?",
                                                                  (channel.id, ctx.guild.id)) as cursor:
                                    channelBlacklisted = await cursor.fetchone()

                                if channelBlacklisted is not None:
                                    embed0 = Embed(description=f"This channel is already blacklisted",
                                                   color=random_color())
                                    await ctx.send(embed=embed0)
                                    return

                                await self.client.db.execute(
                                    'INSERT INTO channelsBlacklist VALUES (?, ?)', (ctx.guild.id, channel.id))

                                await self.client.db.commit()

                                # db.child("active_blacklist").child(ctx.guild.id).child("channels").update(
                                #   {channel.id: channel.id})
                                embed = Embed(description=f"I have added {channel.mention} to the channels blacklist",
                                              color=random_color())
                                await ctx.send(embed=embed)
                                return
                        elif second_thing == "move":
                            channel_ID = ""
                            for m in third_thing:
                                if m.isdigit():
                                    channel_ID += m

                            channel = self.client.get_channel(int(channel_ID))
                            if channel == None:
                                await ctx.send(f"No channel was found with this ID {channel_ID}")
                                return
                            else:
                                async with self.client.db.execute(f"SELECT * FROM moveBlacklist WHERE channelID = ? AND guildID = ?",
                                                                  (channel.id, ctx.guild.id)) as cursor:
                                    moveBlacklisted = await cursor.fetchone()

                                if moveBlacklisted is not None:
                                    embed0 = Embed(description=f"This channel is already blacklisted",
                                                   color=random_color())
                                    await ctx.send(embed=embed0)
                                    return

                                await self.client.db.execute(
                                    'INSERT INTO moveBlacklist VALUES (?, ?)', (ctx.guild.id, channel.id))

                                await self.client.db.commit()

                                # db.child("active_blacklist").child(ctx.guild.id).child("move").update(
                                #   {channel.id: channel.id})
                                embed = Embed(description=f"I have added {channel.mention} to the move blacklist",
                                              color=random_color())
                                await ctx.send(embed=embed)
                                return
                        elif second_thing == "category":
                            channel_ID = ""
                            for m in third_thing:
                                if m.isdigit():
                                    channel_ID += m

                            category = self.client.get_channel(int(channel_ID))
                            if category == None:
                                await ctx.send(f"No category was found with this ID {channel_ID}")
                                return
                            else:
                                if str(category.type) != "category":
                                    embed0 = Embed(title=f"Please use a valid category ID", color=random_color())
                                    await ctx.send(embed=embed0)
                                    return

                                async with self.client.db.execute(
                                        f"SELECT * FROM bannedCategories WHERE categoryID = ? AND guildID = ?",
                                        (category.id, ctx.guild.id)) as cursor:
                                    moveBlacklisted = await cursor.fetchone()

                                if moveBlacklisted is not None:
                                    embed0 = Embed(description=f"This category is already blacklisted",
                                                   color=random_color())
                                    await ctx.send(embed=embed0)
                                    return

                                await self.client.db.execute(
                                    'INSERT INTO bannedCategories VALUES (?, ?)', (ctx.guild.id, category.id))

                                await self.client.db.commit()

                                # db.child("active_blacklist").child(ctx.guild.id).child("move").update(
                                #   {channel.id: channel.id})
                                embed = Embed(description=f"I have added {category.name} to the category blacklist",
                                              color=random_color())
                                await ctx.send(embed=embed)
                                return



    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:

            channel = message.channel

            if message.guild == None:
                print("message.guild")
                return
            if str(type(channel)) == "<class 'discord.threads.Thread'>":
                print("Thread")
                return

            if channel.category == None:
                print("No category")
                return
            async with self.client.db.execute("SELECT * FROM categories_channels WHERE guildID = ?", (message.guild.id,)) as cursor:
                guildSetUp = await cursor.fetchall()

            if len(guildSetUp) == 0:
                return
            async with self.client.db.execute(f"SELECT * FROM active WHERE guildID = ?", (message.guild.id,)) as cursor:
                listOfAllItems = await cursor.fetchone()


            # times = db.child("active").child(message.guild.id).get().val()
            if len(listOfAllItems) == 0:
                print("No active set up")
                return
            else:

                arena_cagetory_ID = int(listOfAllItems[1])

                timer = int(listOfAllItems[4])

                number = int(listOfAllItems[3])

                active_alerts_ID = int(listOfAllItems[2])

                if arena_cagetory_ID == 0:
                    return
                move_blacklist = []
                channels_blacklist = []
                members_blacklist = []
                async with self.client.db.execute(f"SELECT * FROM moveBlacklist WHERE guildID = ?",
                                                  (message.guild.id,)) as cursor:
                    listOfAllItems = await cursor.fetchall()

                if len(listOfAllItems) > 0:
                    for i in listOfAllItems:
                        move_blacklist.append(int(i[0]))
                async with self.client.db.execute(f"SELECT * FROM channelsBlacklist WHERE guildID = ?",
                                                  (message.guild.id,)) as cursor:
                    listOfAllItems = await cursor.fetchall()

                if len(listOfAllItems) > 0:
                    for i in listOfAllItems:
                        channels_blacklist.append(int(i[0]))

                async with self.client.db.execute(f"SELECT * FROM membersBlacklist WHERE guildID = ?",
                                                  (message.guild.id,)) as cursor:
                    listOfAllItems = await cursor.fetchall()

                if len(listOfAllItems) > 0:
                    for i in listOfAllItems:
                        members_blacklist.append(int(i[0]))

                # members_blacklist = db.child("active_blacklist").child(message.guild.id).child("members").get().val()

                not_moving = []
                # move_blacklist = db.child("active_blacklist").child(message.guild.id).child("move").get().val()
                # is_active = db.child("is_active").child(channel.id).get().val()
                async with self.client.db.execute(f"SELECT * FROM activeTextChannels WHERE guildID = ? AND channelID = ?",
                                                  (message.guild.id, channel.id)) as cursor:
                    activeChannel = await cursor.fetchone()



                if activeChannel is not None:
                    return

                # channels_blacklist = db.child("active_blacklist").child(message.guild.id).child("channels").get().val()

                if message.channel.id in channels_blacklist:
                    return
                if message.author.id in members_blacklist:
                    return


                messages = await message.channel.history(limit=number).flatten()

                liste = []


                if len(messages) == number:

                    for messagee in messages:
                        if messagee.author.id in members_blacklist:

                            continue
                        else:
                            minutes = messagee.created_at.strftime('%M')
                            seconds = messagee.created_at.strftime('%S')
                            hours = messagee.created_at.strftime("%H")
                            days = messagee.created_at.strftime("%d")
                            month = messagee.created_at.strftime("%m")
                            year = messagee.created_at.strftime("%Y")
                            liste.append((year, month, days, hours, minutes, seconds))

                    if len(liste) == number:
                        flag = True
                        i = 0
                        new_liste = []
                        while flag:
                            try:
                                option1 = liste[i]
                                option2 = liste[i + 1]
                            except Exception:
                                flag = False
                            else:
                                a = datetime(int(option1[0]), int(option1[1]), int(option1[2]),
                                             int(option1[3]),
                                             int(option1[4]), int(option1[5]))
                                b = datetime(int(option2[0]), int(option2[1]), int(option2[2]),
                                             int(option2[3]),
                                             int(option2[4]), int(option2[5]))

                                c = a - b
                                new_liste.append(int(c.total_seconds()))
                                i += 1
                        results = []

                        for result in new_liste:
                            if result <= timer:
                                results.append("True")
                            else:
                                results.append("False")

                        if "False" in results:

                            return


                        else:

                            old_channel_name = channel.name
                            old_name = old_channel_name.split("-")
                            async with self.client.db.execute("SELECT * FROM bannedCategories WHERE guildID = ?",
                                                              (message.guild.id,)) as cursor:
                                banned_categories = await cursor.fetchall()
                            bannedCategories = []
                            for bCategory in banned_categories:
                                bannedCategories.append(bCategory[1])
                            if channel.category == None:

                                return

                            elif channel.category.id in bannedCategories:

                                await self.client.db.execute(
                                    f'INSERT INTO activeTextChannels VALUES (?, ?, ?)',
                                    (message.guild.id, channel.id, channel.category.id))
                                await self.client.db.commit()
                                # db.child("is_active").child(channel.id).update(
                                # {"position": channel.position, "category": channel.category.id})
                                pass
                            else:
                                await self.client.db.execute(
                                    f'INSERT INTO activeTextChannels VALUES (?, ?, ?)',
                                    (message.guild.id, channel.id, channel.category.id))
                                await self.client.db.commit()
                                # db.child("is_active").child(channel.id).update(
                                #   {"position": channel.position, "category": channel.category.id})
                                arena_cagetory = self.client.get_channel(arena_cagetory_ID)

                                if channel.id in move_blacklist:
                                    pass
                                else:
                                    await channel.edit(position=0, category=arena_cagetory)
                            if not "active" in old_name:
                                await channel.edit(name=old_channel_name + " active")
                            try:
                                async with self.client.db.execute(
                                        f"SELECT * FROM pingME WHERE channelID = ? AND guildID = ?", (channel.id, message.guild.id)) as cursor:
                                    listOfAllItems = await cursor.fetchall()
                            except Exception as e:
                                print(f"Error is {e}")
                                pass
                            else:

                                PingMeInThere = []
                                if len(listOfAllItems) > 0:
                                    for i in listOfAllItems:
                                        PingMeInThere.append(int(i[2]))

                                # PingMeInThere = db.child("pingme").child(channel.id).get().val()
                                if len(PingMeInThere) == 0:

                                    return
                                else:
                                    list_of_pings = []
                                    pings = ""
                                    for key in PingMeInThere:
                                        member = message.guild.get_member(int(key))
                                        if member == None:
                                            pass
                                        else:
                                            list_of_pings.append(member.mention)
                                        if len(pings) < 2000:

                                            if member == None:
                                                pass
                                            else:
                                                pings += f"{member.mention}"
                                        else:
                                            list_of_pings.append(pings)
                                            pings = ""
                                            if member == None:
                                                pass
                                            else:
                                                pings += f"{member.mention}"
                                    active_alerts = self.client.get_channel(active_alerts_ID)
                                    if active_alerts is not None:
                                        if len(list_of_pings) > 0:
                                            pings = ""
                                            for msg in list_of_pings:
                                                if len(pings) < 1800:
                                                    pings += f"{msg} "
                                                else:
                                                    await active_alerts.send(pings)
                                                    pings = ""
                                                    pings += f"{msg} "
                                            if len(pings) < 1800 and pings != "":
                                                await active_alerts.send(pings)

                                        embed = Embed(description=message.content or "", color=random_color())
                                        embed.add_field(name="Source",
                                                        value=f"[Jump](https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id})",
                                                        inline=False)
                                        if len(message.attachments):
                                            embed.set_image(url=message.attachments[0].url)
                                        embed.set_author(name=message.author, icon_url=message.author.avatar.url)
                                        await active_alerts.send(embed=embed)
                                        await active_alerts.send(f"{channel.mention} is now active!")

                                        return






def setup(client):
    client.add_cog(Active(client))