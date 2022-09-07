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
print("***profiles:\n", profiles, "\nvs profile_data_dir_exist\n", database.initial_profile_state)


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



# DEVELOPMENT SPACE FOR PROFILE BUILDER
# profile generation


# create new profile for user
# INFO:
# BUG FIXED  -- i was getting a "application did not respond" error for a WHILE because i had the nextcord.interaction parameter AFTER nextcord.Member
# and apparently the description must be less than 100 characters.
#  Each user may only have up to TWO profiles. \n One for dating, and one for standard server activities.
# \n After using this command you need to edit your profile by using the:\n /profile_name, /profile_type, /age_range, /gender, /pronouns, and /about_me
# \n commands to fill in your user profile.\n You can also see what your profile currently contains with /view_profile")
@client.slash_command(guild_ids= [guild], description = "This creates a new profile for a user.")
async def create_profile(interaction: nextcord.Interaction):    
    # i might have to save the user's ID too in case they change usernames

    print("database from csv: ", database._get_user_profiles())
    print("***Interaction.user: ", interaction.user)
    add_name = interaction.user.name + "#" + interaction.user.discriminator

    # FIXED BUG, the issue with all data columns being empty AND them overwriting the existing data entries
    # every time bot is turned on!
    # changed existing_user_data = database._get_user_profiles() to database.parse_existing_user_data()
    local_profiles = database.create_new_profile(existing_user_data = database.parse_existing_user_data(), profile_name= add_name)   # create new empty profile
    
    print("local_profiles variable (ie need to save this to csv):\n", local_profiles)
    database._set_user_profiles(local_profiles)
    database.update_profile_csv()
    
    '''
    # TEMPORARILY REMOVED (7/30/22 @ 5:07am) because this was flooding my dm's while i was testing

    await interaction.response.send_message(
        f"Created {interaction.user}'s profile!"
    )
    private = await interaction.user.create_dm()
    await private.send(""""Each user may only have up to TWO profiles. \n One for dating, and one for standard server activities.
        \n After using this command you need to edit your profile by using the:\n /profile_name, /profile_type, /age_range, /gender, /pronouns, and /about_me
        \n commands to fill in your user profile.\n You can also see what your profile currently contains with /view_profile") """)
    '''

# NEWLY ADDED as of 7/27/22 3:31pm
@client.slash_command(guild_ids= [guild])
async def edit_profile(interaction: nextcord.Interaction):
    """
    This is the main slash command that will be the prefix of all commands below.
    This will never get called since it has subcommands.
    """
    pass

@edit_profile.subcommand(description= "edit your profile type")
async def profile_type(
    interaction: nextcord.Interaction,
    profile_type: int = SlashOption(
        name = "profile_type",
        # as you add more profile types, add them respectively here, and under the match keyword below
        choices = {"Normal": 1, "Dating": 2},  #, "Gaming": 3}
    ),
):
    # profile_as_string = ""    # appears you dont need to use this bit.
    # it seems that switch statements exist until the function completes based on the contents of the variable
    
    # Python's Switch statement
    match profile_type:
        case 1:
            profile_as_string = "Normal"
            await interaction.response.send_message(f"This will become a {profile_as_string}")
            index = database.get_index("profile_type", profile_as_string)

        case 2:
            profile_as_string = "Dating"
            await interaction.response.send_message(f"This will become a {profile_as_string}")

        case _:
            await interaction.response.send_message("Error, you did not choose a valid input.\n Please use numbers to select the desired profile type.\n Example, to assign your profile as a Dating profile, type '2'.")
            raise Exception("Valid input not selected")
    
    # formerly had the await lines for non case _: right here and it was throwing a weird error because you cant use
    # .response multiple times one after another, you'd need to use .followup
    # or in my case, the best option was to outright move .response into the case 1-2 so that
    # there were no potential conflicts at all.

    @edit_profile.subcommand(description= "state which field you want to change, then select the change")
    async def age_range():
        pass


client.run(TOKEN)

# this can be bundled up above in: https://stackoverflow.com/questions/64844786/run-another-function-when-any-command-is-called-discord-py
'''
test = client.guilds
print ("After test result:", test)
'''