import nextcord
from nextcord import SlashOption
from nextcord.ext import commands   # this is new didnt know about nextcord.ext
import os
from dotenv import load_dotenv
from profile_builderV3 import profile_database
import time
import asyncio

from typing import Optional

print(dir(profile_database))

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_MARE_BOT')
GUILD = os.getenv('DISCORD_GUILD')

intents = nextcord.Intents.all()
intents.members = True
intents.message_content = True

#bot = commands.Bot(command_prefix= '$') # removed when @bot.command was acting lame af

client = nextcord.Client(intents=intents)
guild = nextcord.utils.find(lambda g: g.name == GUILD, client.guilds)
startTime = time.time()

list_of_admins = ["MareBear#7504", "Regulus#8269", "gilcraos#2111"]

database = profile_database()
print("***database:\n", database)
profiles = database._get_user_profiles()
print("***profiles:\n", profiles, "\nvs profile_data_dir_exist\n", database.initial_creation_of_profiles)


# admin commands:
def admin_commands(message):
    pass

# member commands:
def member_commands(message):
    pass


# verifies bot is online
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    for member in client.get_all_members():
        print(member)


# trying out how to use commands AND embeds
# at present im following the guides, videos and posts to a T...but im still getting fucked because of some issue with message_content not being enabled...WHEN IT LITERALLY IS


#attempt 3 -- works, but not "amazing"
# i got this to work for the most part... but i think it would be FAR smarter and more secure to get the message_command to work.
''''''
@client.event
async def on_message(message):
    if message.author != client.user:
        print(message)
        print(message.author)
        embed = nextcord.Embed(title = message.author, color = nextcord.Color(9106754))    # RGB hexadecimal tuple : (138,245,66) aka (8AF542)
        embed.add_field(name = "ID", value = message.content, inline= True)
        await message.channel.send(embed = embed)

# ************************* MAJOR SECTION *************************
#attempt 4
# using the slash_commands
@client.slash_command(guild_ids = [guild])
async def ping(interaction = nextcord.Interaction):
    """Simple Command that responds with Pong!"""
    await interaction.response.send_message("Pong!")

@client.slash_command(guild_ids = [guild])
async def echo(interaction : nextcord.Interaction, arg: str):
    '''
    Repeats your message that you send as an argument

    Parameters
    ----------
    interaction: Interaction
        The interaction object
    arg: str
        The message to repeat. This is a required argument.
    '''
    await interaction.response.send_message(f'Parroting: {arg}')

@client.slash_command(guild_ids = [guild])
async def echo_number(
    interaction : nextcord.Interaction,
    number: Optional[int] = SlashOption(required = False)
):
    """Repeats your number that you send as an argument

    Parameters
    ----------
    interaction: Interaction
        The interaction object
    arg: Optional[int]
        The number to repeat. This is an optional argument.
    """
    if number is None:
        await interaction.response.send_message("You didn't specify a number!")
    else:
        await interaction.response.send_message(f"You said: {number}")


'''
CHOICES
You can also use choices to make fields that only accept certain values.

The choices can be specified using choices in a SlashOption
which can be a list of choices or a mapping of choices to their values.
'''
@client.slash_command(guild_ids = [guild])
async def choose_a_number(
    interaction: nextcord.Interaction,
    number: int = SlashOption(
        name ="picker",
        choices = {"one":1, "two":2, "three": 3},
    ),
):
    """Repeats your number that you choose from a list

    Parameters
    ----------
    interaction: Interaction
        The interaction object
    number: int
        The chosen number.
    """
    await interaction.response.send_message(f"You chose {number}!")

@client.slash_command(guild_ids = [guild])
async def hi(interaction: nextcord.Interaction, user: nextcord.Member):
    """Say hi to a user

    Parameters
    ----------
    interaction: Interaction
        The interaction object
    user: nextcord.Member
        The user to say hi to.
    """
    await interaction.response.send_message(
        f"{interaction.user} just said hi to {user.mention}"
    )

# subcommands in slash_command
@client.slash_command(guild_ids=[guild])
async def main(interaction: nextcord.Interaction):
    """
    This is the main slash command that will be the prefix of all commands below.
    This will never get called since it has subcommands.
    """
    pass


@main.subcommand(description="Subcommand 1")
async def sub1(interaction: nextcord.Interaction):
    """
    This is a subcommand of the '/main' slash command.
    It will appear in the menu as '/main sub1'.
    """
    await interaction.response.send_message("This is subcommand 1!")


@main.subcommand(description="Subcommand 2")
async def sub2(interaction: nextcord.Interaction):
    """
    This is another subcommand of the '/main' slash command.
    It will appear in the menu as '/main sub2'.
    """
    await interaction.response.send_message("This is subcommand 2!")


@main.subcommand()
async def main_group(interaction: nextcord.Interaction):
    """
    This is a subcommand group of the '/main' slash command.
    All subcommands of this group will be prefixed with '/main main_group'.
    This will never get called since it has subcommands.
    """
    pass


@main_group.subcommand(description="Subcommand group subcommand 1")
async def subsub1(interaction: nextcord.Interaction):
    """
    This is a subcommand of the '/main main_group' subcommand group.
    It will appear in the menu as '/main main_group subsub1'.
    """
    await interaction.response.send_message("This is a subcommand group's subcommand!")


@main_group.subcommand(description="Subcommand group subcommand 2")
async def subsub2(interaction: nextcord.Interaction):
    """
    This is another subcommand of the '/main main_group' subcommand group.
    It will appear in the menu as '/main main_group subsub2'.
    """
    await interaction.response.send_message("This is subcommand group subcommand 2!")

# context menu slash_commands
@client.user_command(guild_ids=[guild])
async def hello(interaction: nextcord.Interaction, member: nextcord.Member):
    """Says hi to a user that was right-clicked on"""
    await interaction.response.send_message(f"Hello {member}!")

@client.message_command(guild_ids=[guild])
async def say(interaction: nextcord.Interaction, message: nextcord.Message):
    """Sends the content of the right-clicked message as an ephemeral response"""
    await interaction.response.send_message(message.content, ephemeral=True)

# deferred response (discord requires responses in 3 seconds, but you can extend that by deferring and then sending followup in the next 15 min)
# responding with defer() will show the bot is thinking message to the user until the followup response is sent.
# note: by default the message will by public, but you can make it visible only to the user by setting the ephemeral parameter to True
@client.slash_command(guild_ids=[guild])
async def hi_there(interaction: nextcord.Interaction):
    """Say hi to a user"""
    # defer the response, so we can take a long time to respond
    await interaction.response.defer()
    # do something that takes a long time
    await asyncio.sleep(5)
    # followup must be used after defer since a response is already sent
    await interaction.followup.send(f"Hi {interaction.user}! Thanks for waiting!")

# application commands in cogs (https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html#:~:text=There%20comes%20a%20point%20in,Python%20class%20that%20subclasses%20commands.)



# DEVELOPMENT SPACE FOR PROFILE BUILDER
# profile generation
'''
def actualize_profile():
    embed = nextcord.Embed(title = "moose gallery", description= "smol moose boi", color = nextcord.Color((138,245,66)))
    embed.add_field(name = "ID", value = "moose id", inline= True)
    await 
'''
# create new profile for user
# INFO:
# BUG FIXED  -- i was getting a "application did not respond" error for a WHILE because i had the nextcord.interaction parameter AFTER nextcord.Member
# and apparently the description must be less than 100 characters.
#  Each user may only have up to TWO profiles. \n One for dating, and one for standard server activities.
# \n After using this command you need to edit your profile by using the:\n /profile_name, /profile_type, /age_range, /gender, /pronouns, and /about_me
# \n commands to fill in your user profile.\n You can also see what your profile currently contains with /view_profile")
@client.slash_command(guild_ids= [guild], description = "This creates a new profile for a user.")
async def create_profile(interaction: nextcord.Interaction):    
    #FINALLY WORKED AFTER instantiating profile_database() and banging my head against the wall for 2 days
    #database = profile_database()

    print("database from csv: ", database._get_user_profiles())
    print("***Interaction.user: ", interaction.user)
    add_name = interaction.user.name + "#" + interaction.user.discriminator
    local_profiles = database.create_new_profile(existing_user_data = database._get_user_profiles(), profile_name= add_name)   # create new empty profile
    print("profiles to update:\n", local_profiles)
    database._set_user_profiles(local_profiles)
    database.update_profile_csv()
    
    await interaction.response.send_message(
        f"Created {interaction.user}'s profile!"
    )
    private = await interaction.user.create_dm()
    await private.send(""""Each user may only have up to TWO profiles. \n One for dating, and one for standard server activities.
        \n After using this command you need to edit your profile by using the:\n /profile_name, /profile_type, /age_range, /gender, /pronouns, and /about_me
        \n commands to fill in your user profile.\n You can also see what your profile currently contains with /view_profile") """)



client.run(TOKEN)

# this can be bundled up above in: https://stackoverflow.com/questions/64844786/run-another-function-when-any-command-is-called-discord-py
'''
test = client.guilds
print ("After test result:", test)
'''