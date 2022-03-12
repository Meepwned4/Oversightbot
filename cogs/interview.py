import discord
import os
from discord.ext import commands
import json
import typing
import nest_asyncio
nest_asyncio.apply()
import OversightData

class colors:
    default = 0
    teal = 0x1abc9c
    dark_teal = 0x11806a
    green = 0x2ecc71
    dark_green = 0x1f8b4c
    blue = 0x3498db
    dark_blue = 0x206694
    purple = 0x9b59b6
    dark_purple = 0x71368a
    magenta = 0xe91e63
    dark_magenta = 0xad1457
    gold = 0xf1c40f
    dark_gold = 0xc27c0e
    orange = 0xe67e22
    dark_orange = 0xa84300
    red = 0xe74c3c
    dark_red = 0x992d22
    lighter_grey = 0x95a5a6
    dark_grey = 0x607d8b
    light_grey = 0x979c9f
    darker_grey = 0x546e7a
    blurple = 0x7289da
    greyple = 0x99aab5

apikey = 'a00d3f1cd6f1ad'
token = 'NzM1MjU3Mzc3NjA3MjU0MTE3.Xxdnyw.yCKnVzcCHxY_vS5GMelz2ElqSXs'
oversight_channel_id = 812131124489879552
disc_channel_id = 605910228692893726
test_oversight_channel_id = 736099358344478764
test_disc_channel_id = 834653321099739177
carthago_server_id = 567336454632636416
nerds_id = 712071416505172090
raider_id = 853790553375768586
guild_id_1 = 567336454632636416
guild_id_2 = 645391966598594561
management_role_id = 568141320011382825
suffet_role_id = 567338425443942420
elder_role_id = 567338487380967430
adirim_role_id = 752227315832062063
pentarch_role_id = 567389583289876490
trainee_role_id = 712071416505172090
foreigner_role_id = 569519945847930911
citizen_role_id = 567389586934726677

right_arrow = '➡' # right arrow emoji
robot = '🤖' # robot emoji
person = '🧑' # person emoji
interview_emoji = '📝' # interview emoji
x_emoji = '❌' # x emoji

class interview(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_message(self, message):
        client = self.client
        # Check if the message came from the bot and contains specific message
        if message.author == client.user:
            if 'confirm by reacting or responding to this message' in message.content:
              emoji = '\N{THUMBS UP SIGN}' # Thumbs up emoji
              await message.add_reaction(emoji)
        if str(message.channel.type) == 'private' or str(message.channel.type) == 'group':
            if message.author != client.user:
                channel = client.get_channel(946196124614664212)
                author_id = message.author.id
                author_name = message.author.name 
                
                message_content = message.content
                embed = discord.Embed(title = f'USER: {author_name}\nID: {author_id}',
                                description = f'MESSAGE: {message_content}', color=colors.teal)
                await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if channel.category.id == 567390184774303745 or channel.category.id == 876639217042751578:
            chan_name = channel.name.split('-')
            if chan_name[0] == 'ticket':
                message = f'''
                Please read and follow these instructions before you proceed with the prompt below, provided by the bot.

                - Apply to us at: https://politicsandwar.com/alliance/join/id=5049
                - No current in-game wars or alliance;
                - No unsettled debt or loans;
                - You must be active on Discord and in-game, inactivity is not acceptable;
                - You must obey orders in a timely manner, abide by our rules and listen to your superiors, insubordination will not be tolerated.
                - You cannot possess two or more nations/accounts in the same network. This is a grave offense that may lead to banishment.

                React with {interview_emoji} if you are applying
                React with {person} if you stumbled upon this place for any other reason
                '''
                embed = discord.Embed(title = f'Application',
                                    description = f'{message}', color=colors.dark_gold)
                msg = await channel.send(embed=embed)
                await msg.add_reaction(interview_emoji)
                await msg.add_reaction(person)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        client = self.client
        message_id = payload.message_id
        if payload.guild_id == guild_id_1:
            guild = client.get_guild(guild_id_1)
            channels = guild.channels
        if payload.guild_id == guild_id_2:
            guild = client.get_guild(guild_id_2)
            channels = guild.channels
        member = payload.member
        emoji = payload.emoji
        message_id = payload.message_id
        channel_id = payload.channel_id
        if not member.bot:
            for channel in channels:
                if channel.id == channel_id:
                    channel = channel
                    break
            user_message = await channel.fetch_message(message_id)
            
            if f'React with {right_arrow} to begin the automated interview' in \
            user_message.embeds[0].description or f'react with {right_arrow} to continue' in \
            user_message.embeds[0].description  or f'React with {interview_emoji} if you are applying' in \
            user_message.embeds[0].description:
                if emoji.name == right_arrow or emoji.name == person \
                or emoji.name == interview_emoji:
                    chan = user_message.channel
                    chan_id = chan.id
                    chan_name = chan.name
                    for reaction in user_message.reactions:
                        users = reaction.users()
                        async for user in users:
                            if member == user and reaction.emoji == emoji.name:
                                reaction = reaction
                                break
                    if emoji.name == person:
                        disc_channel = client.get_channel(disc_channel_id)
                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> requests assistance')
                        message = 'Staff have been notified.\nPlease be patient.'
                        embed = discord.Embed(title = f'Notice',
                                        description = f'{message}', color=colors.dark_gold)
                        await chan.send(embed=embed)
                        await user_message.reactions[1].remove(member)
                    if emoji.name == interview_emoji:
                        num = '0'
                        try:
                            with open(f'./data/tickets/{chan_name}-{chan_id}.json') as data:
                                dic = json.load(data)
                            dic.update({'num':num})
                        except:
                            dic = {'channel':chan.name, 'user_id':member.id}
                            dic.update({'num':num})
                        with open(f'./data/tickets/{chan_name}-{chan_id}.json', 'w') as outfile:
                            json.dump(dic, outfile)
                        message = OversightData.interview_message(num, member)
                        embed = discord.Embed(title = f'Interview information',
                                        description = f'{message}', color=colors.dark_gold)
                        msg = await chan.send(embed=embed)
                        await msg.add_reaction(right_arrow)
                        await msg.add_reaction(person)
                        await user_message.reactions[0].remove(member)
                        
                    if emoji.name == right_arrow:
                        disc_channel = client.get_channel(disc_channel_id)
                        try:
                            with open(f'./data/tickets/{chan_name}-{chan_id}.json') as data:
                                dic = json.load(data)
                        except:
                            num = '0'
                            dic = {'channel':chan.name, 'user_id':member.id}
                            dic.update({'num':num})
                        num = int(dic.get('num'))
                        num += 1
                        num = str(num)
                        dic.update({'num':num})
                        with open(f'./data/tickets/{chan_name}-{chan_id}.json', 'w') as outfile:
                            json.dump(dic, outfile)
                        if num == '9':
                            message_list = OversightData.interview_message(num, member)
                            l = 0
                            for item in message_list:
                                l += 1
                                if l == 1:
                                    embed = discord.Embed(title = f'Question number {num}',
                                                description = f'{item}', color=colors.dark_gold)
                                    await chan.send(embed=embed)
                                else:
                                    embed = discord.Embed(title = f'',
                                                description = f'{item}', color=colors.dark_gold)
                                    msg = await chan.send(embed=embed)
                                    await msg.add_reaction(right_arrow)
                                    await msg.add_reaction(person)
                            await user_message.reactions[0].remove(member)
                        elif num == '11':
                            message = OversightData.interview_message(num, member)
                            embed = discord.Embed(title = f'',
                                                description = f'{message}', color=colors.dark_gold)
                            msg = await chan.send(embed=embed)
                            await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                            os.remove(f'./data/tickets/{chan_name}-{chan_id}.json')
                            await user_message.reactions[0].remove(member)
                        else:
                            message = OversightData.interview_message(num, member)
                            embed = discord.Embed(title = f'Question number {num}',
                                            description = f'{message}', color=colors.dark_gold)
                            msg = await chan.send(embed=embed)
                            await msg.add_reaction(right_arrow)
                            await msg.add_reaction(person)
                            with open(f'./data/tickets/{chan_name}-{chan_id}.json', 'w') as outfile:
                                json.dump(dic, outfile)
                            await user_message.reactions[0].remove(member)
    
    @commands.command(name='start', help='+start')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'Interviewer')
    async def start(self, ctx, num: typing.Optional[str] = '0' ):
        if ctx.channel.category.id == 567390184774303745 or ctx.channel.category.id == 876639217042751578 or ctx.channel.id == 736099358344478764:
            chan_name = ctx.channel.name
            chan_id = ctx.channel.id
            suffet_role = ctx.guild.get_role(suffet_role_id)
            elder_role = ctx.guild.get_role(elder_role_id)
            pentarch_role = ctx.guild.get_role(pentarch_role_id)
            interviewer_role = ctx.guild.get_role(management_role_id)
            adirim_role = ctx.guild.get_role(adirim_role_id)
            try:
                with open(f'./data/tickets/{chan_name}-{chan_id}.json') as data:
                    dic = json.load(data)
                dic.update({'num':num})
                with open(f'./data/tickets/{chan_name}-{chan_id}.json', 'w') as outfile:
                    json.dump(dic, outfile)
            except:
                for member in ctx.channel.members:
                    if suffet_role not in member.roles and elder_role not in member.roles \
                    and pentarch_role not in member.roles and interviewer_role not in member.roles \
                    and adirim_role not in member.roles:
                        member_id = member.id
                        break
                dic = {'channel':ctx.channel.name, 'user_id':member_id}
                dic.update({'num':num})
                with open(f'./data/tickets/{chan_name}-{chan_id}.json', 'w') as outfile:
                    json.dump(dic, outfile)
            user = None
            message = OversightData.interview_message(num, user)
            if num != '0':
                embed = discord.Embed(title = f'Question number {num}',
                            description = f'{message}', color=colors.dark_gold)
            else:
                embed = discord.Embed(title = f'Interview information',
                            description = f'{message}', color=colors.dark_gold)
            msg = await ctx.send(embed=embed)
            await msg.add_reaction(right_arrow)
            await msg.add_reaction(person)

    @commands.command(name='next', help='+next')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'Interviewer')
    async def next(self, ctx):
        if ctx.channel.category.id == 567390184774303745 or ctx.channel.category.id == 876639217042751578 or ctx.channel.id == 736099358344478764:
            chan_name = ctx.channel.name
            chan_id = ctx.channel.id
            suffet_role = ctx.guild.get_role(suffet_role_id)
            elder_role = ctx.guild.get_role(elder_role_id)
            pentarch_role = ctx.guild.get_role(pentarch_role_id)
            interviewer_role = ctx.guild.get_role(management_role_id)
            adirim_role = ctx.guild.get_role(adirim_role_id)
            try:
                with open(f'./data/tickets/{chan_name}-{chan_id}.json') as data:
                    dic = json.load(data)
                num = int(dic.get('num'))
            except:
                for member in ctx.channel.members:
                    if suffet_role not in member.roles and elder_role not in member.roles \
                    and pentarch_role not in member.roles and interviewer_role not in member.roles \
                    and adirim_role not in member.roles:
                        member_id = member.id
                        break
                dic = {'channel':ctx.channel.name, 'user_id':member_id}
                dic.update({'num':'0'})
                with open(f'./data/tickets/{chan_name}-{chan_id}.json', 'w') as outfile:
                    json.dump(dic, outfile)
                with open(f'./data/tickets/{chan_name}-{chan_id}.json') as data:
                    dic = json.load(data)
                    num = int(dic.get('num'))
            num = int(num)
            num += 1
            num = str(num)
            dic.update({'num':num})
            with open(f'./data/tickets/{chan_name}-{chan_id}.json', 'w') as outfile:
                json.dump(dic, outfile)
            user = None
            if num != '11':
                if num == '9':
                    message_list = OversightData.interview_message(num, user)
                    l = 0
                    for item in message_list:
                        l += 1
                        if l == 1:
                            embed = discord.Embed(title = f'Question number {num}',
                                        description = f'{item}', color=colors.dark_gold)
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(title = f'',
                                        description = f'{item}', color=colors.dark_gold)
                            msg = await ctx.send(embed=embed)
                            await msg.add_reaction(right_arrow)
                            await msg.add_reaction(person)
                else:
                    message = OversightData.interview_message(num, user)
                    embed = discord.Embed(title = f'Question number {num}',
                                    description = f'{message}', color=colors.dark_gold)
                    msg = await ctx.send(embed=embed)
                    await msg.add_reaction(right_arrow)
                    await msg.add_reaction(person)
                data = open(f'./data/tickets/{chan_name}-{chan_id}.json')
                dic = json.load(data)
                dic.update({'num':num})
                for user in ctx.channel.members:
                    if 'foreigner' in user.roles:
                        user_id = user.id
                        dic.update({'user_id':user_id})
            elif num == '11':
                embed = discord.Embed(title = f'',
                                    description = f'{item}', color=colors.dark_gold)
                msg = await ctx.send(embed=embed)
                await msg.add_reaction(right_arrow)
                await msg.add_reaction(person)
                os.remove(f'./data/tickets/{chan_name}-{chan_id}.json') 
            await ctx.message.delete()


def setup(client):
	client.add_cog(interview(client))