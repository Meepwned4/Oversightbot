import discord
from discord.ext import commands
import typing
import nest_asyncio
nest_asyncio.apply()
from OversightData import lesson_message, build

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

class rookie_program(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command(name='lesson', help='+lesson (number 1-6)')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'DisC')
    async def lesson(self, ctx, lesson: typing.Optional[str] = 'default'):
         if ctx.channel.category.name != '[The Harbour]':
             message = lesson_message(lesson)
             await ctx.send(message)
    
    @commands.command(name='beige', help='+beige')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'Citizen', 'Trainee')
    async def beige(self, ctx):
         if ctx.channel.category.name != '[The Harbour]':
             message = 'The only color bloc that offers protection to your nation; while on beige no new wars can be declared on you (and you cannot declare new wars).'
             embed = discord.Embed(title = 'Beige',
                              description = f'{message}', color=colors.dark_gold)
             await ctx.send(embed=embed)
    
    @commands.command(name='raiding_rules', help='+raiding_rules')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'Citizen', 'Trainee')
    async def raiding_rules(self, ctx):
         if ctx.channel.category.name != '[The Harbour]':
             message = '''
                 **Raiding/War Policy**:
    - Raid targets must not be in an alliance that is ranked in the top 50.
    - Targets must not be in an alliance protected or allied to a top 50 alliance.
    - Targets must not be in alliances we have treaties with.
    - If you are seeking to raid a nation in any alliance, ask @War Corps for approval with the nation link of your desired target.
    - Nations that are not in an alliance may be raided at will.
    - If you are ordered to peace out by a military officer, obey immediately.
     '''
             embed = discord.Embed(title = 'Raiding rules',
                              description = f'{message}', color=colors.dark_gold)
             await ctx.send(embed=embed)
    
    @commands.command(name='mass_infra', help='+mass_infra')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'Citizen', 'Trainee')
    async def mass_infra(self, ctx):
         if ctx.channel.category.name != '[The Harbour]':
             message = '<https://politicsandwar.com/cities/mass-infra-purchase/>'
             await ctx.send(message)
    
    @commands.command(name='mass_land', help='+mass_land')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'Citizen', 'Trainee')
    async def mass_land(self, ctx):
         if ctx.channel.category.name != '[The Harbour]':
             message = '<https://politicsandwar.com/cities/mass-land-purchase/>'
             await ctx.send(message)
             
    @commands.command(name='bulk', help='+bulk')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'Citizen', 'Trainee')
    async def bulk(self, ctx):
         if ctx.channel.category.name != '[The Harbour]':
             message = '<https://politicsandwar.com/cities/mass-land-purchase/>'
             message += '\n<https://politicsandwar.com/cities/mass-infra-purchase/>'
             await ctx.send(message)
             message = 'Use these tools to calculate the cost for 1k infrastructure/land.'
             message += '\nThen screenshot those and send them here.'
#             message += '\nhttps://media.discordapp.net/attachments/750164611499688026/912091985085628486/import_bulk.gif'
             await ctx.send(message)
    
    @commands.command(name='beige_cycle', help='+beige_cycle')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'Citizen', 'Trainee')
    async def beige_cycle(self, ctx):
         if ctx.channel.category.name != '[The Harbour]':
             message = '''
                 During a war, beige cycling is used to make sure that an enemy nation always has at least one war ongoing.
                 Since a nation gets 2 days (24 turns) of beige after each defeat, the attacking nations will take turns beiging the enemy.
                 Once that nation comes out of beige, more people will attack them before they are beiged again.
                 This leads to a beige “cycle”.
     '''
             embed = discord.Embed(title = 'Beige cycle',
                              description = f'{message}', color=colors.dark_gold)
             await ctx.send(embed=embed)
    
    @commands.command(name='overextension', help='+overextension')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'Citizen', 'Trainee')
    async def overextension(self, ctx):
         if ctx.channel.category.name != '[The Harbour]':
             message = '''
                 Overextension refers to when a nation attacks more nations than they can handle.
     '''
             embed = discord.Embed(title = 'Overextension',
                              description = f'{message}', color=colors.dark_gold)
             await ctx.send(embed=embed)
    
    @commands.command(name='import_file', help='+import', aliases=['import'])
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'Citizen', 'Trainee')
    async def import_file(self, ctx, gif: typing.Optional[str] = 'default'):
         if ctx.channel.category.name != '[The Harbour]':
                await ctx.send('https://media.discordapp.net/attachments/750164611499688026/912091985085628486/import_bulk.gif')

    @commands.command(name='build_oil', help='+build_oil')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'Interviewer', 'Trainee')
    async def build_oil(self, ctx):
         if ctx.channel.category.name == '[Admission & Training]':
             rss = 'oil'
             import_build = build(rss)
             await ctx.send(import_build)
    
    @commands.command(name='build_coal', help='+build_coal')
    @commands.has_any_role('Pentarch', 'Elder', 'Suffet', 'Adirim', 'Interviewer', 'Trainee')
    async def build_coal(self, ctx):
         if ctx.channel.category.name == '[Admission & Training]':
             rss = 'coal'
             import_build = build(rss)
             await ctx.send(import_build)
#    '''
#    What is beige?
#    A nation defeated gets 2 more days of being on the beige color. Beige protects from new war declarations. We want to have active enemies always in war, so they don't have the opportunity to build back up.
#    
#    Tips for avoiding unnecessary attacks:
#     - Don't open with navals if they have units which are a threat. Ships can't attack planes, tanks or soldiers.
#     - Dont naval if you already have them blockaded
#     - Never airstrike infra, cash, or small amounts of units - wait for them to build more units
#     - If they just have some soldiers and can't get a victory against you, don't spam ground attacks.
#     - If the enemy only has soldiers (no tanks) and you have max planes. Airstriking soldiers kills more soldiers than a ground attack will.
#     - Missiles/Nukes do NOT kill any units
#    
#    note: You can do some unnecessary attacks if the war is going to expire, or you need to beige them as part of a beige cycle
#    
#    What is beige cycling?
#    Beige cycling is when we have a weakened enemy, and 3 strong nations declared on that enemy - then 1 nation defeats them, whilst the other two sit on them whilst they are on beige
#    When their 2 days of beige from the defeat ends, another nation declares on the enemies free slot and the next nation defeats the enemy.
#    
#    Beige cycling checklist:
#    1. Is the enemy military mostly weakened/gone?
#    2. Is the enemy not currently on beige?
#    3. Do they have 3 defensive wars, with the other two attackers having enough military?
#    4. Are you the first person to have declared?
#    
#    Tip: Save your MAP. Avoid going below 40 resistance until you are GO for beiging them
#    
#    Allowed beige reasons:
#     - NOT_AN_ENEMY: Non enemies are not subject to beige/cycle orders
#     - DO_NOT_RAID: Try to peace nations that are on the Do Not Raid list
#     - LOW_RESISTANCE: Low resistance, at risk of getting beiged
#     - BEIGE_CYCLE_4D: If the enemy does not have beige, and one other strong nation can sit them whilst beige for 4d. DO NOT BEIGE DEFENSIVE WARS
#    - INACTIVE: Nations who are inactive (2 days)
#     - NO_RECENT_WARS: Enemy is has not declared a war in the past 20 days
#     - NO_RECENT_3_CONSECUTIVE_LOGINS: Enemy has not had 3 consecutive logins in the past 120 days
#     - APPLICANT: Applicants aren't subject to beige/cycle orders
#     - NO_RECENT_5_CONSECUTIVE_LOGINS: Enemy has not had 5 consecutive logins in the past 120 days
#     - MISSILE_TURRET: Enemies with high number of missiles
#     - USELESS: Enemy has no recent wars and no recent consecutive logins OR incorrect MMR
#     - BEIGE_CYCLE: If the enemy does not have beige, and two other strong nations can sit them whilst beige. DO NOT BEIGE DEFENSIVE WARS
#     - VACATION_MODE: You can beige enemies in Vacation Mode
#     - INCORRECT_ENEMY_MMR: Enemy does not have 5 barracks/factories
#     - NUKE_TURRET: Enemies with high numbers of nukes
#     - BEIGE_CYCLE_1: If the enemy does not have beige, and one other strong nation can sit them whilst beige for 2d. DO NOT BEIGE DEFENSIVE WARS
#     - ALREADY_BEIGE_STACKED: Enemies already with enough beige to rebuild (6 days)
#     - BLOCKADED: If you are being sat on/blockaded and need to restock on warchest
#    '''

def setup(client):
	client.add_cog(rookie_program(client))