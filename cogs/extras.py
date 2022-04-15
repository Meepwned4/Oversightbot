import discord
from discord.ext import commands
import requests
import aiohttp
from bs4 import BeautifulSoup
import OversightData

#class Select(discord.ui.Select):
#    def __init__(self):
#        options=[
#            discord.SelectOption(label="Option 1",emoji="👌",description="This is option 1!"),
#            discord.SelectOption(label="Option 2",emoji="✨",description="This is option 2!"),
#            discord.SelectOption(label="Option 3",emoji="🎭",description="This is option 3!")
#            ]
#        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)
#    async def callback(self, interaction: discord.Interaction):
#        if self.values[0] == "Option 1":
#            await interaction.response.send_message("1", ephemeral=False)
#        elif self.values[0] == "Option 2":
#            await interaction.response.send_message("2",ephemeral=False)
#        elif self.values[0] == "Option 3":
#            await interaction.response.send_message("3",ephemeral=False)
##            await interaction.response.edit_message(content="1")
##        elif self.values[0] == "Option 2":
##            await interaction.response.send_message("2",ephemeral=False)
##        elif self.values[0] == "Option 3":
##            await interaction.response.send_message("3",ephemeral=True)
#
#class SelectView(discord.ui.View):
#    def __init__(self, *, timeout = 180):
#        super().__init__(timeout=timeout)
#        self.add_item(Select())

class extras(commands.Cog):

    def __init__(self, client):
        self.client = client
        client = self.client

#    @commands.command(name='menu', help='+menu')
#    @commands.has_any_role('Pentarch', 'Elder', 'Suffet')
#    async def menu(self, ctx):
#        member = None
#        num = 8
#        words = OversightData.interview_question(num, member)
#        await ctx.send(words,view=SelectView())


    @commands.command(name='tax_bracket', help='+tax_bracket 92845 100', aliases=['tax', 'taxes'])
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet')
    async def tax_bracket(self, ctx, nation, tax):
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


def setup(client):
	client.add_cog(extras(client))