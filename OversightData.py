import json
import pickle
import requests

left_arrow = '⬅' # left arrow emoji
right_arrow = '➡' # right arrow emoji
robot = '🤖' # robot emoji
person = '🧑' # person emoji

pickle_off = open('./data/api_key.pickle', 'rb')
apikeys = pickle.load(pickle_off)
apikeys = apikeys.split(',')
token = 'NzM1MjU3Mzc3NjA3MjU0MTE3.Xxdnyw.yCKnVzcCHxY_vS5GMelz2ElqSXs'
oversight_channel_id = 812131124489879552
disc_channel_id = 605910228692893726
test_oversight_channel_id = 736099358344478764
test_disc_channel_id = 834653321099739177
carthago_server_id = 567336454632636416
nerds_id = 712071416505172090
raider_id = 853790553375768586

def data_storage(memberdata):
    with open('./data/memberdata.json', 'w') as outfile:
        json.dump(memberdata, outfile)
    return memberdata

def data_retrieval(oldmemberdata):
    data = open('./data/memberdata.json')
    if data:
        oldmemberdata = json.load(data)
    return oldmemberdata

def merge_memberdata(memberdata, oldmemberdata, list_of_dics):
    if not oldmemberdata:
        oldmemberdata = memberdata
    for dic1 in oldmemberdata:
        for dic2 in memberdata:
            if dic1.get('nationid') == dic2.get('nationid'):
                for dic3 in list_of_dics:
                    if dic2.get('nationid') == dic3.get('_id'):
                        dic2.update({'DiscordID':dic3.get('DiscordID')})
                dic2['ping'] = dic1.get('ping')
                dic2['war_status'] = dic1.get('war_status')
                dic2['ChannelID'] = dic1.get('ChannelID')
                dic2['Trainee'] = dic1.get('Trainee')
            else:
                continue
    return memberdata


def lesson_message(lesson):
    if lesson == '1' or lesson == 'one':
        message = 'https://docs.google.com/document/d/1XICmeGQ9zLiGjZ9oKAGeOKtgcpBEn6lz-kgCFFaNoN4/edit'
    elif lesson == '2' or lesson == 'two':
        message = 'https://docs.google.com/document/d/1VipevfZ1R590BJWQeFgUKy-q50_dnU-tx_QobbsKRf0/edit'
    elif lesson == '3' or lesson == 'three':
        message = 'https://docs.google.com/document/d/1i8XUd93uQtygUW_3rD7wZCnr5cbgdhUgRWy6UUs5qV0/edit'
    elif lesson == '4' or lesson == 'four':
        message = 'https://docs.google.com/document/d/1IJ7ioQqHGGncMeyckgq_yoxmjhuluzZMnLRp8j1pAaI/edit'
    elif lesson == '5' or lesson == 'five':
        message = 'https://docs.google.com/document/d/1RZZV6SlX6eWRD7TLS8y3HZKunrgHbsnoV6-t67s7qa8/edit'
    elif lesson == '6' or lesson == 'six':
        message = 'https://docs.google.com/document/d/1R9DCHjdyjtLZOCpVjUbWx3C4AbBf2NE0GfHRGEYuXxw/edit'

    return message

def build(build):
    if build == 'coal':
        message = '''{
    "infra_needed": 1000,
    "imp_total": 20,
    "imp_coalpower": 2,
    "imp_oilpower": 0,
    "imp_windpower": 0,
    "imp_nuclearpower": 0,
    "imp_coalmine": 5,
    "imp_oilwell": 0,
    "imp_uramine": 0,
    "imp_leadmine": 0,
    "imp_ironmine": 0,
    "imp_bauxitemine": 0,
    "imp_farm": 0,
    "imp_gasrefinery": 0,
    "imp_aluminumrefinery": 0,
    "imp_munitionsfactory": 0,
    "imp_steelmill": 0,
    "imp_policestation": 1,
    "imp_hospital": 0,
    "imp_recyclingcenter": 1,
    "imp_subway": 0,
    "imp_supermarket": 0,
    "imp_bank": 0,
    "imp_mall": 0,
    "imp_stadium": 0,
    "imp_barracks": 5,
    "imp_factory": 0,
    "imp_hangars": 5,
    "imp_drydock": 1
}'''
        return message
    elif build == 'oil':
        message = '''{
    "infra_needed": 1000,
    "imp_total": 20,
    "imp_coalpower": 0,
    "imp_oilpower": 2,
    "imp_windpower": 0,
    "imp_nuclearpower": 0,
    "imp_coalmine": 0,
    "imp_oilwell": 5,
    "imp_uramine": 0,
    "imp_leadmine": 0,
    "imp_ironmine": 0,
    "imp_bauxitemine": 0,
    "imp_farm": 0,
    "imp_gasrefinery": 0,
    "imp_aluminumrefinery": 0,
    "imp_munitionsfactory": 0,
    "imp_steelmill": 0,
    "imp_policestation": 1,
    "imp_hospital": 0,
    "imp_recyclingcenter": 1,
    "imp_subway": 0,
    "imp_supermarket": 0,
    "imp_bank": 0,
    "imp_mall": 0,
    "imp_stadium": 0,
    "imp_barracks": 5,
    "imp_factory": 0,
    "imp_hangars": 5,
    "imp_drydock": 1
}'''
        return message
def interview_message(num, user):
    message = ''
    reminder = f'If at any time you\'d like to be interviewed by a human, react with {person} \n' \
    + f'**After** you\'ve answered, react with {right_arrow} to continue'
    if num == '0':
        message = (' This will be a simple 5-10 minute text interview about your time ' \
                        + 'so far in the game and to give you a sense of our alliance policies and format.\n\n' \
                        + f'If at any time you\'d like to be interviewed by a human, react with {person} \n' \
                        + f'React with {right_arrow} to begin the automated interview')
    if num == '1':
        try:
            discord_id = user.id
#            discord_id = 175719252995604480
            user = requests.get(
            f'http://24.117.204.187:8080/discord/?DiscordID={discord_id}&key=davethsmellskrampuswhales')
            user = user.json()
            user = user[0]
            nation_id = user.get('_id')
            leader = user.get('leader')
            nation_name = user.get('name')
            nation_link = f'https://politicsandwar.com/nation/id={nation_id}' 
            
            message = (f'My sources tell me that the nation {nation_name} led by {leader} at the link {nation_link} is your nation.\n' \
                           + 'Is this correct? If not, what is the link to your nation?\n\n' \
                           + reminder)
        except:
            message = ('Could I get a link to your Nation page?\n' \
                       + 'If you can\'t find it, go to your nation page' \
                       + ' and copy/paste your nation ID.\n\n' \
                       + reminder)
    if num == '2':
        message = ('How did you find out about Carthago? What led you to apply?\n\n' \
                       + reminder)
    if num == '3':
        message = ('Have you ever been involved in another alliance ' \
                       + 'on Politics and War, either under this account or' \
                       + ' another account?\n\n' + reminder)
    if num == '4':
        message = ('How long have you been playing Politics and War? Have you had' + \
                   ' any gaming experience in similar games?\n\n' + reminder)
    if num == '5':
        message = ('Do you have any standing debts to anyone in the game?\n\n' \
                       + reminder)
    if num == '6':
        message = ('What would you consider your greatest skills? These can be ' \
                       + 'in games or IRL which translate into the game, such as GFX ' \
                       + '(Photoshop, GIMP, etc), Video editing, Diplomacy, Spreadsheet ' \
                       + 'or Coding.\n\n' \
                       + reminder)
    if num == '7':
        message = ('What would you consider your worst weaknesses?\n\n' \
                   + reminder)
    if num == '8':
        message = ('''Now, please select one of the following, or use your own words to best describe what your activity would look like: 
 
- I will login once a week. I would like the protection and economic benefits that CTO offers, and I will fight in wars for the Alliance, but I don't really want a job or be particularly involved the community.
 
- I will login at least once or twice a day. I want to be moderately active in the CTO community. I will be active on Discord whenever possible and participate when I'm able.

- I would like to be as active as I'd like, while building my Nation and income at peace and I'm just here so I don't get raided.

- I will log in multiple times every single day. I want to be extremely active and contribute in whatever capacity I can within the CTO community. I will frequent the Discord channels and would like to work my way up to a leadership position in the future.\n\n''' \
+ reminder)
    if num == '9':
        message = ('''If you were given the opportunity to choose a government department to work in, considering the descriptions provided, which would you choose?
 
- **War Department**: Defense during peacetime and wartime, making sure members meet minimum military requirements, monitoring conflicts across Orbis and assisting with Foreign Affairs when necessary; ensuring warchests are kept stocked.
 
- **Foreign Affairs Department**: Diplomacy among allies and other parties; posting in forums and keeping up the Carthago public image; constant intelligence gathering and maintenance of contacts via social interaction.
 
- **Tech Department**: Maintaining our alliance stat sites, discord bots and sheets/scripts. Having an intermediate coding knowledge and a level of alliance seniority/trust (to prevent corporate espionage) is a requirement to entry.

- **Discipline Department**: Helping mentor other members, especially new members; helping members maximise income; ensuring warchests are kept up to date and ensuring members are active, aware and following alliance policies. Ensuring the smooth running of the alliance (jack-of-all trades).

- **Culture Department**: Creating graphics, such as banners and flags for the Alliance and making sure members are active and having fun with events and activities; managing our Discord channel; keeping our Wiki up-to-date and looking good. 
 
- **Treasury Department**: Providing loans and grants to members; managing the alliance’s taxes and resources through trade routes with other alliances; helping members maximize income.
 
If you aren't interested in any of these, that’s okay, just say so. If you have ideas for other government positions we should be offering, feel free to bring this up after this interview.\n\n''' \
+ reminder)
    if num == '10':
        message = ('''
With your answer in mind, which among the following or using your own words, would you consider the most interesting aspects which drew you to the game? Which would you consider the least interesting? 

- Staying at peace, building my nation, trading and growing my income.
 
- Fighting in wars against other Nations and Alliances.

- Working in the environment of an organized Alliance government.

- Making friends and being part of a community.

- Raiding inactive nations for money and resources. Arrgh!

- Becoming a politically influential, well-known player.\n\n''' + reminder)
    if num == '11':
        message = [('''
 These Terms and Conditions constitute a legally binding agreement, between yourself and the alliance, by which you agree to be bound by terms and conditions herein stated. 

**- Economics -**
Our economic policy includes taxes which are determined by your size and primarily by your choice. We provide the best within the two avenues of economic development, with your prosperity and freedom to choose in mind above all. While it is highly recommended that you join our growth cycles (that is, communist taxes), provided your nation has City 17+ you may choose 10/10 tax rates.

Our Treasury Department will work with you to maximize your income, within the confines of our recommended nation builds. We will help you with your nation builds and will allow some flexibility within reason. Inquire with our gov and have a look at the econ-updates channel for more detailed info.

Any grants received by the time that you leave the AA shall be seen as debt. This debt will be calculated based on the taxes you paid versus the Grants and Aid you received (subtracted by said taxes). These will have to be repaid by you or the AA you are staying at. If no agreement on this can be made and/or no payment is received. It shall serve as a valid Casus Belli against you. Raiding shall ensue until satisfaction or recovery of the debt amount.

**- New Nations -** 
New nations are expected to take the time to read guides and listen to assigned mentors while they raid until they get to 10 Cities. After that is done, they are eligible to join our growth cycle program, previously mentioned, being taxed at 30/30 in the meantime. This is subject to change, depending on if we are in wartime or at peace.           
        '''), ('''
**- Responsibilities -** 
The respective departments of government enforce our Minimum Military Requirements (MMR) and Warchest (WC), Citizens will be told the level of MMR they should be expected to maintain, dependent on the state of affairs in Orbis (e.g. peace/war/high alert). 
 
You will be encouraged to be involved and take on as much responsibility in the different government departments and in the community as you are comfortable with, subject to promotion based on good performance. 

Our policies on Raids must be followed strictly. If you are unsure if your intended target is allowed, ask War Corps in war-general. 

You are encouraged to log on every 3 days. You must be active in-game at least once every 7 days in game or you will be set to applicant and if your nation turns purple in-game, you will be removed from the alliance. This policy is enforced at the discretion of the Discipline and Oversight department. Fighting actively in alliance wars is mandatory, should you opt to go into vacation mode without warning and without just cause, as determined by the Oversight Department, you will be removed from the alliance. If you take any other actions deemed detrimental to the alliance, you will be removed, with just cause given to you to explain the decision.

We hope to see you on Discord as much as your time commitments allow, but you must check Discord whenever an @ everyone ping is made. This can be a mandatory call to arms and we need our members to be responsive, in the event of an emergency

---
If you have any questions, comments, or concerns, please let us know. Otherwise, state you agree to these terms.\n\n'''
+ reminder)]
    if num == '12':
        message = ('For coordination purposes, what\'s your Timezone?\n\n' + reminder)
    if num == '13':
        message = ('That was the last question, a human should be along soon to review your interview.')
        
    return message

def nagging_message(num):
    if num == 1:
        query = '''{
  alliances(id: [5049], first: 1) {
    data {
      id
      name
      nations {
        id
        vacation_mode_turns
        score
        last_active
        nation_name
        alliance_position
        num_cities
        cities {
          id
          name
          infrastructure
          land
          powered
          oil_power
          wind_power
          coal_power
          nuclear_power
          coal_mine
          oil_well
          uranium_mine
          barracks
          farm
          police_station
          hospital
          recycling_center
          subway
          supermarket
          bank
          shopping_mall
          stadium
          lead_mine
          iron_mine
          bauxite_mine
          oil_refinery
          steel_mill
          munitions_factory
          factory
          hangar
          drydock
          nuke_date
        }
        mass_irrigation
        color
        continent
        leader_name
        domestic_policy
        war_policy
        wars {
          date
          id
          war_type
          turns_left
          naval_blockade
          att_id
          att_alliance_id
          att_gas_used
          att_mun_used
          att_alum_used
          att_steel_used
          att_resistance
          att_money_looted
          att_missiles_used
          att_points
          att_resistance
          att_money_looted
          att_infra_destroyed_value
          att_soldiers_killed
          att_aircraft_killed
          def_id
          def_alliance_id
          def_resistance
          air_superiority
          ground_control
          naval_blockade
        }
      }
    }
  }
}'''
        
    if num == 2:
         query = '''{
  alliances(id: [5049], first: 1) {
    data {
      id
      name
      nations {
        id
        vacation_mode_turns
        score
        last_active
        nation_name
        alliance_position
        color
        continent
        leader_name
        domestic_policy
        war_policy
        wars {
          date
          id
          war_type
          turns_left
          attacker{
            id
            alliance_id
            alliance_position
            war_policy
            num_cities
            cities{
              infrastructure
              powered
              oil_power
              oil_well
              coal_power
              coal_mine
              nuclear_power
              uranium_mine
              wind_power
              barracks
              hangar
              factory
              drydock
            }
          	continent
            update_tz
            population
            beige_turns
            score
            espionage_available
          }
          defender{
            id
            alliance_id
            alliance_position
            war_policy
            num_cities
            cities{
              infrastructure
              powered
              oil_power
              oil_well
              coal_power
              coal_mine
              nuclear_power
              uranium_mine
              wind_power
              barracks
              hangar
              factory
              drydock
            }
          	continent
            update_tz
            population
            beige_turns
            score
            espionage_available
          }
          attacks {
            date
            war_id
            id
            att_id
            attcas1
            attcas2
            att_mun_used
            att_gas_used
            aircraft_killed_by_tanks
            money_stolen
            loot_info
            resistance_eliminated
            def_id
            defcas1
            defcas2
            city_id
            city_infra_before
            infra_destroyed
            infra_destroyed_value
            improvements_lost
            def_mun_used
            def_gas_used
            victor
          }
          att_id
          att_gas_used
          att_mun_used
          att_alum_used
          att_steel_used
          att_resistance
          att_money_looted
          att_missiles_used
          att_points
          att_resistance
          att_money_looted
          att_infra_destroyed_value
          att_soldiers_killed
          att_aircraft_killed
          def_id
          air_superiority
          ground_control
          naval_blockade
        }
      }
    }
  }
}'''

    return query
