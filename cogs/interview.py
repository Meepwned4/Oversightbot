import discord
import os
from discord.ext import commands
import json
import typing
import nest_asyncio
nest_asyncio.apply()
import requests
import random
import pickle
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

pickle_off = open('./data/token.pickle', 'rb')
token = pickle.load(pickle_off)
oversight_channel_id = 812131124489879552
disc_channel_id = 605910228692893726
test_oversight_channel_id = 736099358344478764
test_disc_channel_id = 834653321099739177
carthago_server_id = 567336454632636416
nerds_id = 712071416505172090
raider_id = 853790553375768586
guild_id_1 = 567336454632636416
guild_id_2 = 645391966598594561
trainee_role_id = 568141320011382825
suffet_role_id = 567338425443942420
elder_role_id = 567338487380967430
adirim_role_id = 752227315832062063
pentarch_role_id = 567389583289876490
trainee_role_id = 712071416505172090
foreigner_role_id = 569519945847930911
citizen_role_id = 567389586934726677
bot_role_id = 567722813335535622
information_board = 714233548332204084
information_board_2 = 876651793428414485
archive_channel = 754640623276916756
ticket_category_name = '[Admission & Training]'
interviewer_role_id = 568141320011382825
disc_role_id = 605910328613535784

right_arrow = '➡' # right arrow emoji
#robot = '🤖' # robot emoji
person = '🧑' # person emoji
interview_emoji = '📝' # interview emoji
x_emoji = '✖️' # x emoji

class interview(commands.Cog):
    def __init__(self, client):
        self.client = client
        client = self.client

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        reminder = f'If at any time you\'d like to be interviewed by a human, react with {person} \n' \
                    + f'**After** you\'ve answered, react with {right_arrow} to continue'
        client = self.client
        custom_id = interaction.data.get('custom_id')
        components = interaction.message.components
        try:
            for component in components:
                for child in component.children:
                    if child.custom_id == custom_id:
                        label = child.label
                        break
        except:
            label = 'False'
        member = interaction.user
        guild_id = interaction.guild_id
        channel_id = interaction.channel_id
        channel = interaction.channel
        category = channel.category
        message_embed = interaction.message.embeds
        author = interaction.message.author
        ignore_channels = [605910228692893726, 845685557367144448, 568822425253576739]
        embed_title = ''
        if message_embed != []:
            message_embed = message_embed[0]
            embed_title = message_embed.title
#            embed_desc = message_embed.description


        if embed_title == 'Greetings' and label == 'Apply' and author == client.user:
            if channel_id == information_board or channel_id == information_board_2:
                if guild_id == guild_id_1:
                    guild = client.get_guild(guild_id_1)
                    ticket_category = discord.utils.get(guild.categories, name=ticket_category_name)
                    interviewer_role = guild.get_role(interviewer_role_id)
                    pentarch_role = guild.get_role(pentarch_role_id)
                    disc_role = guild.get_role(disc_role_id)
                    adirim_role = guild.get_role(adirim_role_id)
                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(view_channel=False),
                        member: discord.PermissionOverwrite(view_channel=True),
                        guild.me: discord.PermissionOverwrite(view_channel=True),
                        interviewer_role: discord.PermissionOverwrite(view_channel=True),
                        pentarch_role: discord.PermissionOverwrite(view_channel=True),
                        adirim_role: discord.PermissionOverwrite(view_channel=True),
                        disc_role: discord.PermissionOverwrite(view_channel=True),
                    }
                if guild_id == guild_id_2:
                    guild = client.get_guild(guild_id_2)
                    ticket_category = discord.utils.get(guild.categories, name=ticket_category_name)
                    interviewer_role = guild.get_role(874085960885878786)
                    pentarch_role = guild.get_role(736050504089731173)
                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(view_channel=False),
                        member: discord.PermissionOverwrite(view_channel=True),
                        guild.me: discord.PermissionOverwrite(view_channel=True),
                        interviewer_role: discord.PermissionOverwrite(view_channel=True),
                        pentarch_role: discord.PermissionOverwrite(view_channel=True),
                    }


                discord_id = member.id
                dup = False
                try:
                    user = requests.get(f'http://24.117.204.187:8080/discord/?disc_id={discord_id}&key=davethsmellskrampuswhales')
                    user = user.json()
                    user = user[0]
                    nation_id = user.get('id')
                except:
                    nation_id = random.randrange(1,100)
                for ticket_channel in ticket_category.channels:
                    if ticket_channel.name == f'ticket-{nation_id}':
                        dup = True
                if dup == True:
                    await interaction.response.send_message('Can\'t create more than one ticket',ephemeral=True)
                else:
                    await interaction.response.send_message('Ticket created',ephemeral=True)
                    await ticket_category.create_text_channel(f'ticket-{nation_id}', overwrites=overwrites)
                    channel = discord.utils.get(guild.text_channels, name=f'ticket-{nation_id}')
                    await channel.edit(sync_permissions=True)
                    dic = {'channel':channel.id, 'user_id':member.id}
                    with open(f'./data/tickets/{nation_id}.json', 'w') as outfile:
                        json.dump(dic, outfile)
                    message = f'''
                    Please read and follow these instructions before you proceed with the prompt below, provided by the bot.

                    - Apply to us at: https://politicsandwar.com/alliance/join/id=5049
                    - No current in-game wars or alliance;
                    - No unsettled debt or loans;
                    - You must be active on Discord and in-game, inactivity is not acceptable;
                    - You must obey orders in a timely manner, abide by our rules and listen to your superiors, insubordination will not be tolerated.
                    - You cannot possess two or more nations/accounts in the same network. This is a grave offense that may lead to banishment.
                    '''
                    ping = f'<@{member.id}>'
                    class pre_application_buttons(discord.ui.View):
                        def __init__(self, timeout=None):
                            super().__init__()
                        @discord.ui.button(label='Start',style=discord.ButtonStyle.blurple)
                        async def start_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                            try:
                                await interaction.followup.defer()
                            except:
                                await interaction.response.defer()
                        @discord.ui.button(label='Help',style=discord.ButtonStyle.gray)
                        async def help_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                            try:
                                await interaction.followup.defer()
                            except:
                                await interaction.response.defer()
                        @discord.ui.button(label='Close',style=discord.ButtonStyle.red)
                        async def close_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                            try:
                                await interaction.followup.defer()
                            except:
                                await interaction.response.defer()
                    embed = discord.Embed(title = 'Pre-Application',
                                        description = f'{message}', color=colors.dark_gold)
                    await channel.send(ping, embed=embed, view=pre_application_buttons())


        if label == 'Help':
            if category.name == ticket_category_name and channel.id not in ignore_channels:
                disc_channel = client.get_channel(disc_channel_id)
#                await disc_channel.send(f'<@&568141320011382825>\n<#{channel_id}> requests assistance')
                message = 'Staff have been notified. Please be patient.'
                await channel.send(message)


        if label == 'Close':
            if category.name == ticket_category_name and channel.id not in ignore_channels:
                client = self.client
                channel_name = channel.name.split('-')
                channel_name = channel_name[0]
                channel_name = channel.name
                user = interaction.user
                class close_modal(discord.ui.Modal, title='Reason for closing ticket'):
                    answer = discord.ui.TextInput(label='Reason', style=discord.TextStyle.short)
                    async def on_submit(self, interaction: discord.Interaction):
                        answer = self.answer
                        embed = discord.Embed(title='Ticket closed',color=colors.dark_gold)
                        embed.add_field(name = 'Closed by',
                                    value = f'<@{user.id}>',
                                    inline = True)
                        embed.add_field(name = 'Ticket name',
                                    value = f'{channel_name}',
                                    inline = True)
                        embed.add_field(name = 'Reason',
                                    value = f'{answer}',
                                    inline = False)
                        transcript = await chat_exporter.export(channel)

                        if transcript is None:
                            return
                        try:
        #                    file = open(f'./data/transcripts/transcript-{channel_id}.html', 'w')
        #                    file.write(transcript)
        #                    file.close()
        #                    transcript_file = open(f'./data/transcripts/transcript-{channel_id}.html', 'r')
                            transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f'transcript-{channel_id}.html')
                            chan = client.get_channel(archive_channel)
        #                    await chan.send(embed=embed, file=discord.File(transcript_file))
                            await chan.send(embed=embed, file=transcript_file)
                            try:
                                for filename in os.listdir('./data/transcripts'):
                                    if str(chan.id) in filename:
                                        os.remove(f'./data/transcripts/transcript-{channel_id}.html')
                            except:
                                pass
                            try:
                                for filename in os.listdir('./data/tickets'):
                                    if str(chan.id) in filename:
                                        os.remove(f'./data/tickets/{channel_id}.json')
                            except:
                                pass
                            await chan.delete()
                        except:
                            if member == client.is_owner:
                                msg = f'❌ Failed to archive <#{channel_id}> \n\'+close\' ran by <@{member.id}>'
                                await DMChannel.send(member, msg)
                            else:
                                msg = f'❌ Failed to archive <#{ctx.channel.id}>'
                                user = await client.fetch_user(175719252995604480)
                                await DMChannel.send(user, msg)
                                await interaction.response.send_message(f'Ticket closing!', ephemeral=True)

                await interaction.response.send_modal(close_modal())



        if embed_title == 'Pre-Application' and label == 'Start':
            class interview_buttons_1(discord.ui.View):
                def __init__(self, timeout=None):
                    super().__init__()
                @discord.ui.button(label='Yes',style=discord.ButtonStyle.blurple)
                async def yes_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    await interaction.response.defer()
                @discord.ui.button(label='No',style=discord.ButtonStyle.blurple)
                async def no_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    await interaction.response.defer()
                @discord.ui.button(label='Help',style=discord.ButtonStyle.gray)
                async def help_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    await interaction.response.defer()
            print(member.id)
            message = OversightData.interview_message('1', member)
            message = message.replace(reminder, '')
            embed = discord.Embed(title = 'Question number 1',
                                  description = f'{message}', color=colors.dark_gold)
            await channel.send(embed=embed, view=interview_buttons_1())


        if embed_title == 'Question number 1' and label == 'No':
            class link_question(discord.ui.Modal, title='What is your nation link?'):
                answer = discord.ui.TextInput(label='Politics and War nation link', style=discord.TextStyle.short)
                async def on_submit(self, interaction: discord.Interaction):
                    answer = self.answer
                    await channel.edit(topic=answer)
                    await interaction.response.send_message(f'Nation link is {answer}')
                    class interview_buttons_2(discord.ui.View):
                        def __init__(self, timeout=None):
                            super().__init__()
                        @discord.ui.button(label='Next',style=discord.ButtonStyle.blurple)
                        async def next_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                            await interaction.response.defer()
                        @discord.ui.button(label='Help',style=discord.ButtonStyle.gray)
                        async def help_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                            await interaction.response.defer()
                    message = OversightData.interview_message('2', member)
                    message = message.replace(reminder, '')
                    embed = discord.Embed(title = 'Question number 2',
                                          description = f'{message}', color=colors.dark_gold)
                    await channel.send(embed=embed, view=interview_buttons_2())
            await interaction.response.send_modal(link_question())


        if embed_title == 'Question number 1' and label == 'Yes':
            class interview_buttons_2(discord.ui.View):
                def __init__(self, timeout=None):
                    super().__init__()
                @discord.ui.button(label='Next',style=discord.ButtonStyle.blurple)
                async def next_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    try:
                        await interaction.followup.defer()
                    except:
                        await interaction.response.defer()
                @discord.ui.button(label='Help',style=discord.ButtonStyle.gray)
                async def help_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    try:
                        await interaction.followup.defer()
                    except:
                        await interaction.response.defer()
            await interaction.response.send_message('Nation link is correct')
            discord_id = member.id
            user = requests.get(
            f'http://24.117.204.187:8080/discord/?disc_id={discord_id}&key=davethsmellskrampuswhales')
            user = requests.get(f'http://24.117.204.187:8080/discord/?disc_id={discord_id}&key=davethsmellskrampuswhales')
            user = user.json()
            user = user[0]
            nation_id = user.get('id')
            nation_link = f'https://politicsandwar.com/nation/id={nation_id}'
            await channel.edit(topic=nation_link)
            message = OversightData.interview_message('2', member)
            message = message.replace(reminder, '')
            embed = discord.Embed(title = 'Question number 2',
                                  description = f'{message}', color=colors.dark_gold)
            await channel.send(embed=embed, view=interview_buttons_2())


        if embed_title == 'Question number 2' and label == 'Next':
            class interview_buttons_3(discord.ui.View):
                def __init__(self, timeout=None):
                    super().__init__()
                @discord.ui.button(label='Next',style=discord.ButtonStyle.blurple)
                async def next_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    await interaction.response.defer()
                @discord.ui.button(label='Help',style=discord.ButtonStyle.gray)
                async def help_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    await interaction.response.defer()
            message = OversightData.interview_message('3', member)
            message = message.replace(reminder, '')
            embed = discord.Embed(title = 'Question number 3',
                                  description = f'{message}', color=colors.dark_gold)
            await channel.send(embed=embed, view=interview_buttons_3())


        if embed_title == 'Question number 3' and label == 'Next':
            class interview_buttons_4(discord.ui.View):
                def __init__(self, timeout=None):
                    super().__init__()
                @discord.ui.button(label='Next',style=discord.ButtonStyle.blurple)
                async def next_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    await interaction.response.defer()
                @discord.ui.button(label='Help',style=discord.ButtonStyle.gray)
                async def help_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    await interaction.response.defer()
            message = OversightData.interview_message('4', member)
            message = message.replace(reminder, '')
            embed = discord.Embed(title = 'Question number 4',
                                  description = f'{message}', color=colors.dark_gold)
            await channel.send(embed=embed, view=interview_buttons_4())


        if embed_title == 'Question number 4' and label == 'Next':
            class interview_buttons_5(discord.ui.View):
                def __init__(self, timeout=None):
                    super().__init__()
                @discord.ui.button(label='Yes',style=discord.ButtonStyle.blurple)
                async def yes_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    await interaction.response.defer()
                @discord.ui.button(label='No',style=discord.ButtonStyle.blurple)
                async def no_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    await interaction.response.defer()
                @discord.ui.button(label='Help',style=discord.ButtonStyle.gray)
                async def help_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    await interaction.response.defer()
            message = OversightData.interview_message('5', member)
            message = message.replace(reminder, '')
            embed = discord.Embed(title = 'Question number 5',
                                  description = f'{message}', color=colors.dark_gold)
            await channel.send(embed=embed, view=interview_buttons_5())


        if embed_title == 'Question number 5' and label == 'No':
            class interview_buttons_6(discord.ui.View):
                def __init__(self, timeout=None):
                    super().__init__()
                @discord.ui.button(label='Next',style=discord.ButtonStyle.blurple)
                async def next_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    await interaction.response.defer()
                @discord.ui.button(label='Help',style=discord.ButtonStyle.gray)
                async def help_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    await interaction.response.defer()
            await interaction.response.send_message('No')
            message = OversightData.interview_message('6', member)
            message = message.replace(reminder, '')
            embed = discord.Embed(title = 'Question number 6',
                                  description = f'{message}', color=colors.dark_gold)
            await channel.send(embed=embed, view=interview_buttons_6())


        if embed_title == 'Question number 5' and label == 'No':
            class interview_buttons_6(discord.ui.View):
                def __init__(self, timeout=None):
                    super().__init__()
                @discord.ui.button(label='Next',style=discord.ButtonStyle.blurple)
                async def next_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    await interaction.response.defer()
                @discord.ui.button(label='Help',style=discord.ButtonStyle.gray)
                async def help_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    await interaction.response.defer()
            await interaction.response.send_message('Yes')
            message = OversightData.interview_message('6', member)
            message = message.replace(reminder, '')
            embed = discord.Embed(title = 'Question number 6',
                                  description = f'{message}', color=colors.dark_gold)
            await channel.send(embed=embed, view=interview_buttons_6())


        if embed_title == 'Question number 6' and label == 'Next':
            class interview_buttons_7(discord.ui.View):
                def __init__(self, timeout=None):
                    super().__init__()
                @discord.ui.button(label='Next',style=discord.ButtonStyle.blurple)
                async def next_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    await interaction.response.defer()
                @discord.ui.button(label='Help',style=discord.ButtonStyle.gray)
                async def help_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    await interaction.response.defer()
            message = OversightData.interview_message('7', member)
            message = message.replace(reminder, '')
            embed = discord.Embed(title = 'Question number 7',
                                  description = f'{message}', color=colors.dark_gold)
            await channel.send(embed=embed, view=interview_buttons_7())


        if embed_title == 'Question number 7' and label == 'Next':
            class Select(discord.ui.Select):
                def __init__(self):
                    options=[
            discord.SelectOption(label='Option 1', emoji='1️⃣'),
            discord.SelectOption(label='Option 2', emoji='2️⃣'),
            discord.SelectOption(label='Option 3', emoji='3️⃣'),
            discord.SelectOption(label='Option 4', emoji='4️⃣'),
            discord.SelectOption(label='Other'),
            ]
                    super().__init__(placeholder='Select an option',max_values=1,min_values=1,options=options)
                async def callback(self, interaction: discord.Interaction):
                    if self.values[0] == 'Option 1':
                        await interaction.response.send_message('Option 1', ephemeral=False)
                    elif self.values[0] == 'Option 2':
                        await interaction.response.send_message('Option 2', ephemeral=False)
                    elif self.values[0] == 'Option 3':
                        await interaction.response.send_message('Option 3', ephemeral=False)
                    elif self.values[0] == 'Option 4':
                        await interaction.response.send_message('Option 4', ephemeral=False)
                    elif self.values[0] == 'Other':
                        class Questionnaire(discord.ui.Modal, title='Questionnaire Response'):
                            answer = discord.ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)

                            async def on_submit(self, interaction: discord.Interaction):
                                answer = self.answer
                                await interaction.response.send_message(f'{answer}', ephemeral=False)
                        await interaction.response.send_modal(Questionnaire())

            class SelectView(discord.ui.View):
                def __init__(self, *, timeout = None):
                    super().__init__(timeout=timeout)
                    self.add_item(Select())
            message = OversightData.interview_message('8', member)
            message = message.replace(reminder, '')
            embed = discord.Embed(title = 'Question number 8',
                                  description = f'{message}', color=colors.dark_gold)
            await channel.send(embed=embed,view=SelectView())


        if embed_title == 'Question number 8':
            class Select(discord.ui.Select):
                def __init__(self):
                    options=[
            discord.SelectOption(label='War Department'),
            discord.SelectOption(label='Foreign affairs department'),
            discord.SelectOption(label='Tech Department'),
            discord.SelectOption(label='Discipline Department'),
            discord.SelectOption(label='Culture Department'),
            discord.SelectOption(label='Treasury Department'),
            discord.SelectOption(label='None')
            ]
                    super().__init__(placeholder='Select an option',max_values=7,min_values=1,options=options)
                async def callback(self, interaction: discord.Interaction):
                    values = ''
                    for value in self.values:
                        values += f'{value}\n'
                    await interaction.response.send_message(f'{values}', ephemeral=False)

            class SelectView(discord.ui.View):
                def __init__(self, *, timeout = None):
                    super().__init__(timeout=timeout)
                    self.add_item(Select())
            message = OversightData.interview_message('9', member)
            message = message.replace(reminder, '')
            embed = discord.Embed(title = 'Question number 9',
                                  description = f'{message}', color=colors.dark_gold)
            await channel.send(embed=embed,view=SelectView())


        if embed_title == 'Question number 9':
            class Select(discord.ui.Select):
                def __init__(self):
                    options=[
            discord.SelectOption(label='Option 1', emoji='1️⃣'),
            discord.SelectOption(label='Option 2', emoji='2️⃣'),
            discord.SelectOption(label='Option 3', emoji='3️⃣'),
            discord.SelectOption(label='Option 4', emoji='4️⃣'),
            discord.SelectOption(label='Option 5', emoji='5️⃣'),
            discord.SelectOption(label='Option 6', emoji='6️⃣'),
            discord.SelectOption(label='Option 7', emoji='7️⃣')
            ]
                    super().__init__(placeholder='Select an option',max_values=7,min_values=1,options=options)
                async def callback(self, interaction: discord.Interaction):
                    values = ''
                    for value in self.values:
                        values += f'{value}\n'
                    await interaction.response.send_message(f'{values}', ephemeral=False)

            class SelectView(discord.ui.View):
                def __init__(self, *, timeout = None):
                    super().__init__(timeout=timeout)
                    self.add_item(Select())
            message = OversightData.interview_message('10', member)
            message = message.replace(reminder, '')
            embed = discord.Embed(title = 'Question number 10',
                                  description = f'{message}', color=colors.dark_gold)
            await channel.send(embed=embed,view=SelectView())


        if embed_title == 'Question number 10':
            class Select(discord.ui.Select):
                def __init__(self):
                    options=[
            discord.SelectOption(label='Option 1',emoji='1️⃣'),
            discord.SelectOption(label='Option 2',emoji='2️⃣'),
            discord.SelectOption(label='Option 3',emoji='3️⃣'),
            discord.SelectOption(label='Option 4',emoji='4️⃣'),
            discord.SelectOption(label='Option 5',emoji='5️⃣'),
            discord.SelectOption(label='Option 6',emoji='6️⃣'),
            discord.SelectOption(label='Option 7',emoji='7️⃣')
            ]
                    super().__init__(placeholder='Select an option',max_values=7,min_values=1,options=options)
                async def callback(self, interaction: discord.Interaction):
                    values = ''
                    for value in self.values:
                        values += f'{value}\n'
                    await interaction.response.send_message(f'{values}', ephemeral=False)

            class SelectView(discord.ui.View):
                def __init__(self, *, timeout = None):
                    super().__init__(timeout=timeout)
                    self.add_item(Select())
            message = OversightData.interview_message('11', member)
            message = message.replace(reminder, '')
            embed = discord.Embed(title = 'Question number 11',
                                  description = f'{message}', color=colors.dark_gold)
            await channel.send(embed=embed,view=SelectView())


        if embed_title == 'Question number 11':
            class interview_buttons_12(discord.ui.View):
                def __init__(self, timeout=None):
                    super().__init__()
                @discord.ui.button(label='Agree',style=discord.ButtonStyle.blurple)
                async def next_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    try:
                        await interaction.followup.defer()
                    except:
                        await interaction.response.defer()
                @discord.ui.button(label='Disagree',style=discord.ButtonStyle.red)
                async def help_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    try:
                        await interaction.followup.defer()
                    except:
                        await interaction.response.defer()
                @discord.ui.button(label='Help',style=discord.ButtonStyle.gray)
                async def help_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                    try:
                        await interaction.followup.defer()
                    except:
                        await interaction.response.defer()
            message = OversightData.interview_message('12', member)
            if isinstance(message, list) == True:
                l = 0
                for item in message:
                    l += 1
                    if l == 1:
                        embed = discord.Embed(title = f'--- TERMS AND CONDITIONS of Carthago ---',
                                    description = f'{item}', color=colors.dark_gold)
                        await channel.send(embed=embed)
                    else:
                        item = item.replace(reminder, '')
                        embed = discord.Embed(title = f'',
                                    description = f'{item}', color=colors.dark_gold)
            await channel.send(embed=embed,view=interview_buttons_12())


        if label == 'Agree':
            disc_channel = client.get_channel(disc_channel_id)
            class Select(discord.ui.Select):
                def __init__(self):
                    options=[
            discord.SelectOption(label='UTC -12',emoji='🕛'),
            discord.SelectOption(label='UTC -11',emoji='🕚'),
            discord.SelectOption(label='UTC -10',emoji='🕙'),
            discord.SelectOption(label='UTC -9',emoji='🕘'),
            discord.SelectOption(label='UTC -8',emoji='🕗'),
            discord.SelectOption(label='UTC -7',emoji='🕖'),
            discord.SelectOption(label='UTC -6',emoji='🕕'),
            discord.SelectOption(label='UTC -5',emoji='🕔'),
            discord.SelectOption(label='UTC -4',emoji='🕓'),
            discord.SelectOption(label='UTC -3',emoji='🕒'),
            discord.SelectOption(label='UTC -2',emoji='🕑'),
            discord.SelectOption(label='UTC -1',emoji='🕐'),
            discord.SelectOption(label='UTC +0',emoji='⏳'),
            discord.SelectOption(label='UTC +1',emoji='🕐'),
            discord.SelectOption(label='UTC +2',emoji='🕑'),
            discord.SelectOption(label='UTC +3',emoji='🕒'),
            discord.SelectOption(label='UTC +4',emoji='🕓'),
            discord.SelectOption(label='UTC +5',emoji='🕔'),
            discord.SelectOption(label='UTC +6',emoji='🕕'),
            discord.SelectOption(label='UTC +7',emoji='🕖'),
            discord.SelectOption(label='UTC +8',emoji='🕗'),
            discord.SelectOption(label='UTC +9',emoji='🕘'),
            discord.SelectOption(label='UTC +10',emoji='🕙'),
            discord.SelectOption(label='UTC +11',emoji='🕚'),
            discord.SelectOption(label='UTC +12',emoji='🕛')
            ]
                    super().__init__(placeholder='Select a timezone',max_values=1,min_values=1,options=options)
                async def callback(self, interaction: discord.Interaction):

                    if self.values[0] == 'UTC -12':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -12', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -11':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -11', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -10':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -10', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -9':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -9', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -8':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -8', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -7':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -7', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -6':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -6', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -5':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -5', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -4':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -4', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -3':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -3', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -2':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -2', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -1':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -1', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +0':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +0', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +1':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +1', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +2':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +2', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +3':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +3', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +4':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +4', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +5':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +5', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +6':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +6', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +7':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC 7', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +8':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +8', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +9':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +9', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +10':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +10', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +11':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +11', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +12':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +12', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

            class SelectView(discord.ui.View):
                def __init__(self, *, timeout = None):
                    super().__init__(timeout=timeout)
                    self.add_item(Select())
            message = OversightData.interview_message('13', member)
            await interaction.response.send_message('Agree', ephemeral=False)
            embed = discord.Embed(title = f'Question number 13',
                                description = f'{message}', color=colors.dark_gold)
            await channel.send(embed=embed,view=SelectView())


        if label == 'Disagree':
            disc_channel = client.get_channel(disc_channel_id)
            class Select(discord.ui.Select):
                def __init__(self):
                    options=[
            discord.SelectOption(label='UTC -12',emoji='🕛'),
            discord.SelectOption(label='UTC -11',emoji='🕚'),
            discord.SelectOption(label='UTC -10',emoji='🕙'),
            discord.SelectOption(label='UTC -9',emoji='🕘'),
            discord.SelectOption(label='UTC -8',emoji='🕗'),
            discord.SelectOption(label='UTC -7',emoji='🕖'),
            discord.SelectOption(label='UTC -6',emoji='🕕'),
            discord.SelectOption(label='UTC -5',emoji='🕔'),
            discord.SelectOption(label='UTC -4',emoji='🕓'),
            discord.SelectOption(label='UTC -3',emoji='🕒'),
            discord.SelectOption(label='UTC -2',emoji='🕑'),
            discord.SelectOption(label='UTC -1',emoji='🕐'),
            discord.SelectOption(label='UTC +0',emoji='⏳'),
            discord.SelectOption(label='UTC +1',emoji='🕐'),
            discord.SelectOption(label='UTC +2',emoji='🕑'),
            discord.SelectOption(label='UTC +3',emoji='🕒'),
            discord.SelectOption(label='UTC +4',emoji='🕓'),
            discord.SelectOption(label='UTC +5',emoji='🕔'),
            discord.SelectOption(label='UTC +6',emoji='🕕'),
            discord.SelectOption(label='UTC +7',emoji='🕖'),
            discord.SelectOption(label='UTC +8',emoji='🕗'),
            discord.SelectOption(label='UTC +9',emoji='🕘'),
            discord.SelectOption(label='UTC +10',emoji='🕙'),
            discord.SelectOption(label='UTC +11',emoji='🕚'),
            discord.SelectOption(label='UTC +12',emoji='🕛')
            ]
                    super().__init__(placeholder='Select a timezone',max_values=1,min_values=1,options=options)
                async def callback(self, interaction: discord.Interaction):
                    reminder = f'If at any time you\'d like to be interviewed by a human, react with {person} \n' \
                    + f'**After** you\'ve answered, react with {right_arrow} to continue'

                    if self.values[0] == 'UTC -12':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -12', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -11':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -11', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -10':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -10', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -9':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -9', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -8':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -8', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -7':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -7', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -6':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -6', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -5':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -5', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -4':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -4', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -3':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -3', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -2':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -2', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC -1':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC -1', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +0':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +0', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +1':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +1', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +2':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +2', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +3':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +3', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +4':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +4', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +5':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +5', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +6':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +6', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +7':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC 7', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +8':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +8', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +9':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +9', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +10':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +10', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +11':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +11', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

                    elif self.values[0] == 'UTC +12':
                        message = OversightData.interview_message('14', member)
                        message = message.replace(reminder, '')
                        embed = discord.Embed(title = f'Automated interview over',
                                        description = f'{message}', color=colors.dark_gold)
                        await interaction.response.send_message('UTC +12', ephemeral=False)
                        await channel.send(embed=embed)
#                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')

            class SelectView(discord.ui.View):
                def __init__(self, *, timeout = None):
                    super().__init__(timeout=timeout)
                    self.add_item(Select())
            await interaction.response.send_message('Disagree', ephemeral=False)
            message = OversightData.interview_message('13', member)
            embed = discord.Embed(title = f'Question number 13',
                                description = f'{message}', color=colors.dark_gold)
            await channel.send(embed=embed,view=SelectView())


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
            client = self.client
            chan_name = channel.name.split('-')
            chan_id = channel.id
            suffet_role = channel.guild.get_role(suffet_role_id)
            elder_role = channel.guild.get_role(elder_role_id)
            pentarch_role = channel.guild.get_role(pentarch_role_id)
            interviewer_role = channel.guild.get_role(interviewer_role_id)
            adirim_role = channel.guild.get_role(adirim_role_id)
            bot_role = channel.guild.get_role(bot_role_id)
            if chan_name[0] == 'ticket':
                try:
                    with open(f'./data/tickets/{chan_id}.json') as data:
                        dic = json.load(data)
                        member_id = dic.get('user_id')
                except:
                    for member in channel.members:
                        if suffet_role not in member.roles and elder_role not in member.roles \
                        and pentarch_role not in member.roles and interviewer_role not in member.roles \
                        and adirim_role not in member.roles and bot_role not in member.roles \
                        and not member.bot:
                            member_id = member.id
                            break
                    dic = {'channel':chan_name, 'user_id':member_id}
                with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                    json.dump(dic, outfile)
#                async for message in channel.history(limit=5):
#                    if message == f'<@{member_id}>' and message.author == client.user:
#                        await message.delete()
#                        break
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
                msg = await channel.send(f'<@{member_id}>', embed=embed)
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
#                    chan_name = chan.name
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
                            with open(f'./data/tickets/{chan_id}.json') as data:
                                dic = json.load(data)
                            dic.update({'num':num})
                        except:
                            dic = {'channel':chan.name, 'user_id':member.id}
                            dic.update({'num':num})
                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
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
                            with open(f'./data/tickets/{chan_id}.json') as data:
                                dic = json.load(data)
                        except:
                            num = '0'
                            dic = {'channel':chan.name, 'user_id':member.id}
                            dic.update({'num':num})
                        num = int(dic.get('num'))
                        num += 1
                        num = str(num)
                        dic.update({'num':num})
                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                            json.dump(dic, outfile)

                        message = OversightData.interview_message(num, member)
                        skip = False
                        if isinstance(message, list) == True:
                            skip = True
                            l = 0
                            for item in message:
                                l += 1
                                if l == 1:
                                    embed = discord.Embed(title = f'--- TERMS AND CONDITIONS of Carthago ---',
                                                description = f'{item}', color=colors.dark_gold)
                                    await chan.send(embed=embed)
                                else:
                                    embed = discord.Embed(title = f'',
                                                description = f'{item}', color=colors.dark_gold)
                                    msg = await chan.send(embed=embed)
                                    await msg.add_reaction(right_arrow)
                                    await msg.add_reaction(person)
                            await user_message.reactions[0].remove(member)
                        elif num == '17':
                            class Select(discord.ui.Select):
                                def __init__(self):
                                    options=[
                            discord.SelectOption(label='UTC -12',emoji='🕛'),
                            discord.SelectOption(label='UTC -11',emoji='🕚'),
                            discord.SelectOption(label='UTC -10',emoji='🕙'),
                            discord.SelectOption(label='UTC -9',emoji='🕘'),
                            discord.SelectOption(label='UTC -8',emoji='🕗'),
                            discord.SelectOption(label='UTC -7',emoji='🕖'),
                            discord.SelectOption(label='UTC -6',emoji='🕕'),
                            discord.SelectOption(label='UTC -5',emoji='🕔'),
                            discord.SelectOption(label='UTC -4',emoji='🕓'),
                            discord.SelectOption(label='UTC -3',emoji='🕒'),
                            discord.SelectOption(label='UTC -2',emoji='🕑'),
                            discord.SelectOption(label='UTC -1',emoji='🕐'),
                            discord.SelectOption(label='UTC +0',emoji='⏳'),
                            discord.SelectOption(label='UTC +1',emoji='🕐'),
                            discord.SelectOption(label='UTC +2',emoji='🕑'),
                            discord.SelectOption(label='UTC +3',emoji='🕒'),
                            discord.SelectOption(label='UTC +4',emoji='🕓'),
                            discord.SelectOption(label='UTC +5',emoji='🕔'),
                            discord.SelectOption(label='UTC +6',emoji='🕕'),
                            discord.SelectOption(label='UTC +7',emoji='🕖'),
                            discord.SelectOption(label='UTC +8',emoji='🕗'),
                            discord.SelectOption(label='UTC +9',emoji='🕘'),
                            discord.SelectOption(label='UTC +10',emoji='🕙'),
                            discord.SelectOption(label='UTC +11',emoji='🕚'),
                            discord.SelectOption(label='UTC +12',emoji='🕛')
                            ]
                                    super().__init__(placeholder='Select a timezone',max_values=1,min_values=1,options=options)
                                async def callback(self, interaction: discord.Interaction):
                                    reminder = f'If at any time you\'d like to be interviewed by a human, react with {person} \n' \
                                    + f'**After** you\'ve answered, react with {right_arrow} to continue'
                                    if self.values[0] == 'UTC -12':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC -12', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC -11':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC -11', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC -10':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC -10', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC -9':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC -9', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC -8':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC -8', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC -7':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC -7', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC -6':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC -6', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC -5':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC -5', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC -4':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC -4', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC -3':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC -3', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC -2':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC -2', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC -1':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC -1', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC +0':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC +0', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        await user_message.reactions[0].remove(member)
                                    elif self.values[0] == 'UTC +1':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC +1', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC +2':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC +2', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC +3':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC +3', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC +4':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC +4', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC +5':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC +5', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC +6':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC +6', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC +7':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC 7', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC +8':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC +8', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC +9':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC +9', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC +10':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC +10', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC +11':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC +11', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                    elif self.values[0] == 'UTC +12':
                                        num = int(dic.get('num'))
                                        num += 1
                                        num = str(num)
                                        dic.update({'num':num})
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)
                                        message = OversightData.interview_message(num, member)
                                        message = message.replace(reminder, '')
                                        embed = discord.Embed(title = f'Question number {num}',
                                                        description = f'{message}', color=colors.dark_gold)
                                        await interaction.response.send_message('UTC +12', ephemeral=False)
                                        await chan.send(embed=embed)
                                        await disc_channel.send(f'<@&568141320011382825>\n<#{chan_id}> Needs approved/denied')
                                        with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                            json.dump(dic, outfile)

                            class SelectView(discord.ui.View):
                                def __init__(self, *, timeout = None):
                                    super().__init__(timeout=timeout)
                                    self.add_item(Select())
                            message = OversightData.interview_message(num, member)
                            embed = discord.Embed(title = f'Question number {num}',
                                                description = f'{message}', color=colors.dark_gold)
                            await chan.send(embed=embed,view=SelectView())
                        elif skip != True:
                            message = OversightData.interview_message(num, member)
                            embed = discord.Embed(title = f'Question number {num}',
                                            description = f'{message}', color=colors.dark_gold)
                            msg = await chan.send(embed=embed)
                            await msg.add_reaction(right_arrow)
                            await msg.add_reaction(person)
                            with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                json.dump(dic, outfile)
                            await user_message.reactions[0].remove(member)

    @commands.command(name='start', help='+start')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'Interviewer')
    async def start(self, ctx, num: typing.Optional[str] = '0' ):
        if ctx.channel.category.id == 567390184774303745 or ctx.channel.category.id == 876639217042751578 or ctx.channel.id == 736099358344478764:
            chan_id = ctx.channel.id
            suffet_role = ctx.guild.get_role(suffet_role_id)
            elder_role = ctx.guild.get_role(elder_role_id)
            pentarch_role = ctx.guild.get_role(pentarch_role_id)
            interviewer_role = ctx.guild.get_role(trainee_role_id)
            adirim_role = ctx.guild.get_role(adirim_role_id)
            try:
                with open(f'./data/tickets/{chan_id}.json') as data:
                    dic = json.load(data)
                dic.update({'num':num})
                with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
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
                with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                    json.dump(dic, outfile)
            user = None
            message = OversightData.interview_message(num, user)
            skip = False
            if isinstance(message, list) == True:
                skip = True
                l = 0
                for item in message:
                    l += 1
                    if l == 1:
                        embed = discord.Embed(title = f'--- TERMS AND CONDITIONS of Carthago ---',
                                    description = f'{item}', color=colors.dark_gold)
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title = f'',
                                    description = f'{item}', color=colors.dark_gold)
                        msg = await ctx.send(embed=embed)
                        await msg.add_reaction(right_arrow)
                        await msg.add_reaction(person)
            elif num != '0':
                embed = discord.Embed(title = f'Question number {num}',
                            description = f'{message}', color=colors.dark_gold)
            elif skip != True:
                embed = discord.Embed(title = f'Interview information',
                            description = f'{message}', color=colors.dark_gold)
            msg = await ctx.send(embed=embed)
            await msg.add_reaction(right_arrow)
            await msg.add_reaction(person)

    @commands.command(name='next', help='+next')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'Interviewer')
    async def next(self, ctx):
        if ctx.channel.category.id == 567390184774303745 or ctx.channel.category.id == 876639217042751578 or ctx.channel.id == 736099358344478764:
            member = None
            chan_name = ctx.channel.name
            chan_id = ctx.channel.id
            suffet_role = ctx.guild.get_role(suffet_role_id)
            elder_role = ctx.guild.get_role(elder_role_id)
            pentarch_role = ctx.guild.get_role(pentarch_role_id)
            interviewer_role = ctx.guild.get_role(trainee_role_id)
            adirim_role = ctx.guild.get_role(adirim_role_id)
            try:
                with open(f'./data/tickets/{chan_id}.json') as data:
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
            with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                json.dump(dic, outfile)
            user = None
            message = OversightData.interview_message(num, user)
            skip = False
            if num != '19' and int(num) <= 19:
                if isinstance(message, list) == True:
                    skip = True
                    l = 0
                    for item in message:
                        l += 1
                        if l == 1:
                            embed = discord.Embed(title = f'--- TERMS AND CONDITIONS of Carthago ---',
                                        description = f'{item}', color=colors.dark_gold)
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(title = f'',
                                        description = f'{item}', color=colors.dark_gold)
                            msg = await ctx.send(embed=embed)
                            await msg.add_reaction(right_arrow)
                            await msg.add_reaction(person)
                elif num == '13':
                    class Select(discord.ui.Select):
                        def __init__(self):
                            options=[
                    discord.SelectOption(label='UTC -12',emoji='🕛'),
                    discord.SelectOption(label='UTC -11',emoji='🕚'),
                    discord.SelectOption(label='UTC -10',emoji='🕙'),
                    discord.SelectOption(label='UTC -9',emoji='🕘'),
                    discord.SelectOption(label='UTC -8',emoji='🕗'),
                    discord.SelectOption(label='UTC -7',emoji='🕖'),
                    discord.SelectOption(label='UTC -6',emoji='🕕'),
                    discord.SelectOption(label='UTC -5',emoji='🕔'),
                    discord.SelectOption(label='UTC -4',emoji='🕓'),
                    discord.SelectOption(label='UTC -3',emoji='🕒'),
                    discord.SelectOption(label='UTC -2',emoji='🕑'),
                    discord.SelectOption(label='UTC -1',emoji='🕐'),
                    discord.SelectOption(label='UTC +0',emoji='⏳'),
                    discord.SelectOption(label='UTC +1',emoji='🕐'),
                    discord.SelectOption(label='UTC +2',emoji='🕑'),
                    discord.SelectOption(label='UTC +3',emoji='🕒'),
                    discord.SelectOption(label='UTC +4',emoji='🕓'),
                    discord.SelectOption(label='UTC +5',emoji='🕔'),
                    discord.SelectOption(label='UTC +6',emoji='🕕'),
                    discord.SelectOption(label='UTC +7',emoji='🕖'),
                    discord.SelectOption(label='UTC +8',emoji='🕗'),
                    discord.SelectOption(label='UTC +9',emoji='🕘'),
                    discord.SelectOption(label='UTC +10',emoji='🕙'),
                    discord.SelectOption(label='UTC +11',emoji='🕚'),
                    discord.SelectOption(label='UTC +12',emoji='🕛')
                    ]
                            super().__init__(placeholder='Select a timezone',max_values=1,min_values=1,options=options)
                        async def callback(self, interaction: discord.Interaction):
                            if self.values[0] == 'UTC -12':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                if int(num) >= 14:
                                    dic.update({'num':num})
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC -12', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC -11':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) >= 14:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC -11', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC -10':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) >= 14:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC -10', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC -9':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) >= 14:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC -9', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC -8':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) >= 14:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC -8', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC -7':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) >= 14:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC -7', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC -6':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) >= 14:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC -6', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC -5':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                    json.dump(dic, outfile)
                                message = OversightData.interview_message(num, member)
                                embed = discord.Embed(title = f'Question number {num}',
                                                description = f'{message}', color=colors.dark_gold)
                                await interaction.response.send_message('UTC -5', ephemeral=False)
                                await ctx.send(embed=embed)
                                with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                    json.dump(dic, outfile)
                            elif self.values[0] == 'UTC -4':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) >= 14:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC -4', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC -3':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) >= 14:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC -3', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC -2':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) >= 14:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC -2', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC -1':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) >= 14:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC -1', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC +0':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) >= 14:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC +0', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC +1':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) >= 14:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC +1', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC +2':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) >= 14:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC +2', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC +3':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) >= 14:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC +3', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC +4':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) >= 14:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC +4', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC +5':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) >= 14:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC +5', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC +6':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) >= 14:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC +6', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC +7':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                if int(num) <= 19:
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC 7', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC +8':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                if int(num) <= 19:
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC +8', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC +9':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                if int(num) <= 19:
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC +9', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC +10':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                if int(num) <= 19:
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC +10', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC +11':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                if int(num) <= 19:
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC +11', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                            elif self.values[0] == 'UTC +12':
                                num = int(dic.get('num'))
                                num += 1
                                num = str(num)
                                dic.update({'num':num})
                                with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)
                                if int(num) <= 19:
                                    message = OversightData.interview_message(num, member)
                                    embed = discord.Embed(title = f'Question number {num}',
                                                    description = f'{message}', color=colors.dark_gold)
                                    await interaction.response.send_message('UTC +12', ephemeral=False)
                                    await ctx.send(embed=embed)
                                    with open(f'./data/tickets/{chan_id}.json', 'w') as outfile:
                                        json.dump(dic, outfile)

                    class SelectView(discord.ui.View):
                        def __init__(self, *, timeout = 180):
                            super().__init__(timeout=timeout)
                            self.add_item(Select())
                    message = OversightData.interview_message(num, member)
                    embed = discord.Embed(title = f'Question number {num}',
                                        description = f'{message}', color=colors.dark_gold)
                    await ctx.send(embed=embed,view=SelectView())
                elif skip != True and int(num) <= 19:
                    message = OversightData.interview_message(num, user)
                    embed = discord.Embed(title = f'Question number {num}',
                                    description = f'{message}', color=colors.dark_gold)
                    msg = await ctx.send(embed=embed)
                    await msg.add_reaction(right_arrow)
                    await msg.add_reaction(person)
                data = open(f'./data/tickets/{chan_id}.json')
                dic = json.load(data)
                dic.update({'num':num})
                for user in ctx.channel.members:
                    if 'foreigner' in user.roles:
                        user_id = user.id
                        dic.update({'user_id':user_id})
            elif num == '19':
                message = OversightData.interview_message(num, member)
                embed = discord.Embed(title = f'',
                                    description = f'{message}', color=colors.dark_gold)
                msg = await ctx.send(embed=embed)
                await msg.add_reaction(right_arrow)
                await msg.add_reaction(person)
                os.remove(f'./data/tickets/{chan_id}.json')
            await ctx.message.delete()


async def setup(client):
	await client.add_cog(interview(client))