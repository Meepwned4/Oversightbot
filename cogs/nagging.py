import discord
import requests
from discord.ext import commands
from discord import DMChannel
import pickle
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

class nagging(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(name='DM', help='+DM test', aliases=['dm'])
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim')
    async def DM(self, ctx, user_id, *, msg):
        client = self.client
        user = await client.fetch_user(user_id)
        try:
            await DMChannel.send(user, msg)
            await ctx.send(f':white_check_mark: Your Message has been sent')
        except:
            await ctx.send(':x: Message failed to send, I might have been blocked')

#    @commands.command(name='temp', help='+temp')
#    @commands.is_owner()
#    async def temp(self, ctx):
#        if ctx.channel.name == 'oversight-nagging' or \
#        ctx.channel.name == 'disciplinarians' and ctx.channel.category.name \
#                != '[The Harbour]':
#                    test = requests.get(
#        'http://24.117.204.187:8080/discord/?disc_id=800760164680204340' +
#        '&key=davethsmellskrampuswhales')
#                    test = test.json()

    @commands.command(name='ping', help='+ping')
    @commands.is_owner()
    async def ping(self,ctx):
        client = self.client
        if ctx.channel.name == 'oversight-nagging' or \
        ctx.channel.name == 'disciplinarians' and ctx.channel.category.name \
                != '[The Harbour]':
            channel_id = 946196124614664212
            channel = client.get_channel(channel_id)
            await channel.send(file=discord.File('./assets/ping.gif'))
#            await channel.send('<@730268552149336107> <@735199419045249099> Get pinged nerds.')
#            await channel.send('<@734551328184991845> You da best.')

    @commands.command(name='reset')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim')
    async def reset(self, ctx):
        if ctx.channel.name == 'oversight-nagging' or \
        ctx.channel.name == 'disciplinarians' and ctx.channel.category.name \
                != '[The Harbour]':
                    oldmemberdata = []
                    oldmemberdata = OversightData.data_retrieval(oldmemberdata)
                    fetcheddata = requests.get(
                            'https://politicsandwar.com/api/alliance-members/' +
                            '?allianceid=5049&key=' + apikey)
                    fetcheddata = fetcheddata.json()
                    memberdata = fetcheddata.get(['nations'][0])
                    list_of_dics = requests.get(
                        'http://24.117.204.187:8080/discord/?alliance=5049' +
                        '&key=davethsmellskrampuswhales')
                    list_of_dics = list_of_dics.json()
                    memberdata = OversightData.merge_memberdata(memberdata, oldmemberdata, list_of_dics)
                    for dic in memberdata:
                        ping_dic = dic.get('ping')
                        for k in ping_dic:
                            ping_dic.update({k: 0})
                    OversightData.data_storage(memberdata)
                    reset_message = 'Reset ping counter for everyone'
                    await ctx.send(reset_message)

    @commands.command(name='war_status', help='+war_status True')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim')
    async def war_status(self, ctx, status: typing.Optional[str] = 'False'):
         if ctx.channel.category.name != '[The Harbour]' and \
         ctx.channel.category.name != '[Discussion]':
             if status != 'True' and status != 'true' and \
             status != 'False' and status != 'false' and \
             status != '1' and status != '0':
                 await ctx.send('Invalid input, must be True or False.')
             else:
                 oldmemberdata = []
                 oldmemberdata = OversightData.data_retrieval(oldmemberdata)
                 if status == 'True' or status == 'true' or status == '1':
                     status = '1'
                 else:
                     status = '0'
                 for nation in oldmemberdata:
                     nation.update({'war_status':status})
                 OversightData.data_storage(oldmemberdata)
                 if status == '1':
                     await ctx.send('War status set to true')
                 if status == '0':
                     await ctx.send('War status set to false')

    @commands.command(name='mmr_set', help='+mmr_set 0350')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim')
    async def mmr_set(self, ctx, mmr, mmr2: typing.Optional[str] = '10',
                      all_check: typing.Optional[str] = '5051'):
         if ctx.channel.category.name != '[The Harbour]' and \
         ctx.channel.category.name != '[Discussion]':
                    mmr = mmr + ' ' + all_check
                    pickling_on = open('./data/mmr.pickle', 'wb')
                    pickle.dump(mmr, pickling_on)
                    pickling_on.close()

                    #pickle_off = open('./data/mmr.pickle', 'rb')
                    #mmr = pickle.load(pickle_off)
                    await ctx.send('MMR locked and loaded')

    @commands.command(name='inactive', help='+inactive 3 days')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'DisC')
    async def inactive(self, ctx, number: float, time):
        client = self.client
        if ctx.channel.name == 'oversight-nagging' or \
        ctx.channel.name == 'disciplinarians' and ctx.channel.category.name \
                != '[The Harbour]':
            if number < 1 and number >= 0:
                await ctx.send('ERROR: numbers below 1 not allowed')
            elif number < 0:
                await ctx.send('ERROR: Negative numbers not allowed')

            else:
    #            disc_channel = client.get_channel(disc_channel_id)
                server = client.get_guild(carthago_server_id)
                nerds_list = []

                for member in server.members:
                    for role in member.roles:
                        if role.name == 'Trainee':
                            nerds_list.append(str(member.id))
                fetcheddata = requests.get(
                    'https://politicsandwar.com/api/alliance-members/' +
                    '?allianceid=5049&key=' + apikey)
                fetcheddata = fetcheddata.json()
                memberdata = fetcheddata.get(['nations'][0])
                list_of_dics = requests.get(
                    'http://24.117.204.187:8080/discord/?alliance=5049' +
                    '&key=davethsmellskrampuswhales')
                list_of_dics = list_of_dics.json()
                inactivenations = []
                duplicate_ping_check = []
                login_temp = '__People who have been inactive for more than ' \
                    + str(number) + f' {time}:__\n'
                nerds_login_temp = '__Trainees who have been inactive for more than ' \
                + str(number) + f' {time}:__\n'
                login_ping = ''
                nerds_login_ping = ''
                if 'day' == time:
                    number *= 1440
                elif 'days' == time:
                    number *= 1440
                elif 'week' == time:
                    number *= 10080
                elif 'weeks' == time:
                    number *= 10080
    #            elif 'hour' == time:
    #                number *= 60
    #            elif 'hours' == time:
    #                number *= 60
                #        elif 'minutes' == time:
                #            number = number
                #        elif 'minute' == time:
                #            number = number
                else:
                    await ctx.send('Invalid specified time')

                for dic1 in memberdata:
                    for key, val in dic1.items():
                        if key == 'minutessinceactive':
                            if val >= number and dic1.get('vacmode') == '0':
                                b = dic1.get('nationid')
                                inactivenations.append(b)
                if not inactivenations:
                    login_ping = 'Everyone has logged in within that time.'
                for dic2 in list_of_dics:
                    if dic2.get('_id') in duplicate_ping_check:
                        continue
                    elif dic2.get('_id') in inactivenations:
                        c = dic2.get('disc_id')
                        c = str(c)
                        if c in nerds_list:
                            duplicate_ping_check.append(c)
                            nerds_login_ping = nerds_login_ping + \
                                '<@' + c + '>' + ' '
                        else:
                            duplicate_ping_check.append(c)
                            login_ping = login_ping + '<@' + c + '>' + ' '
                login_ping = login_temp + login_ping
                nerds_login_ping = nerds_login_temp + nerds_login_ping
                await ctx.send(login_ping)
                await ctx.send(nerds_login_ping)
    #            await disc_channel.send(nerds_login_ping)


    @commands.command(name='nsp', help='+nsp')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'DisC')
    async def nsp(self, ctx):
        client = self.client
        if ctx.channel.name == 'oversight-nagging' or \
        ctx.channel.name == 'disciplinarians' and ctx.channel.category.name \
                != '[The Harbour]':
            fetcheddata = requests.get(
                'https://politicsandwar.com/api/alliance-members/' +
                '?allianceid=5049&key=' + apikey)
            fetcheddata = fetcheddata.json()
            memberdata = fetcheddata.get(['nations'][0])
            list_of_dics = requests.get(
                'http://24.117.204.187:8080/discord/?alliance=5049' +
                '&key=davethsmellskrampuswhales')
            list_of_dics = list_of_dics.json()
            disc_channel = client.get_channel(disc_channel_id)
            server = client.get_guild(carthago_server_id)
            pickle_off = open('./data/spiesoldmemory.pickle', 'rb')
            spiesoldmemory = pickle.load(pickle_off)
            spiesnewmemory = {}
            nationids = []
            nerds_list = []
            for member in server.members:
                for role in member.roles:
                    if role.name == 'Trainee':
                        nerds_list.append(str(member.id))
            nsp_temp = '__People who don\'t have max spies:__\n'
            nsp_ping = ''
            nerds_nsp_temp = '__Trainees who don\'t have max spies:__\n'
            nerds_nsp_ping = ''

            for dic1 in memberdata:
                if int(dic1.get('intagncy')):
                    if int(dic1.get('spies')) != 60 and dic1.get('vacmode') == '0':
                        b = dic1.get('nationid')
                        nationids.append(b)
                if not int(dic1.get('intagncy')):
                    if int(dic1.get('spies')) != 50 and dic1.get('vacmode') == '0':
                        b = dic1.get('nationid')
                        nationids.append(b)
            for dic2 in list_of_dics:
                for dic in memberdata:
                    if dic.get('nationid') == dic2.get('_id'):
                        spiesnewmemory[dic.get('leader')] = int(dic.get('spies'))
                        if dic.get('nationid') in nationids:
                            if not spiesoldmemory.get(dic.get('leader')):
                                continue
                            if spiesnewmemory.get(dic.get(
                                    'leader')) <= spiesoldmemory.get(dic.get(
                                        'leader')):
                                c = dic2.get('disc_id')
                                c = str(c)
                                if c in nerds_list:
                                    nerds_nsp_ping = nerds_nsp_ping + \
                                        '<@' + c + '>' + ' '
                                else:
                                    nsp_ping = nsp_ping + '<@' + c + '>' + ' '
            if not nsp_ping:
                nsp_ping = 'Everyone has max spies.'
            nsp_ping = nsp_temp + nsp_ping
            if not nerds_nsp_ping:
                nerds_nsp_ping = 'Everyone has max spies.'
            nerds_nsp_ping = nerds_nsp_temp + nerds_nsp_ping
            pickling_on = open('./data/spiesoldmemory.pickle', 'wb')
            pickle.dump(spiesnewmemory, pickling_on)
            pickling_on.close()
            await ctx.send(nsp_ping)
            await disc_channel.send(nerds_nsp_ping)


    @commands.command(name='nmp', help='+nmp')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'DisC')
    async def nmp(self, ctx):
        client = self.client
        if ctx.channel.name == 'oversight-nagging' or \
        ctx.channel.name == 'disciplinarians' and ctx.channel.category.name \
                != '[The Harbour]':
            fetcheddata = requests.get(
                'https://politicsandwar.com/api/alliance-members/' +
                '?allianceid=5049&key=' + apikey)
            fetcheddata = fetcheddata.json()
            memberdata = fetcheddata.get(['nations'][0])
            list_of_dics = requests.get(
                'http://24.117.204.187:8080/discord/?alliance=5049' +
                '&key=davethsmellskrampuswhales')
            list_of_dics = list_of_dics.json()
            disc_channel = client.get_channel(disc_channel_id)
            server = client.get_guild(carthago_server_id)
            pickle_off = open('./data/planesoldmemory.pickle', 'rb')
            planesoldmemory = pickle.load(pickle_off)
            pickle_off = open('./data/mmr.pickle', 'rb')
            mmr = pickle.load(pickle_off)
            all_check = mmr.split('-')
            nerds_list = []
            if all_check[1] != 'all' and all_check[1] == '':
                for member in server.members:
                    for role in member.roles:
                        if role.name == 'Trainee':
                            nerds_list.append(str(member.id))
            nationids = []
            nmp_temp = '__People who don\'t have max planes__\n'
            nmp_ping = ''
            nerds_nmp_temp = '__Trainees who don\'t have max planes__\n'
            nerds_nmp_ping = ''
            planesnewmemory = {}

            for dic in memberdata:
                plane_mmr = int(dic.get('cities') * int(mmr[2]) * 15)
                if plane_mmr > int(dic.get('aircraft')) and \
                    dic.get('vacmode') == '0':
                    b = dic.get('nationid')
                    nationids.append(b)
            for dic2 in list_of_dics:
                for dic in memberdata:
                    if dic.get('nationid') == dic2.get('_id'):
                        planesnewmemory[dic.get('leader')] = int(dic.get(
                            'aircraft'))
                        if dic.get('nationid') in nationids:
                            if not planesoldmemory.get(dic.get('leader')):
                                continue
                            elif planesnewmemory.get(
                                    dic.get('leader')) <= planesoldmemory.get(
                                        dic.get('leader')):
                                c = dic2.get('disc_id')
                                c = str(c)
                                if c in nerds_list:
                                    nerds_nmp_ping = nerds_nmp_ping + \
                                        '<@' + c + '>' + ' '
                                else:
                                    nmp_ping = nmp_ping + '<@' + c + '>' + ' '

            if not nmp_ping:
                nmp_ping = 'Everyone has max planes.'
            nmp_ping = nmp_temp + nmp_ping
            if not nerds_nmp_ping:
                nerds_nmp_ping = 'Everyone has max planes.'
            nerds_nmp_ping = nerds_nmp_temp + nerds_nmp_ping
            pickling_on = open('./data/planesoldmemory.pickle', 'wb')
            pickle.dump(planesnewmemory, pickling_on)
            pickling_on.close()
            await ctx.send(nmp_ping)
            await disc_channel.send(nerds_nmp_ping)


    @commands.command(name='nmt', help='+nmt')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'DisC')
    async def nmt(self, ctx):
        client = self.client
        if ctx.channel.name == 'oversight-nagging' or \
        ctx.channel.name == 'disciplinarians' and ctx.channel.category.name \
                != '[The Harbour]':
            fetcheddata = requests.get(
                'https://politicsandwar.com/api/alliance-members/' +
                '?allianceid=5049&key=' + apikey)
            fetcheddata = fetcheddata.json()
            memberdata = fetcheddata.get(['nations'][0])
            list_of_dics = requests.get(
                'http://24.117.204.187:8080/discord/?alliance=5049' +
                '&key=davethsmellskrampuswhales')
            list_of_dics = list_of_dics.json()
            disc_channel = client.get_channel(disc_channel_id)
            server = client.get_guild(carthago_server_id)
            pickle_off = open('./data/mmr.pickle', 'rb')
            mmr = pickle.load(pickle_off)
            all_check = mmr.split('-')
            nerds_list = []
            if all_check[1] != 'all' and all_check[1] == '':
                for member in server.members:
                    for role in member.roles:
                        if role.name == 'Trainee':
                            nerds_list.append(str(member.id))
            pickle_off = open('./data/tankoldmemory.pickle', 'rb')
            tankoldmemory = pickle.load(pickle_off)
            nationids = []
            nmt_temp = '__People who don\'t have max tanks__\n'
            nmt_ping = ''
            nerds_nmt_temp = '__Trainees who don\'t have max tanks__\n'
            nerds_nmt_ping = ''
            tanknewmemory = {}

            for dic in memberdata:
                tank_mmr = int(dic.get('cities') * int(mmr[1]) * 250)
                if tank_mmr > int(dic.get('tanks')) and \
                    dic.get('vacmode') == '0':
                    b = dic.get('nationid')
                    nationids.append(b)
            for dic2 in list_of_dics:
                for dic in memberdata:
                    if dic.get('nationid') == dic2.get('_id'):
                        tanknewmemory[dic.get('leader')] = int(dic.get(
                            'tanks'))
                        if dic.get('nationid') in nationids:
                            if tanknewmemory.get(
                                    dic.get('leader')) <= tankoldmemory.get(
                                        dic.get('leader')):
                                c = dic2.get('disc_id')
                                c = str(c)
                                if c in nerds_list:
                                    nerds_nmt_ping = nerds_nmt_ping + \
                                        '<@' + c + '>' + ' '
                                else:
                                    nmt_ping = nmt_ping + '<@' + c + '>' + ' '
            if not nmt_ping:
                nmt_ping = 'Everyone has max tanks.'
            nmt_ping = nmt_temp + nmt_ping
            if not nerds_nmt_ping:
                nerds_nmt_ping = 'Everyone has max tanks.'
            nerds_nmt_ping = nerds_nmt_temp + nerds_nmt_ping
            pickling_on = open('./data/tankoldmemory.pickle', 'wb')
            pickle.dump(tanknewmemory, pickling_on)
            pickling_on.close()
            await ctx.send(nmt_ping)
            await disc_channel.send(nerds_nmt_ping)


    @commands.command(name='nms', help='+nms')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'DisC')
    async def nms(self, ctx):
        client = self.client
        if ctx.channel.name == 'oversight-nagging' or \
        ctx.channel.name == 'disciplinarians' and ctx.channel.category.name \
                != '[The Harbour]':
            fetcheddata = requests.get(
                'https://politicsandwar.com/api/alliance-members/' +
                '?allianceid=5049&key=' + apikey)
            fetcheddata = fetcheddata.json()
            memberdata = fetcheddata.get(['nations'][0])
            list_of_dics = requests.get(
                'http://24.117.204.187:8080/discord/?alliance=5049' +
                '&key=davethsmellskrampuswhales')
            list_of_dics = list_of_dics.json()
            disc_channel = client.get_channel(disc_channel_id)
            server = client.get_guild(carthago_server_id)
            pickle_off = open('./data/mmr.pickle', 'rb')
            mmr = pickle.load(pickle_off)
            all_check = mmr.split('-')
            nerds_list = []
            if all_check[1] != 'all' and all_check[1] == '':
                for member in server.members:
                    for role in member.roles:
                        if role.name == 'Trainee':
                            nerds_list.append(str(member.id))
            pickle_off = open('./data/soldieroldmemory.pickle', 'rb')
            soldieroldmemory = pickle.load(pickle_off)
            nationids = []
            nms_temp = '__People who don\'t have max soldiers__\n'
            nms_ping = ''
            nerds_nms_temp = '__Trainees who don\'t have max soldiers__\n'
            nerds_nms_ping = ''
            soldiernewmemory = {}

            for dic in memberdata:
                soldier_mmr = int(dic.get('cities') * int(mmr[0]) * 3000)
                if soldier_mmr > int(dic.get('soldiers')) and \
                    dic.get('vacmode') == '0':
                    b = dic.get('nationid')
                    nationids.append(b)
            for dic2 in list_of_dics:
                for dic in memberdata:
                    if dic.get('nationid') == dic2.get('_id'):
                        soldiernewmemory[dic.get('leader')] = int(dic.get(
                            'soldiers'))
                        if dic.get('nationid') in nationids:
                            if not soldieroldmemory.get(dic.get('leader')):
                                continue
                            elif soldiernewmemory.get(
                                    dic.get('leader')) <= soldieroldmemory.get(
                                        dic.get('leader')):
                                c = dic2.get('disc_id')
                                c = str(c)
                                if c in nerds_list:
                                    nerds_nms_ping = nerds_nms_ping + \
                                        '<@' + c + '>' + ' '
                                else:
                                    nms_ping = nms_ping + '<@' + c + '>' + ' '
            if not nms_ping:
                nms_ping = 'Everyone has max soldiers.'
            nms_ping = nms_temp + nms_ping
            if not nerds_nms_ping:
                nerds_nms_ping = 'Everyone has max soldiers.'
            nerds_nms_ping = nerds_nms_temp + nerds_nms_ping
            pickling_on = open('./data/soldieroldmemory.pickle', 'wb')
            pickle.dump(soldiernewmemory, pickling_on)
            pickling_on.close()
            await ctx.send(nms_ping)
            await disc_channel.send(nerds_nms_ping)


    @commands.command(name='nmsh', help='+nmsh')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'DisC')
    async def nmsh(self, ctx):
        client = self.client
        if ctx.channel.name == 'oversight-nagging' or \
        ctx.channel.name == 'disciplinarians' and ctx.channel.category.name \
                != '[The Harbour]':
            fetcheddata = requests.get(
                'https://politicsandwar.com/api/alliance-members/' +
                '?allianceid=5049&key=' + apikey)
            fetcheddata = fetcheddata.json()
            memberdata = fetcheddata.get(['nations'][0])
            list_of_dics = requests.get(
                'http://24.117.204.187:8080/discord/?alliance=5049' +
                '&key=davethsmellskrampuswhales')
            list_of_dics = list_of_dics.json()
            disc_channel = client.get_channel(disc_channel_id)
            server = client.get_guild(carthago_server_id)
            pickle_off = open('./data/mmr.pickle', 'rb')
            mmr = pickle.load(pickle_off)
            all_check = mmr.split('-')
            nerds_list = []
            if all_check[1] != 'all' and all_check[1] == '':
                for member in server.members:
                    for role in member.roles:
                        if role.name == 'Trainee':
                            nerds_list.append(str(member.id))
            pickle_off = open('./data/shipoldmemory.pickle', 'rb')
            shipoldmemory = pickle.load(pickle_off)
            nationids = []
            nmsh_temp = '__People who don\'t have max ships__\n'
            nmsh_ping = ''
            nerds_nmsh_temp = '__Trainees who don\'t have max ships__\n'
            nerds_nmsh_ping = ''
            shipnewmemory = {}

            for dic in memberdata:
                ship_mmr = int(dic.get('cities') * int(mmr[3]) * 5)
                if ship_mmr > int(dic.get('ships')) and \
                    dic.get('vacmode') == '0':
                    b = dic.get('nationid')
                    nationids.append(b)
            for dic2 in list_of_dics:
                for dic in memberdata:
                    if dic.get('nationid') == dic2.get('_id'):
                        shipnewmemory[dic.get('leader')] = int(dic.get(
                            'ships'))
                        if dic.get('nationid') in nationids:
                            if not shipoldmemory.get(dic.get('leader')):
                                continue
                            elif shipnewmemory.get(
                                    dic.get('leader')) <= shipoldmemory.get(
                                        dic.get('leader')):
                                c = dic2.get('disc_id')
                                c = str(c)
                                if c in nerds_list:
                                    nerds_nmsh_ping = nerds_nmsh_ping + \
                                        '<@' + c + '>' + ' '
                                else:
                                    nmsh_ping = nmsh_ping + '<@' + c + '>' + ' '
            if not nmsh_ping:
                nmsh_ping = 'Everyone has max ships.'
            nmsh_ping = nmsh_temp + nmsh_ping
            if not nerds_nmsh_ping:
                nerds_nmsh_ping = 'Everyone has max ships.'
            nerds_nmsh_ping = nerds_nmsh_temp + nerds_nmsh_ping
            pickling_on = open('./data/shipoldmemory.pickle', 'wb')
            pickle.dump(shipnewmemory, pickling_on)
            pickling_on.close()
            await ctx.send(nmsh_ping)
            await disc_channel.send(nerds_nmsh_ping)


    @commands.command(name='color', help='+color')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'DisC')
    async def color(self, ctx):
        client = self.client
        if ctx.channel.name == 'oversight-nagging' or \
        ctx.channel.name == 'disciplinarians' and ctx.channel.category.name \
                != '[The Harbour]':
            fetcheddata = requests.get(
                'https://politicsandwar.com/api/alliance-members/' +
                '?allianceid=5049&key=' + apikey)
            fetcheddata = fetcheddata.json()
            memberdata = fetcheddata.get(['nations'][0])
            list_of_dics = requests.get(
                'http://24.117.204.187:8080/discord/?alliance=5049' +
                '&key=davethsmellskrampuswhales')
            list_of_dics = list_of_dics.json()
            disc_channel = client.get_channel(disc_channel_id)
            server = client.get_guild(carthago_server_id)
            nerds_list = []
            for member in server.members:
                for role in member.roles:
                    if role.name == 'Trainee':
                        nerds_list.append(str(member.id))
            nationids = []
            fetcheddata = requests.get(
                'https://politicsandwar.com/api/alliance/id=5049&key=id=5049&key='
                + apikey)
            fetcheddata = fetcheddata.json()
            color_temp = '__People not on the nation color ' + fetcheddata.get(
                'color') + ':__\n'
            nerds_color_temp = '__Trainees not on the nation color ' + \
                fetcheddata.get('color') + ':__\n'
            color_ping = ''
            nerds_color_ping = ''
            for dic1 in memberdata:
                for key, val in dic1.items():
                    if key == 'color':
                        if val != fetcheddata.get('color') and val != 'beige' \
                            and dic1.get('vacmode') == '0':
                            b = dic1.get('nationid')
                            nationids.append(b)
            for dic2 in list_of_dics:
                if dic2.get('_id') in nationids:
                    c = dic2.get('disc_id')
                    c = str(c)
                    if c in nerds_list:
                        nerds_color_ping = nerds_color_ping + \
                                    '<@' + c + '>' + ' '
                    else:
                        color_ping = color_ping + '<@' + c + '>' + ' '
            if not nationids:
                color_ping = 'Everyone is on the correct color.'
            color_ping = color_temp + color_ping
            if not nerds_color_ping:
                nerds_color_ping = 'Everyone is on the correct color.'
            nerds_color_ping = nerds_color_temp + nerds_color_ping
            await ctx.send(color_ping)
            await disc_channel.send(nerds_color_ping)



    @commands.command(name='timer', help='+timer (nationid)')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim',
                           'Senator', 'Citizen')
    async def timer(self, ctx, nation):
        if ctx.channel.category.name != '[The Harbour]':
            fetcheddata = requests.get(
                'http://politicsandwar.com/api/alliance-members/'
                '?allianceid=5049&key=' + apikey)
            fetcheddata = fetcheddata.json()
            memberdata = fetcheddata.get(['nations'][0])
            list_of_dics = requests.get(
                'http://159.118.147.210:8080/discord/?alliance=5049' +
                '&key=davethsmellskrampuswhales')
            list_of_dics = list_of_dics.json()
            for dic1 in list_of_dics:
                for dic2 in memberdata:
                    if dic2.get('nationid') == int(
                            nation) and str(dic1.get('_id')) == nation:
                        citytimer = int(dic2.get('turns_since_last_city'))
                        citytimer = 120 - citytimer
                        projecttimer = int(dic2.get('turns_since_last_project'))
                        projecttimer = 120 - projecttimer
                        # 120 turns(10 days)
                        cityhour = citytimer * 2
                        projecthour = projecttimer * 2
                        leader = dic1.get('leader')
                        break
            if dic2.get('cities') <= 10:
                await ctx.send(leader + ' has ' + ' 0 ' + ' turns(' +
                    ' 0 ' + ' hours) left before they can buy a city.')
                if projecttimer > 0:
                    await ctx.send(leader + ' has ' + str(
                        projecttimer) + ' turns(' +
                            str(projecthour) +
                            ' hours) left before they can buy a project.')
                elif projecttimer < 0:
                    await ctx.send(leader + ' has ' + ' 0 ' + ' turns(' +
                            ' 0 ' + ' hours) left before they can buy a project.')

            elif citytimer > 0:
                await ctx.send(leader + ' has ' + str(
                    citytimer) + ' turns(' +
                        str(cityhour) +
                        ' hours) left before they can buy a city.')
            elif citytimer < 0:
                await ctx.send(leader + ' has ' + ' 0 ' + ' turns(' +
                    ' 0 ' + ' hours) left before they can buy a city.')
            elif projecttimer > 0:
                await ctx.send(leader + ' has ' + str(
                    projecttimer) + ' turns(' +
                        str(projecthour) +
                        ' hours) left before they can buy a project.')
            elif projecttimer < 0:
                await ctx.send(leader + ' has ' + ' 0 ' + ' turns(' +
                        ' 0 ' + ' hours) left before they can buy a project.')

    @commands.command(name='mmr_check', help='+mmr_check 5553')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim')
    async def mmr_check(self, ctx, mmr, ping: typing.Optional[str] = '-pingfalse'):
        if ctx.channel.name == 'oversight-nagging' or \
        ctx.channel.name == 'disciplinarians' and ctx.channel.category.name \
                != '[The Harbour]':
            nationids = []
            fetcheddata = requests.get(
                'https://politicsandwar.com/api/alliance-members/' +
                '?allianceid=5049&key=' + apikey)
            fetcheddata = fetcheddata.json()
            memberdata = fetcheddata.get(['nations'][0])
            list_of_dics = requests.get(
                'http://24.117.204.187:8080/discord/?alliance' +
                '=5049&key=davethsmellskrampuswhales')
            list_of_dics = list_of_dics.json()
            mmr_message = ''
            soldiers_max = ''
            tanks_max = ''
            planes_max = ''
            ships_max = ''
            b = ''
            x = 0
            dup_check = []
            message = f'__People who don\'t meet MMR({mmr}):__\n'

            for dic in memberdata:
                soldiers_max = int(dic.get('cities') * int(mmr[0]) * 3000)
                tanks_max = int(dic.get('cities') * int(mmr[1]) * 250)
                planes_max = int(dic.get('cities') * int(mmr[2]) * 15)
                ships_max = int(dic.get('cities') * int(mmr[3]) * 5)
                if dic.get('cities') * int(mmr[0]) * 3000 > \
                        int(dic.get('soldiers')):
                    b = dic.get('nationid')
                    if b not in nationids:
                        nationids.append(str(b))
                    elif b in nationids:
                        continue
                if dic.get('cities') * int(mmr[1]) * 250 > \
                        int(dic.get('tanks')):
                    nationids.append(str(b))
                    if b not in nationids:
                        nationids.append(str(b))
                    elif b in nationids:
                        continue
                if dic.get('cities') * int(mmr[2]) * 15 > \
                        int(dic.get('aircraft')):
                    b = dic.get('nationid')
                    if b not in nationids:
                        nationids.append(str(b))
                    elif b in nationids:
                        continue
                if dic.get('cities') * (int(mmr[3]) * 5) > \
                        int(dic.get('ships')):
                    b = dic.get('nationid')
                    if b not in nationids:
                        nationids.append(str(b))
                    elif b in nationids:
                        continue
                if b in nationids:
                    if dup_check:
                        if dic.get('nationid') in dup_check:
                            continue
                if not nationids:
                    continue
                if ping == '-pingtrue':
                    if len(mmr_message) > 1800:
                        await ctx.send(mmr_message)
                        mmr_message = ''
                        len_check = 1
                    if dic.get('nationid') in dup_check or dic.get('vacmode') != \
                        '0':
                        continue
                    for natid in nationids:
                        if x != 0:
                            break
                        for dic2 in list_of_dics:
                            if str(dic2.get('_id')) not in natid:
                                if x == 0:
                                    x += 1
                                    await ctx.send('Everyone meets or exceeds ' + \
                                                   f'{mmr} MMR')
                            if str(dic2.get('_id')) == str(dic.get('nationid')):
                                c = dic2.get('disc_id')
                                c = str(c)
                                mmr_message = mmr_message + '<@' + c + '>' + \
                                ' ' + 'soldiers: ' + str(dic.get(
                                'soldiers')) + '/' + str(soldiers_max) + ' ' \
                                + 'tanks: ' + str(dic.get('tanks')) + '/' + \
                                str(tanks_max) + ' ' + 'planes: ' + str(
                                dic.get('aircraft')) + '/' + str(planes_max) \
                                + ' ' + 'ships: ' + str(dic.get('ships')) + \
                                '/' + str(ships_max) + '\n'
                                dup_check.append(dic.get('nationid'))
                else:
                    if len(mmr_message) > 1800:
                        await ctx.send(mmr_message)
                        mmr_message = ''
                        len_check = 1
                    mmr_message = mmr_message + '**' + str(dic.get('nation')) + \
                        ':** ' + 'soldiers: ' + str(dic.get('soldiers')) + '/' + \
                        str(soldiers_max) + ' ' + 'tanks: ' + \
                        str(dic.get('tanks')) + '/' + str(tanks_max) + ' ' + \
                        'planes: ' + str(dic.get('aircraft')) + '/' + \
                        str(planes_max) + ' ' + 'ships: ' + \
                        str(dic.get('ships')) + '/' + str(ships_max) + '\n'
                    dup_check.append(dic.get('nationid'))
            if len_check == 0:
                mmr_message = message + mmr_message
            await ctx.send(mmr_message)


async def setup(client):
	await client.add_cog(nagging(client))