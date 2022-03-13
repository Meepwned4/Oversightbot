import discord
from discord.ext import commands
import chat_exporter
import pickle
import json
import typing
import requests
import aiohttp
from bs4 import BeautifulSoup
import os

right_arrow = '➡' # right arrow emoji
robot = '🤖' # robot emoji
person = '🧑' # person emoji
interview_emoji = '📝' # interview emoji
elephant = '\N{ELEPHANT}' # elephant emoji
x_emoji = '❌' # x emoji
guild_id = 567336454632636416
information_board = 714233548332204084
archive_channel = 754640623276916756
ticket_category_name = '[Admission & Training]'
management_role_id = 568141320011382825
suffet_role_id = 567338425443942420
elder_role_id = 567338487380967430
pentarch_role_id = 568141320011382825
adirim_role_id = 752227315832062063
bot_role_id = 567722813335535622
trainee_role_id = 712071416505172090
foreigner_role_id = 569519945847930911
citizen_role_id = 567389586934726677

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

class ticket(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    # Ignore these
    ticket_category = None
    management_role = None
    guild = None

    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        client = self.client
        member = payload.member
        emoji = payload.emoji
        message_id = payload.message_id
        channel_id = payload.channel_id
        
        try:
            guild = client.get_guild(guild_id)
            ticket_category = discord.utils.get(guild.categories, name=ticket_category_name)
            management_role = guild.get_role(management_role_id)  # management role
            channel = guild.get_channel(channel_id)
        except:
            guild = client.get_guild(645391966598594561)
            ticket_category = discord.utils.get(guild.categories, name=ticket_category_name)
            management_role = guild.get_role(management_role_id)  # management role
            channel = guild.get_channel(channel_id)
        
        if not member.bot:
            message = 'Welcome to Carthago Co-Operative Alliance. We are glad to see you recognize the glory of the Shining City and wish to join us.'
            
            user_message = await channel.fetch_message(message_id)
            for embed in user_message.embeds:
                if message in embed.description and emoji.name == elephant and \
                user_message.author == client.user:
                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(view_channel=False),
                        member: discord.PermissionOverwrite(view_channel=True),
                        guild.me: discord.PermissionOverwrite(view_channel=True),
                        management_role: discord.PermissionOverwrite(view_channel=True),
                    }
                    
                    pickle_off = open('./data/num.pickle', 'rb')
                    num = pickle.load(pickle_off)
                    num += 1
                    await ticket_category.create_text_channel(
                            f'ticket-{num}', overwrites=overwrites)
                    chan = discord.utils.get(guild.text_channels, name=f'ticket-{num}')
                    dic = {'channel':chan.name, 'user_id':member.id}
                    with open(f'./data/tickets/{chan.name}-{chan.id}.json', 'w') as outfile:
                        json.dump(dic, outfile)
                            
                    pickling_on = open('./data/num.pickle', 'wb')
                    pickle.dump(num, pickling_on)
                    pickling_on.close()
                    await user_message.reactions[0].remove(member)
                    break
                if message in embed.description and emoji.name == robot and \
                user_message.author == client.user:
                    await user_message.clear_reaction(elephant)
                    await user_message.add_reaction(elephant)
                    break
                
                
    
    
    @commands.command(name='sendticket', help='+sendticket')
    @commands.has_any_role('Elder', 'Suffet')
    async def sendticket(self, ctx):
        embed = discord.Embed(
            title='Application',
            description='''
            Welcome to Carthago Co-Operative Alliance. We are glad to see you recognize the glory of the Shining City and wish to join us.
            
            Please make sure you've applied at the Alliance Page: https://politicsandwar.com/alliance/join/id=5049
            
            If that's done, react with :elephant: to apply.
            ''', color=colors.dark_gold
        )
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(elephant)
        await ctx.message.delete()
    
    @commands.command(help='+approve')
    @commands.has_any_role('Interviewer', 'Pentarch', 'Elder', 'Suffet')
    async def approve(self, ctx):
        trainee_role = ctx.guild.get_role(trainee_role_id)
        foreigner_role = ctx.guild.get_role(foreigner_role_id)
        citizen_role = ctx.guild.get_role(citizen_role_id)
        suffet_role = ctx.guild.get_role(suffet_role_id)
        pentarch_role = ctx.guild.get_role(pentarch_role_id)
        elder_role = ctx.guild.get_role(elder_role_id)
        interviewer_role = ctx.guild.get_role(management_role_id)
        adirim_role = ctx.guild.get_role(adirim_role_id)
        bot_role = ctx.guild.get_role(bot_role_id)
        pickle_off = open('./data/api_key.pickle', 'rb')
        apikey = pickle.load(pickle_off)
        chan = ctx.channel
        try:
            
            with open(f'./data/tickets/{chan.name}-{chan.id}.json') as data:
                data = json.load(data)
            discord_id = data.get('user_id')
#            discord_id = 605929396724826135
            user = requests.get(
                f'http://24.117.204.187:8080/discord/?DiscordID={discord_id}&key=davethsmellskrampuswhales')
            user = user.json()
            user = user[0]
            for member in ctx.channel.members:
                if member.id == discord_id:
                    break
        except:
            for member in ctx.channel.members:
               if suffet_role not in member.roles and elder_role not in member.roles \
                and pentarch_role not in member.roles and interviewer_role not in member.roles \
                and adirim_role not in member.roles and bot_role not in member.roles:
                    discord_id = member.id
                    break
#            discord_id = 502150110940233730
            user = requests.get(
                f'http://24.117.204.187:8080/discord/?DiscordID={discord_id}&key=davethsmellskrampuswhales')
            user = user.json()
            user = user[0]
        
        nation_id = user.get('_id')
        try:
            nation = requests.get(
                f'http://24.117.204.187:8080/nations/?_id={nation_id}&key=davethsmellskrampuswhales')
            nation = nation.json()
            nation = nation[0]
        except:
            fetcheddata = requests.get(
                    'https://politicsandwar.com/api/nation/' +
                    f'?id={nation_id}&key={apikey}')
            fetcheddata = fetcheddata.json()
            memberdata = fetcheddata.get(['nations'][0])
            for dic in memberdata:
                if dic.get('nationid') == nation_id:
                    nation = dic
                    break
        user_name = user.get('leader')
        channel_name = user.get('leader').replace(' ', '-') + '-' + str(user.get('NationID'))
        nation_link = f'https://politicsandwar.com/nation/id={nation_id}'
        login_data = {'email': 'jacksonayres11@gmail.com', 'password': 'Dungeons&Dragons', 'loginform': 'Login'}
        async with aiohttp.ClientSession() as session:
            login_url = 'https://politicsandwar.com/login/'
            res1 = await session.post(login_url, data=login_data)
            if(len((BeautifulSoup(await res1.text(), 'html.parser')).body.findAll(text='Login Failure')) > 0):
                print('Login failed')
                raise   Exception('Login failed')
            url = 'https://politicsandwar.com/alliance/id=5049#permissions'
            perms_data = {'nationperm':f'{user_name}', 'level':'2', 'permsubmit':'Go'}
#            res2 = await session.get(url);
#            text = await res2.text()
#            auth_token = (BeautifulSoup(text, 'html.parser')).find('input', {'name':'token'})['value']
#            perms_data.update({'token': auth_token})
            await session.post(url, data=perms_data)
            await session.close()
        await ctx.channel.edit(name=channel_name, topic=nation_link)
        if nation.get('cities') <= 10:
            if nation.get('cenciveng') == True and nation.get('intagncy') == True \
            and nation.get('propbureau') == True:
                await member.remove_roles(citizen_role)
                await member.remove_roles(foreigner_role)
            else:
                await member.add_roles(trainee_role)
                await member.remove_roles(foreigner_role)
    
    @commands.command(help='+save')
    @commands.has_any_role('Interviewer', 'Pentarch', 'Elder', 'Suffet')
    async def save(self, ctx: commands.Context):
        client = self.client
        await ctx.message.delete()
        embed = discord.Embed(title='Ticket manually saved',color=colors.dark_gold)
        embed.add_field(name = 'Saved by',
                    value = f'<@{ctx.author.id}>',
                    inline = True)
        embed.add_field(name = 'Ticket name',
                    value = f'{ctx.channel.name}',
                    inline = True)
        embed.add_field(name = 'Reason',
                    value = 'Manually saved',
                    inline = False)
        transcript = await chat_exporter.export(ctx.channel)
    
        if transcript is None:
            return
    
        file = open(f'./data/transcripts/transcript-{ctx.channel.name}.html', 'w')
        file.write(transcript)
        file.close()
        transcript_file = open(f'./data/transcripts/transcript-{ctx.channel.name}.html', 'r')
        channel = client.get_channel(archive_channel)
        await channel.send(embed=embed)
        await channel.send(file=discord.File(transcript_file))
    
    @commands.command(help='+close (reason)')
    @commands.has_any_role('Interviewer', 'Pentarch', 'Elder', 'Suffet')
    async def close(self, ctx, *, reason: typing.Optional[str] = 'Not specified'):
        client = self.client
        guild = client.get_guild(guild_id)
        ticket_category = discord.utils.get(guild.categories, name=ticket_category_name)
        channel_name = ctx.channel.name.split('-')
        channel_name = channel_name[0]
        suffet_role = ctx.guild.get_role(suffet_role_id)
        elder_role = ctx.guild.get_role(elder_role_id)
        pentarch_role = ctx.guild.get_role(pentarch_role_id)
        interviewer_role = ctx.guild.get_role(management_role_id)
        adirim_role = ctx.guild.get_role(adirim_role_id)
        if ctx.message.channel.category == ticket_category and channel_name == 'ticket':
            await ctx.message.delete()
            try:
                with open(f'./data/tickets/{ctx.channel.name}-{ctx.channel.id}.json') as data:
                    data = json.load(data)
                    user_id = data.get('user_id')
                    channel_name = data.get('channel')
            except:
                for member in ctx.channel.members:
                    if suffet_role not in member.roles and elder_role not in member.roles \
                    and pentarch_role not in member.roles and interviewer_role not in member.roles \
                    and adirim_role not in member.roles:
                        user_id = member.id
                        channel_name = data.get('channel')
                        break
            embed = discord.Embed(title='Ticket closed',color=colors.dark_gold)
            embed.add_field(name = 'Opened by',
                        value = f'<@{user_id}>',
                        inline = True)
            embed.add_field(name = 'Closed by',
                        value = f'<@{ctx.author.id}>',
                        inline = True)
            embed.add_field(name = 'Ticket name',
                        value = f'{channel_name}',
                        inline = True)
            embed.add_field(name = 'Reason',
                        value = f'{reason}',
                        inline = False)
            transcript = await chat_exporter.export(ctx.channel)
        
            if transcript is None:
                return
        
            file = open(f'./data/transcripts/transcript-{ctx.channel.name}.html', 'w')
            file.write(transcript)
            file.close()
            transcript_file = open(f'./data/transcripts/transcript-{ctx.channel.name}.html', 'r')
            channel = client.get_channel(archive_channel)
            await channel.send(embed=embed)
            await channel.send(file=discord.File(transcript_file))
            try:    
                if 'ticket' in ctx.channel.name:
                    await ctx.channel.delete()
                else:
                    await ctx.send('❌ This does not seem like a ticket channel.')
            except:
                await ctx.send('❌ This does not seem like a ticket channel.')
            os.remove(f'./data/tickets/{channel_name}-{ctx.channel.id}.json')

def setup(client):
    client.add_cog(ticket(client))