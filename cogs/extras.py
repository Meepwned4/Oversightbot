import discord
from discord.ext import commands
import requests
import aiohttp
from bs4 import BeautifulSoup
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

class Select(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="UTC -12",emoji='🕛'),
            discord.SelectOption(label="UTC -11",emoji='🕚'),
            discord.SelectOption(label="UTC -10",emoji='🕙'),
            discord.SelectOption(label="UTC -9",emoji='🕘'),
            discord.SelectOption(label="UTC -8",emoji='🕗'),
            discord.SelectOption(label="UTC -7",emoji='🕖'),
            discord.SelectOption(label="UTC -6",emoji='🕕'),
            discord.SelectOption(label="UTC -5",emoji='🕔'),
            discord.SelectOption(label="UTC -4",emoji='🕓'),
            discord.SelectOption(label="UTC -3",emoji='🕒'),
            discord.SelectOption(label="UTC -2",emoji='🕑'),
            discord.SelectOption(label="UTC -1",emoji='🕐'),
            discord.SelectOption(label="UTC +0",emoji='⏳'),
            discord.SelectOption(label="UTC +1",emoji='🕐'),
            discord.SelectOption(label="UTC +2",emoji='🕑'),
            discord.SelectOption(label="UTC +3",emoji='🕒'),
            discord.SelectOption(label="UTC +4",emoji='🕓'),
            discord.SelectOption(label="UTC +5",emoji='🕔'),
            discord.SelectOption(label="UTC +6",emoji='🕕'),
            discord.SelectOption(label="UTC +7",emoji='🕖'),
            discord.SelectOption(label="UTC +8",emoji='🕗'),
            discord.SelectOption(label="UTC +9",emoji='🕘'),
            discord.SelectOption(label="UTC +10",emoji='🕙'),
            discord.SelectOption(label="UTC +11",emoji='🕚'),
            discord.SelectOption(label="UTC +12",emoji='🕛')
            ]
        super().__init__(placeholder="Select a timezone",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "UTC -12":
            await interaction.response.send_message("UTC -12", ephemeral=False)
            await interaction.response.send_message("UTC -12", ephemeral=False)
        elif self.values[0] == "UTC -11":
            await interaction.response.send_message("UTC -11",ephemeral=False)
        elif self.values[0] == "UTC -10":
            await interaction.response.send_message("UTC -10",ephemeral=False)
        elif self.values[0] == "UTC -9":
            await interaction.response.send_message("UTC -9",ephemeral=False)
        elif self.values[0] == "UTC -8":
            await interaction.response.send_message("UTC -8",ephemeral=False)
        elif self.values[0] == "UTC -7":
            await interaction.response.send_message("UTC -7",ephemeral=False)
        elif self.values[0] == "UTC -6":
            await interaction.response.send_message("UTC -6",ephemeral=False)
        elif self.values[0] == "UTC -5":
            await interaction.response.send_message("UTC -5",ephemeral=False)
        elif self.values[0] == "UTC -4":
            await interaction.response.send_message("UTC -4",ephemeral=False)
        elif self.values[0] == "UTC -3":
            await interaction.response.send_message("UTC -3",ephemeral=False)
        elif self.values[0] == "UTC -2":
            await interaction.response.send_message("UTC -2",ephemeral=False)
        elif self.values[0] == "UTC -1":
            await interaction.response.send_message("UTC -1",ephemeral=False)
        elif self.values[0] == "UTC +0":
            await interaction.response.send_message("UTC +0",ephemeral=False)
        elif self.values[0] == "UTC +1":
            await interaction.response.send_message("UTC +1",ephemeral=False)
        elif self.values[0] == "UTC +2":
            await interaction.response.send_message("UTC +2",ephemeral=False)
        elif self.values[0] == "UTC +3":
            await interaction.response.send_message("UTC +3",ephemeral=False)
        elif self.values[0] == "UTC +4":
            await interaction.response.send_message("UTC +4",ephemeral=False)
        elif self.values[0] == "UTC +5":
            await interaction.response.send_message("UTC +5",ephemeral=False)
        elif self.values[0] == "UTC +6":
            await interaction.response.send_message("UTC +6",ephemeral=False)
        elif self.values[0] == "UTC +7":
            await interaction.response.send_message("UTC +7",ephemeral=False)
        elif self.values[0] == "UTC +8":
            await interaction.response.send_message("UTC +8",ephemeral=False)
        elif self.values[0] == "UTC +9":
            await interaction.response.send_message("UTC +9",ephemeral=False)
        elif self.values[0] == "UTC +10":
            await interaction.response.send_message("UTC +10",ephemeral=False)
        elif self.values[0] == "UTC +11":
            await interaction.response.send_message("UTC +11",ephemeral=False)
        elif self.values[0] == "UTC +12":
            await interaction.response.send_message("UTC +12",ephemeral=False)
#            await interaction.response.edit_message(content="1")
#        elif self.values[0] == "Option 2":
#            await interaction.response.send_message("2",ephemeral=False)
#        elif self.values[0] == "Option 3":
#            await interaction.response.send_message("3",ephemeral=True)

class SelectView(discord.ui.View):
    def __init__(self, *, timeout = None):
        super().__init__(timeout=timeout)
        self.add_item(Select())

class Questionnaire(discord.ui.Modal, title='Questionnaire Response'):
    name = discord.ui.TextInput(label='Name')
    answer = discord.ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        data = interaction.data
        data = data.get('components')
        name = data[0].get('components')
        name = name[0].get('value')
        answer = data[1].get('components')
        answer = answer[0].get('value')
        print(name)
        print(answer)
        await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)


class Button(discord.ui.View):
    def __init__(self, timeout=None):
        super().__init__()
    @discord.ui.button(label="Button 1",style=discord.ButtonStyle.gray)
    async def gray_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.edit_message(content=f"This was edited by button 1!")
    @discord.ui.button(label="Button 2",style=discord.ButtonStyle.red)
    async def red_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.edit_message(content=f"This was edited by button 2!")

class extras(commands.Cog):

    def __init__(self, client):
        self.client = client
        client = self.client

    @commands.command(name='modal', help='+modal')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet')
    async def modal(self, ctx):
        class button(discord.ui.View):
            def __init__(self, timeout=None):
                super().__init__()
            @discord.ui.button(label="Button 1",style=discord.ButtonStyle.gray)
            async def gray_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                await interaction.response.send_modal(Questionnaire())
        await ctx.send(view=button())

    @commands.command(name='menu', help='+menu')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet')
    async def menu(self, ctx):
        right_arrow = '➡' # right arrow emoji
        person = '🧑' # person emoji
        reminder = f'If at any time you\'d like to be interviewed by a human, react with {person} \n' \
    + f'**After** you\'ve answered, react with {right_arrow} to continue'
        member = None
        num = '13'
        words = OversightData.interview_message(num, member)
        words = words.replace(reminder, '')
        embed = discord.Embed(title = f'',
                            description = f'{words}', color=colors.dark_gold)
        await ctx.send(embed=embed,view=SelectView())

    @commands.command(name='button', help='+button')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet')
    async def button(self, ctx):
        await ctx.send("This message has buttons!",view=Button())

    @commands.command(name='tax_bracket', help='+tax_bracket 92845 100', aliases=['tax', 'taxes'])
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet')
    async def tax_bracket(self, ctx, nation, tax: str):
        if ctx.channel.category.name != '[The Harbour]' and ctx.channel.category.name != '[Discussion]':
            login_data = {'email': 'jacksonayres11@gmail.com', 'password': 'Dungeons&Dragons', 'loginform': 'Login'}
            check = False
            if len(nation) == 18:
                nation = requests.get(
                    f'http://24.117.204.187:8080/discord/?DiscordID={nation}&key=davethsmellskrampuswhales')
                nation = nation.json()
                nation = nation[0]
                nation_id = str(nation.get('_id'))
            else:
                nation_id = nation

            if tax == 'communism' or tax == 'commie' or tax == '100' or \
            tax == '13587' or tax == 100:
                tax_id = '13587'
                check = True
            elif tax == 'low' or tax == '30' or tax == 'lower tier' or \
            tax == 'lower' or tax == '9472' or tax == 30:
                tax_id = '9472'
                check = True
            elif tax == 'up' or tax == 'upper' or tax == 'upper tier' or \
            tax == '10' or tax == '9293' or tax == 10:
                tax_id = '9293'
                check = True
            elif tax == 'laissez-faire' or tax == 'laissez' or tax == '0' or \
            tax == '15344' or tax == 0:
                tax_id = '15344'
                check = True

            if check == False:
                await ctx.send('Invalid tax bracket.')
            else:
                login = True
                async with aiohttp.ClientSession() as session:
                    login_url = 'https://politicsandwar.com/login/'
                    res1 = await session.post(login_url, data=login_data)
                    if(len((BeautifulSoup(await res1.text(), 'html.parser')).body.findAll(text='Login Failure')) > 0):
                        print('Login failed')
                        login = False
                        raise   Exception('Login failed')
                    url = 'https://politicsandwar.com/alliance/id=5049&display=taxes'
                    perms_data = {'nation_id':f'{nation_id}', 'bracket_id':f'{tax_id}', 'change_member_bracket':'Update Nation\'s Bracket'}
                    res2 = await session.get(url);
                    text = await res2.text()
#                    print((BeautifulSoup(text, 'html.parser')).find('input', {'name':'token'})['value'])
                    auth_token = (BeautifulSoup(text, 'html.parser')).find('input', {'name':'token'})['value']
                    perms_data.update({'token': auth_token})
                    await session.post(url, data=perms_data)
                    await session.close()
                if login == False:
                    await ctx.send('Failed to change their tax bracket')
                else:
                    await ctx.send('Successfully changed their tax bracket.')


async def setup(client):
	await client.add_cog(extras(client))