# bot3.py -- because discord.py becoming deprecated april 2022. had to get nextcord via python3 -m pip install -U nextcord

# NOTE BEYOND IMPORTANT: https://discordpy.readthedocs.io/en/stable/api.html#discord-api-events
# these are the client.event coroutines that async can be listening for and responding to (un)
import os
from ssl import CHANNEL_BINDING_TYPES

import nextcord
from dotenv import load_dotenv
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

current_dir = __file__
this_file = os.path.dirname(__file__)
print(this_file + "/moo.png")

# not going to use this because it was turbo specific to this one file name... but still interesting none the less
# current_dir = current_dir[0:-7]
# print(current_dir)

sampleimage = this_file + "/moo.png"    # GOT IT TO WORK. I had to make this a string proper


intents = nextcord.Intents.default()
intents.members = True
client = nextcord.Client(intents = intents)  # enables all intents

guild = nextcord.utils.find(lambda g: g.name == GUILD, client.guilds)
# for some reason guild is None... im likely using it wrong, but at present, you cant use 'guild' for anything since it throws a big fat 'None' at you -- 7/19/22
# 7/20/22 i just realized... this hasn't been executed yet because client.run(TOKEN) hasn't been called yet. mare-bot.py has some solutions to this iirc...

startTime = time.time()

'''
class CustomClient(nextcord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
'''

'''
(method) event: (coro: Any) -> Any
A decorator that registers an event to listen to.

You can find more info about the events on the documentation below <discord-api-events>.

The events must be a coroutine <coroutine>, if not, TypeError is raised.

Example
. code-block:: python3

    @client.event async def on_ready():
        print('Ready!')
'''

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    elapsed = time.time() - startTime
    print(elapsed)


@client.event
async def on_member_join(member):
    await member.create_dm()
    elapsed = time.time() - startTime
    print(elapsed)

    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Bot Testing Server!'
    )
    elapsed = time.time() - startTime
    print(elapsed)

    # note to self. bot doesnt like to send TEXT + an IMAGE at the same time... but it has no qualms doing it as separate ACTIONS :D
    # await member.dm_channel.send(file = nextcord.File('moo.png'))  -- broke after updating pylance 5/3/22 8:04pm
    await member.dm_channel.send(file = nextcord.File(sampleimage))

# experimenting -- doesnt work
# FIXED typo on_mesage vs on_meSSage (emphasis on the fact that i didnt type the second s of message)

@client.event
async def on_message(message):
    if message.author == client.user:
        print("somehow message was tied to the bot")
        return
    print("inside on_message")

    if message.content.lower() == '!cow':
        print("cow recognized")
        # await message.channel.send(file = nextcord.File('moo.png')) # FIXME this was LITERALLY working 100% fine the other day now it isnt...wtf 5/3/22 8:41pm
        await message.channel.send(file = nextcord.File(sampleimage))
    else:
        print("cow NOT recognized")

# WORKS!!
@client.event
async def on_typing(channel, typist, typing):
    if isinstance(channel, nextcord.TextChannel):
        print("this IS a text channel~")
    await channel.send(f"it appears that {typist} has something to say :eyes:")


# this only works on messages' reactions sent while the bot was active
'''
@client.event
async def on_reaction_add(reaction, user):
    print(f"{user} posted the {reaction} emoji")
'''

# this works on ALL reactions ever. plus payload has a TON of useful info baked in Example:
# <RawReactionActionEvent message_id=971586512904945714 user_id=184855771811414016 channel_id=968244973038362627 guild_id=968244973038362624
# emoji=<PartialEmoji animated=False name='😂' id=None>
# event_type='REACTION_ADD' member=<Member id=184855771811414016 name='Regulus' discriminator='8269' bot=False nick=None
# guild=<Guild id=968244973038362624 name='bot testing' shard_id=None chunked=True member_count=5>>>
@client.event
async def on_raw_reaction_add(payload):
    print(f"full payload:{payload}\n\ntruncated payload:{payload.guild_id} {payload.emoji.animated}")   #WORKS LIKE A CHARM
    
    # WORKS! just make sure you get the channel_id before you try to use the await .send()... payload is super useful because you can easily grab that info from the payload
    channel = client.get_channel(payload.channel_id)
    await channel.send(f"looks like {payload.member.name}#{payload.member.discriminator} added the {payload.emoji.name} reaction")

    
'''
    if "!bigmoo" == message:
    target = message.author
    await target.create_dm()
    count = 3
    while count > 0:
        await target.dm_channel.send(file = nextcord.File('moo.png'))
        count -= 1
'''


# given sample code -- works
'''
@client.event
async def on_message(message):
    if message.author == client.user:
        print("mess up")
        return
    print("made it past author")

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '99!':
        print("made it into message.content")
        import random
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)
'''  


client.run(TOKEN)