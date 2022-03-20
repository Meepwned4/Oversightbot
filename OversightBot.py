import discord
import requests
import traceback
import sys
import os
import importlib
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
from discord.ext.commands import MissingAnyRole, CommandOnCooldown
from discord import DMChannel
import time
import pickle
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import utc
import nest_asyncio
nest_asyncio.apply()
import OversightData
import logging

'''
Options for logging:
logging.NOTSET - No logging
logging.DEBUG - All info
logging.INFO - Slightly less
logging.WARN - Only warnings and worse
logging.ERROR - Only errors and worse
'''

logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%b-%d-%y %H:%M:%S')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

logging.basicConfig(filename='app.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%b-%d-%y %H:%M:%S')

pickle_off = open('./data/api_key.pickle', 'rb')
apikey = pickle.load(pickle_off)
pickle_off = open('./data/token.pickle', 'rb')
token = pickle.load(pickle_off)
oversight_channel_id = 812131124489879552
disc_channel_id = 605910228692893726
test_oversight_channel_id = 736099358344478764
test_disc_channel_id = 834653321099739177
carthago_server_id = 567336454632636416
nerds_id = 712071416505172090
raider_id = 853790553375768586

right_arrow = '➡' # right arrow emoji
robot = '🤖' # robot emoji
person = '🧑' # person emoji
interview = '📝' # interview emoji

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='+', intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(activity=discord.Game(
        'Hauling mad cash'))

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    try:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} loaded')
    except:
        await ctx.send(f'{extension} not recognized')

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} unloaded')
    except:
        await ctx.send(f'{extension} not recognized')

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    if extension == 'oversightdata' or extension == 'OversightData':
        try:
            importlib.reload(OversightData)
            await ctx.send(f'{extension} reloaded')
        except:
            await ctx.send(f'{extension} not recognized')
    else:
        try:
            client.unload_extension(f'cogs.{extension}')
            client.load_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} reloaded')
        except:
            await ctx.send(f'{extension} not recognized')

@client.command()
@commands.is_owner()
async def logs(ctx):
    user = ctx.author
    try:
        await DMChannel.send(user, file=discord.File('app.log'))
    except:
        msg = 'Failed to send logs'
        await DMChannel.send(user, msg)

@client.command()
@commands.is_owner()
async def get_memberdata(ctx):
    user = ctx.author
    try:
        await DMChannel.send(user, file=discord.File('./data/memberdata.json'))
    except:
        msg = 'Failed to send memberdata'
        await DMChannel.send(user, msg)

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

async def daily():
    print('Daily Start!')
    target_channel = client.get_channel(oversight_channel_id)
    disc_channel = client.get_channel(disc_channel_id)
#    target_channel = client.get_channel(test_oversight_channel_id)
#    disc_channel = client.get_channel(test_oversight_channel_id)
    server = client.get_guild(carthago_server_id)
    pickle_off = open('./data/mmr.pickle', 'rb')
    mmr = pickle.load(pickle_off)
    mmr_list = mmr.split()
    mmr = mmr_list[0]
    oldmemberdata = []
    oldmemberdata = OversightData.data_retrieval(oldmemberdata)
    nerds_list = []
    raider_list = []
    piggy_id = 236978935538122754
    
    fetcheddata = requests.get(
            'https://politicsandwar.com/api/alliance-members/' +
            f'?allianceid=5049&key={apikey}')
    fetcheddata = fetcheddata.json()
    memberdata = fetcheddata.get(['nations'][0])
    list_of_dics = requests.get(
        'http://24.117.204.187:8080/discord/?alliance=5049' +
        '&key=davethsmellskrampuswhales')
    list_of_dics = list_of_dics.json()
    memberdata = OversightData.merge_memberdata(memberdata, oldmemberdata, list_of_dics)              

    for chan in server.text_channels:
        if chan.category.id == 605910228692893726:
            if chan.id != 605910228692893726 and chan.id != 845685557367144448 and \
            chan.id != 568822425253576739:
                chan_id = chan.id
                for member in chan.members:
                    if member.id == piggy_id:
                        continue
                    else:
                        member_id = str(member.id)
                        for dic in memberdata:
                            if dic.get('DiscordID') == member_id:
                                for role in member.roles:
                                    role_id = role.id
                                    if role_id == nerds_id:
                                        nerds_list.append(str(member_id))
                                        dic.update({'ChannelID': chan_id})
        if chan.id == 812131124489879552:
            for member in chan.members:
                if member.id == piggy_id:
                    continue
                else:
                    member_id = str(member.id)
                    for dic in memberdata:
                        if dic.get('DiscordID') == member_id:
                            for role in member.roles:
                                role_id = role.id
                                if role_id == raider_id:
                                    raider_list.append(str(member_id))
    if memberdata[0].get('war_status'):
        for i in memberdata:
            i.update({'war_status':memberdata[0].get('war_status')})
    
    for i in memberdata:
        if i.get('DiscordID') in nerds_list:
            i.update({'Trainee':1})
        else:
            i.update({'Trainee':0})
        if not i.get('ChannelID'):
            i.update({'ChannelID':0})
        if not i.get('ping'):
            i.update({'ping':{'color':0, 'soldiers':0, 'ships':0,
                            'login':0, 'tanks':0, 'spies':0}})
        for dic in list_of_dics:
            if i.get('nationid') == dic.get(
                    '_id'):
                i.update({'DiscordID':dic.get('DiscordID')})
                                          
    for nation in memberdata:
        if nation.get('DiscordID') in nerds_list:
            nation.update({'Trainee':1})
        else:
            nation.update({'Trainee':0})
    OversightData.data_storage(memberdata)
    
    pinglist = []
    login_nationids = []
    number = 3
    reminder = '**Reminder**, if you buy a new city, you won\'t ' + \
        'meet MMR until you buy the units for that city.' + \
        '\n\nLet us know if you\'ve read this, confirm by reacting or ' +\
        'responding to this message.'
    login_temp = f'__People who have been inactive for more than {number} days:__\n'
    nerds_login_temp = f'__Trainees who have been inactive for more than {number} days:__\n'
    no_temp = f'**__Members that need to be DMed for failure to comply within {number} days.__**\n\n'
    number *= 1440
    login_ping = [login_temp]
    login_no_ping = [login_temp]
    duplicate_ping_check = []
    nerds_login_ping = [nerds_login_temp]
    for dic in memberdata:
        for key, val in dic.items():
            if key == 'minutessinceactive':
                if dic.get(key) >= number and dic.get('vacmode') == '0':
                    minutes = dic.get(key)
                    minutes = minutes / 1440
                    b = dic.get('nationid')
                    login_nationids.append(b)
                    if b not in pinglist:
                        pinglist.append(b)
        for dic1 in oldmemberdata:
            if dic.get('nationid') in duplicate_ping_check:
                continue
            if dic.get('nationid') != dic1.get('nationid'):
                continue
            if dic1.get('nationid') in login_nationids:
                ping_dic = dic.get('ping')
                if not ping_dic.get('login'):
                    ping_dic.update({'login':0})
                num = ping_dic.get('login')
                c = dic.get('DiscordID')
                c = str(c)
                if c in nerds_list:
                    duplicate_ping_check.append(c)
                    c = dic.get('ChannelID')
                    nerds_login_ping.append(f'<#{c}> {minutes:.0f} days\n')
                    num += 1
                    ping_dic.update({'login':num})
                    continue
                if ping_dic.get('login'):
                    if ping_dic.get('login') >= 3:
                        duplicate_ping_check.append(c)
                        login_no_ping.append(f'<@{c}> ')
                        ping_dic.update({'login':num})
                if c not in nerds_list:
                    duplicate_ping_check.append(c)
                    login_ping.append(f'<@{c}> ')
                    num += 1
                    ping_dic.update({'login':num})
    if not login_ping:
            login_ping = 'Everyone has logged in within 3 days.'
    if nerds_login_ping == nerds_login_temp:
        nerds_login_ping = 'Everyone has logged in within 3 days.'

    nmp_temp = '\n__People who don\'t have max planes__\n'
    nmp_ping = [nmp_temp]
    nmp_no_ping = [nmp_temp]
    nmp_nationids = []
    nerds_nmp_temp = '\n__Trainees who don\'t have max planes:__\n'
    nerds_nmp_ping = [nerds_nmp_temp]
    duplicate_ping_check = []

    for dic in memberdata:
        plane_mmr = int(dic.get('cities') * int(mmr[2]) * 15)
        if plane_mmr > int(dic.get('aircraft')) and \
            dic.get('vacmode') == '0':
            planes = int(dic.get('aircraft'))
            b = dic.get('nationid')
            nmp_nationids.append(b)
            if b not in pinglist:
                pinglist.append(b)
        for dic2 in oldmemberdata:
            if dic.get('nationid') in duplicate_ping_check:
                continue
            if dic.get('nationid') == dic2.get('nationid'):
                if dic.get('nationid') in nmp_nationids:
                    if dic2.get('aircraft') >= dic.get('aircraft'):
                        ping_dic = dic.get('ping')
                        if not ping_dic.get('aircraft'):
                            ping_dic.update({'aircraft':0})
                        num = ping_dic.get('aircraft')
                        c = dic2.get('DiscordID')
                        c = str(c)
                        if c in nerds_list:
                            duplicate_ping_check.append(c)
                            c = dic.get('ChannelID')
                            nerds_nmp_ping.append(f'<#{c}> {planes}\n')
                            ping_dic.update({'aircraft':num})
                            continue
                        if ping_dic.get('ping'):
                            if ping_dic.get('ping') >= 3:
                                duplicate_ping_check.append(c)
                                nmp_no_ping.append(f'<@{c}> ')
                                num += 1
                                ping_dic.update({'aircraft':num})
                        if c not in nerds_list:
                            duplicate_ping_check.append(c)
                            nmp_ping.append(f'<@{c}> ')
                            num += 1
                            ping_dic.update({'aircraft':num})
    if not nmp_ping:
        nmp_ping = 'Everyone has max planes.'
    if not nerds_nmp_ping:
        nerds_nmp_ping = 'Everyone has max planes.'

    nsp_nationids = []
    nsp_temp = '\n\n__People who don\'t have max spies:__\n'
    nsp_ping = [nsp_temp]
    nsp_no_ping = [nsp_temp]
    nerds_nsp_temp = '\n__Trainees who don\'t have max spies:__\n'
    nerds_nsp_ping = [nerds_nsp_temp]
    duplicate_ping_check = []
    
    for dic in memberdata:
        if int(dic.get('intagncy'))== 1:
            if int(dic.get('spies')) != 60 and dic.get('vacmode') == '0':
                spies = int(dic.get('spies'))
                spies = str(f'{spies}/60')
                b = dic.get('nationid')
                nsp_nationids.append(b)
                if b not in pinglist:
                    pinglist.append(b)
        if int(dic.get('intagncy'))== 0:
            if int(dic.get('spies')) != 50 and dic.get('vacmode') == '0':
                spies = int(dic.get('spies'))
                spies = str(f'{spies}/50')
                b = dic.get('nationid')
                nsp_nationids.append(b)
                if b not in pinglist:
                    pinglist.append(b)
        for dic2 in oldmemberdata:
            if dic.get('nationid') in duplicate_ping_check:
                continue
            if dic.get('nationid') == dic2.get('nationid'):
                if dic.get('nationid') in nsp_nationids:
                    if dic2.get('spies') >= dic.get('spies'):
                        ping_dic = dic.get('ping')
                        if not ping_dic.get('spies'):
                            ping_dic.update({'spies':0})
                        num = ping_dic.get('spies')
                        c = dic.get('DiscordID')
                        c = str(c)
                        if c in nerds_list:
                            duplicate_ping_check.append(c)
                            c = dic.get('ChannelID')
                            nerds_nsp_ping.append(f'<#{c}> {spies}\n')
                            ping_dic.update({'spies':num})
                            continue
                        if ping_dic.get('ping'):
                            if ping_dic.get('ping') >= 3:
                                duplicate_ping_check.append(c)
                                nsp_no_ping.append(f'<@{c}> ')
                                ping_dic.update({'spies':num})
                        if c not in nerds_list:
                            duplicate_ping_check.append(c)
                            nsp_ping.append(f'<@{c}> ')
                            num += 1
                            ping_dic.update({'spies':num})
    if not nsp_ping:
        nsp_ping = 'Everyone has max spies.'
    if nerds_nsp_ping == nerds_nsp_temp:
        nerds_nsp_ping = 'Everyone has max spies.'


    nmt_nationids = []
    nmt_temp = '\n\n__People who don\'t have max tanks__\n'
    nmt_ping = [nmt_temp]
    nerds_nmt_temp = '\n__Trainees who have tanks:__\n'
    nerds_nmt_ping = [nerds_nmt_temp]
    nmt_no_ping = [nmt_temp]
    duplicate_ping_check = []
    
    for dic in memberdata:
        tank_mmr = int(dic.get('cities') * int(mmr[1]) * 250)
        if tank_mmr > int(dic.get('tanks')) and \
            dic.get('vacmode') == '0':
                tanks = int(dic.get('tanks'))
                b = dic.get('nationid')
                nmt_nationids.append(b)
                if b not in pinglist:
                    pinglist.append(b)
        for dic2 in oldmemberdata:
            if dic.get('nationid') in duplicate_ping_check:
                continue
            if dic.get('nationid') == dic2.get('nationid'):
                tanks = int(dic.get('tanks'))
                if dic.get('nationid') in nmt_nationids:
                    if dic2.get('tanks') >= dic.get('tanks'):
                        ping_dic = dic.get('ping')
                        if not ping_dic.get('tanks'):
                            ping_dic.update({'tanks':0})
                        num = ping_dic.get('tanks')
                        c = dic.get('DiscordID')
                        c = str(c)
                        if c in raider_list:
                            continue
                        if c in nerds_list:
                            if tanks > 0:
                                tanks = str(tanks)
                                duplicate_ping_check.append(c)
                                c = dic.get('ChannelID')
                                nerds_nmt_ping.append(f'<#{c}> {tanks}\n')
                                ping_dic.update({'tanks':num})
                            continue
                        if ping_dic.get('tanks'):
                            if ping_dic.get('tanks') >= 3:
                                duplicate_ping_check.append(c)
                                nmt_no_ping.append(f'<@{c}> ')
                                ping_dic.update({'tanks':num})
                        if c not in nerds_list:
                            duplicate_ping_check.append(c)
                            nmt_ping.append(f'<@{c}> ')
                            num += 1
                            ping_dic.update({'tanks':num})
            else:
                continue
    if not nmt_ping:
        nmt_ping = 'Everyone has max tanks.'
    if not nerds_nmt_ping:
        nerds_nmt_ping = 'Nobody has tanks.'
    
    
    nms_nationids = []
    nms_temp = '\n\n__People who don\'t have max soldiers__\n'
    nms_ping = [nms_temp]
    nms_no_ping = [nms_temp]
    nerds_nms_temp = '\n__Trainees who don\'t have max soldiers:__\n'
    nerds_nms_ping = [nerds_nms_temp]
    duplicate_ping_check = []
    
    for dic in memberdata:
        soldier_mmr = int(dic.get('cities') * int(mmr[0]) * 3000)
        if soldier_mmr > int(dic.get('soldiers')) and \
            dic.get('vacmode') == '0':
            soldiers = int(dic.get('soldiers'))
            b = dic.get('nationid')
            nms_nationids.append(b)
            if b not in pinglist:
                pinglist.append(b)
        for dic2 in oldmemberdata:
            if dic.get('nationid') in duplicate_ping_check:
                continue
            if dic.get('nationid') == dic2.get('nationid'):
                if dic.get('nationid') in nms_nationids:
                    if dic.get('soldiers') >= dic2.get('soldiers'):
                        ping_dic = dic.get('ping')
                        if not ping_dic.get('soldiers'):
                            ping_dic.update({'soldiers':0})
                        num = ping_dic.get('soldiers')
                        c = dic.get('DiscordID')
                        c = str(c)
                        if c in raider_list:
                            continue
                        if c in nerds_list:
                            duplicate_ping_check.append(c)
                            c = dic.get('ChannelID')
                            nerds_nms_ping.append(f'<#{c}> {soldiers}\n')
                            ping_dic.update({'soldiers':num})
                            continue
                        if ping_dic.get('soldiers'):
                            if ping_dic.get('soldiers') >= 3:
                                duplicate_ping_check.append(c)
                                nms_no_ping.append(f'<@{c}> ')
                                ping_dic.update({'soldiers':num})
                        if c not in nerds_list:
                            duplicate_ping_check.append(c)
                            nms_ping.append(f'<@{c}> ')
                            num += 1
                            ping_dic.update({'soldiers':num})
    if not nms_ping:
        nms_ping = 'Everyone has max soldiers.'
    if not nerds_nms_ping:
        nerds_nms_ping = 'Everyone has max soldiers.'


    nmsh_nationids = []
    nmsh_temp = '\n\n__People who don\'t have max ships__\n'
    nmsh_ping = [nmsh_temp]
    nerds_nmsh_temp = '\n__Trainees who have ships:__\n'
    nerds_nmsh_ping = [nerds_nmsh_temp]
    nmsh_no_ping = [nmsh_temp]
    duplicate_ping_check = []
    
    for dic in memberdata:
        ship_mmr = int(dic.get('cities') * int(mmr[3]) * 5)
        if ship_mmr > int(dic.get('ships')) and \
            dic.get('vacmode') == '0':
            b = dic.get('nationid')
            nmsh_nationids.append(b)
            if b not in pinglist:
                pinglist.append(b)
        for dic2 in oldmemberdata:
            if dic.get('DiscordID') in duplicate_ping_check:
                continue
            if dic.get('nationid') == dic2.get('nationid'):
                ships = int(dic.get('ships'))
                if dic.get('nationid') in nmsh_nationids:
                    if dic2.get('ships') >= dic.get('ships'):
                        ping_dic = dic.get('ping')
                        if not ping_dic.get('ships'):
                            ping_dic.update({'ships':0})
                        num = ping_dic.get('ships')
                        c = dic.get('DiscordID')
                        c = str(c)
                        if c in nerds_list:
                            if ships > 0:
                                ships = str(ships)
                                duplicate_ping_check.append(c)
                                c = dic.get('ChannelID')
                                nerds_nmsh_ping.append(f'<#{c}> {ships}\n')
                                ping_dic.update({'ships':num})
                                continue
                        if ping_dic.get('ships'):
                            if ping_dic.get('ships') >= 3:
                                duplicate_ping_check.append(c)
                                nmsh_no_ping.append(f'<@{c}> ')
                                ping_dic.update({'ships':num})
                        if c not in nerds_list:
                            duplicate_ping_check.append(c)
                            nmsh_ping.append(f'<@{c}> ')
                            num += 1
                            ping_dic.update({'ships':num})
    if not nmsh_ping:
        nmsh_ping = 'Everyone has max ships.'
    if not nerds_nmsh_ping:
        nerds_nmsh_ping = 'Everyone doesn\'t have ships.'


    color_nationids = []
    fetcheddata = requests.get(
            'https://politicsandwar.com/api/alliance/id=5049&key=id=5049&key='
            + apikey)
    fetcheddata = fetcheddata.json()
    AA_color = fetcheddata.get('color')
    color_temp = f'\n\n__People not on the nation color {AA_color}:__\n'
    nerds_color_temp = f'\n__Trainees not on the nation color {AA_color}:__\n'
    color_ping = [color_temp]
    nerds_color_ping = [nerds_color_temp]
    color_no_ping = [color_temp]
    duplicate_ping_check = []
    
    for dic in memberdata:
        for key, val in dic.items():
            if key == 'color':
                if val != AA_color and val != 'beige' and \
                    dic.get('vacmode') == '0':
                    b = dic.get('nationid')
                    if int(b) == 210815:
                        continue
                    color_nationids.append(b)
                    if b not in pinglist:
                        pinglist.append(b)
        if dic.get('DiscordID') in duplicate_ping_check:
            continue
        if dic.get('nationid') in color_nationids:
            ping_dic = dic.get('ping')
            if not ping_dic.get('color'):
                ping_dic.update({'color':0})
            num = ping_dic.get('color')
            c = dic.get('DiscordID')
            c = str(c)
            nation_color = dic.get('color')
            if c in nerds_list:
                duplicate_ping_check.append(c)
                c = dic.get('ChannelID')
                nerds_color_ping.append(f'<#{c}> {nation_color}\n')
                ping_dic.update({'color':num})
                continue
            if ping_dic.get('color'):
                if ping_dic.get('color') >= 3:
                    duplicate_ping_check.append(c)
                    color_no_ping.append(f'<@{c}> ')
                    ping_dic.update({'color':num})
            if c not in nerds_list:
                duplicate_ping_check.append(c)
                color_ping.append(f'<@{c}> ')
                num += 1
                ping_dic.update({'color':num})
    
    if not color_ping:
        color_ping = 'Everyone is on the correct color.'
    if not nerds_color_ping:
        nerds_color_ping = 'Everyone is on the correct color.'
    
    color_message_temp = f'\nChange to {AA_color}' + \
    ' <https://politicsandwar.com/nation/edit/> ' + \
    'and vote <https://politicsandwar.com/world/color/voting/> ' + \
    'for \'Olive belongs to Nexus\''
    war_status = ''
    len_check = 0
    message = ''
    no_message = no_temp
    temp_no_message = no_temp
    nerds_message = ''
    war_status = dic.get('war_status')
    if war_status == '1':
        message_list = [login_ping, color_ping]
        no_message_list = [login_no_ping, color_no_ping]
    elif war_status == '0':
        message_list = [login_ping, nms_ping, nmt_ping, nmp_ping, nmsh_ping,
                    nsp_ping, color_ping]
        no_message_list = [login_no_ping, nms_no_ping, nmt_no_ping,
                    nmp_no_ping, nmsh_no_ping, nsp_no_ping, color_no_ping]
    nerds_message_list = [nerds_login_ping, nerds_nmt_ping, nerds_nmsh_ping,
                          nerds_nsp_ping, nerds_color_ping]

    for x in no_message_list:
        temp_no_message += x[0] 
    for ping in message_list:
        if len(ping) != 1:
            for ids in ping:
                message += ids
                if len(message) > 1800:
                    await target_channel.send(message)
                    message = ''
                    len_check += 1
    if len(message) < 1800:
        message += color_message_temp
        await target_channel.send(message)

    await target_channel.send(reminder)
    for ping in nerds_message_list:
        if len(ping) != 1:
            for ids in ping:
                nerds_message += ids
                if len(message) > 1800:
                    await disc_channel.send(nerds_message)
                    nerds_message = ''
                    len_check += 1
    if len(nerds_message) < 1800:
        await disc_channel.send(nerds_message)

    for ping in no_message_list:
        if len(ping) != 1:
            for ids in ping:
                no_message += f'{ids}\n'
                if len(no_message) > 1800:
                    await disc_channel.send(no_message)
                    no_message = ''
                    len_check += 1  
    if len(no_message) < 1800:
        if no_message != no_temp:
            await disc_channel.send(no_message)
    
    
#    for ping in no_message_list:
#        if ping == login_temp or ping == nms_temp or ping == nmt_temp \
#        or ping == nmp_temp or ping == nmsh_temp or ping == nsp_temp \
#        or ping == color_temp or ping == None:
#            continue
#        else:
#            if ping == login_temp:
#                number /= 1440
#                number *= 2
#                
#                msg = f'''
#                My data sources have shown that you haven't logged in for at least {str(number)} days.
#                failure to login before 7 days inactive, will result in being set as an applicant
#                and eventually, removal from the alliance.
#                '''
#            for user_id in ping:
#                user = await client.fetch_user(user_id)
#                msg = f''
#                channel = client.get_channel(946196124614664212)
#                try:
#                    await DMChannel.send(user, msg)
#                    await channel.send(f':white_check_mark: {user.mention} has been DMed')
#                    time.sleep(4)
#                except:
#                    await channel.send(':x: Message failed to send, I might be blocked by <@{user_id}>')
#                    time.sleep(1)

#        embed = discord.Embed(title = 'Trainee units and inactivity status.',
#                          description = '', color=colors.dark_gold)
#        embed.add_field(name = nerds_login_temp,
#                        value = str(nerds_login_ping),
#                        inline = False)
#        embed.add_field(name = nerds_nsp_temp,
#                        value = str(nerds_nsp_ping),
#                        inline = False)
#        # embed.add_field(name = nerds_nms_temp,
#        #                 value = nerds_nms_ping,
#        #                 inline = False)
#        embed.add_field(name = str(nerds_nmt_temp),
#                        value = str(nerds_nmt_ping),
#                        inline = False)
#        embed.add_field(name = nerds_nmsh_temp,
#                        value = str(nerds_nmsh_ping),
#                        inline = False)
#        # embed.add_field(name = nerds_nmp_temp,
#        #                 value = nerds_nmp_ping,
#        #                 inline = False)
#        embed.add_field(name = nerds_color_temp,
#                        value = str(nerds_color_ping),
#                        inline = False)
#        await disc_channel.send(embed=embed)
#        
#        
#        a = 0
#        embed = discord.Embed(title = no_temp,
#                          description = '', color=colors.dark_gold)
#        if login_no_ping:
#            embed.add_field(name = str(login_temp),
#                            value = str(login_no_ping),
#                            inline = False)
#            a = 1
#        if nsp_no_ping:
#            embed.add_field(name = str(nsp_temp),
#                            value = str(nsp_no_ping),
#                            inline = False)
#            a = 1
#        if nms_no_ping:
#            embed.add_field(name = str(nms_temp),
#                            value = str(nms_no_ping),
#                            inline = False)
#            a = 1
#        if nmt_no_ping:
#            embed.add_field(name = str(nmt_temp),
#                            value = str(nmt_no_ping),
#                            inline = False)
#            a = 1
#        if nmsh_no_ping:
#            embed.add_field(name = str(nmsh_temp),
#                            value = str(nmsh_no_ping),
#                            inline = False)
#            a = 1
#        if nmp_no_ping:
#            embed.add_field(name = str(nmp_temp),
#                            value = str(nmp_no_ping),
#                            inline = False)
#            a = 1
#        if color_no_ping:
#            embed.add_field(name = str(color_temp),
#                            value = str(color_no_ping),
#                            inline = False)
#            a = 1
#        if a == 1:
#            await disc_channel.send(embed=embed)

    OversightData.data_storage(memberdata)
    print('Daily end!')

# initializing scheduler
scheduler = AsyncIOScheduler(
    job_defaults={'misfire_grace_time': 3600})

# runs daily coroutine at 15 mins after default update
scheduler.add_job(daily,
                  CronTrigger(timezone=utc, hour='0', minute='15'),
                  misfire_grace_time=3600)

# starting the scheduler
scheduler.start()

@client.command(name='mandaily', help='+mandaily')
@commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim')
async def mandaily(ctx):
    if ctx.channel.name == 'oversight-nagging' or \
    ctx.channel.name == 'disciplinarians' and ctx.channel.category.name \
            != '[The Harbour]':
        await daily()


@client.listen('on_command_error')
async def on_error(ctx, error):
    # Allows us to check for original exceptions raised and sent to CommandInvokeError.
    # If nothing is found. We keep the exception passed to on_command_error.
    error = getattr(error, 'original', error)


    if isinstance(error, commands.DisabledCommand):
        await ctx.send(f'{ctx.command} has been disabled.')

    elif isinstance(error, commands.NoPrivateMessage):
        try:
            await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
        except discord.HTTPException:
            pass

    if isinstance(error, MissingAnyRole):
        await ctx.send(
            'You do not have the necessary permissions to use this command')
    elif isinstance(error, CommandOnCooldown):
        await ctx.send(f'That command is on cooldown. Try again in {error.retry_after:,.2f} secs.')
    elif isinstance(error, MissingRequiredArgument):
        await ctx.send('One or more required arguments are missing')
    elif isinstance(error, commands.CheckFailure):
           await ctx.send('You do not have the necessary permissions to use this command.')
           return
    else:
        # All other Errors not returned come here. And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

client.run(token)
