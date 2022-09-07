# bot2.py

# NOTE BEYOND IMPORTANT: https://discordpy.readthedocs.io/en/stable/api.html#discord-api-events
# these are the client.event coroutines that async can be listening for and responding to (un)
import os
from ssl import CHANNEL_BINDING_TYPES

import discord
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


intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)  # enables all intents

guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
startTime = time.time()

'''
class CustomClient(discord.Client):
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
    # await member.dm_channel.send(file = discord.File('moo.png'))  -- broke after updating pylance 5/3 8:04pm
    await member.dm_channel.send(file = discord.File(sampleimage))

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
        # await message.channel.send(file = discord.File('moo.png')) # FIXME this was LITERALLY working 100% fine the other day now it isnt...wtf 5/3/22 8:41pm
        await message.channel.send(file = discord.File(sampleimage))
    else:
        print("cow NOT recognized")

# WORKS!!
@client.event
async def on_typing(channel, typist, typing):
    if isinstance(channel, discord.TextChannel):
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
    await payload.send()

    
'''
    if "!bigmoo" == message:
    target = message.author
    await target.create_dm()
    count = 3
    while count > 0:
        await target.dm_channel.send(file = discord.File('moo.png'))
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