import pandas as pd
import os

profile_builder_dir = os.getcwd()
name_of_folder_containing_profile_data = "user_profiles"
#print(profile_builder_dir)
profile_data_path = os.path.join(profile_builder_dir, name_of_folder_containing_profile_data)

__user_data = pd.DataFrame(columns=["a_profile_name", "a_profile_type", "a_age_range", "a_gender", "a_pronouns", "a_about_me"])

'''
MORE INFO REGARDING EACH COLUMN:
ps we can add more columns later on in development

TODO DONT FORGET TO HAVE ANOTHER COLUMN THAT SAVES EACH DISCORD USERS UNIQUE 4-DIGIT IDENTIFICATION KEY (eg. raichu44 -> #1904)

profile-name : takes user's current discord name within the server
profile-type : dating or normal (or 'sample' for my testing purposes)
age-range : will be divided into 18-23?, 23?-26?, and 26?-30? (the ? marks mean idk what mare would like to settle on yet)
gender : m f nb (nb is nonbinary)
pronouns : he/him she/her they/them neo (neo refers to neo pronouns {see https://unf.edu/lgbtqcenter/Pronouns.aspx}, its best for these users to specify their specific preferred pronouns in 'about-me')
about-me : just a long string, we can restrict this to a set # of characters for succinctness sake
'''

def profile_data_dir_exist():
    if os.path.exists(profile_data_path):
        print("it exists!")
        try:
            __user_data = pd.read_csv(f"{profile_data_path}/user-data.csv", index_col=[0])
        except:
            print("Issue occured within 'profile_data_dir_exists()', if-statement")

        print(__user_data)
        return __user_data
    else:
        print("making directory...")
        os.mkdir(profile_data_path)

        try:
            '''
            # didnt complete this bit because it just makes more sense at least as of (7/16/22) to let pandas write this
            with open(f"{profile_data_path}/user-profiles.csv", "w") as user_data_file:
                user_data_file.
                pass
            '''
            __user_data.to_csv(f"{profile_data_path}/user-data.csv")
            return __user_data
        except:
            print("Issue occured within 'profile_data_dir_exists()', else-statement")
        

# GETTER: give mare-bot a way to access user_profiles for manipulation
def _get_user_profiles():
    return __user_data

def _set_user_profiles(updated : pd.DataFrame):
    __user_data = updated

# manipulating user-data dataframe from mare-bot.py
# this reads in the profiles from user-data.csv
def parse_existing_user_data():
    try:
        __user_data = pd.read_csv(f"{profile_data_path}/user-data.csv", index_col=[0])
    except:
        print("Issue occured within 'parse_existing_user_data()'")


# Check if a user already has a profile
def profiles_exist_checker():
    pass

# create an empty profile
def create_mostly_empty_profile(existing_user_data: pd.DataFrame, profile_name: str):
    existing_user_data.loc[len(existing_user_data.index)] = [profile_name, None, None, None, None, None]
    return existing_user_data

# restrict users from having more than 2 profiles. 1 for dating, 1 for normal
def create_new_profile(existing_user_data: pd.DataFrame, profile_name: str, profile_type: str, age_range: str, gender: str, pronouns: str, about_me: str):
    # https://www.geeksforgeeks.org/how-to-add-one-row-in-an-existing-pandas-dataframe/ fast reminder, i was stupidly trying to use .add() earlier which is literally just linear algebra addition
    # reminder for future me, index are the rows in a dataframe. whilst columns are well the columns
    print(existing_user_data.index)
    
    # this isnt working out, because pandas is trying to constantly add the fucking column for each index's row value its throwing my shit off, but ik it might be useful later down the line...UGH
    # so at the moment... we are just going to suspend this code and instead use .concat() and create a NEW data frame for the new profile, and attatch it to the existing __user_profiles
    existing_user_data.loc[len(existing_user_data.index)] = [profile_name, profile_type, age_range, gender, pronouns, about_me]

    return existing_user_data


# someone trying to view their own profile
def view_full_profile():
    pass

# user sharing their almost full profile with others within the server (barring the 4-digit discord identification number)
def share_profile():
    pass

# this updates the dataframe user_data
def update_profile():
    pass

# this actually updates the .csv file every few minutes based on the current contents of user_data.
# this should occur every time the users modify existing data.
# of course should the server become very populated it would instead be ideal to instead back this data up every few hrs or so.
def update_profile_csv():
    try:
        __user_data.to_csv(f"{profile_data_path}/user-data.csv")
    except:
        print("Issue occured within 'update_profile_csv()'")


# purge a profile from the user_data and then call update_profile_csv. this should always update the csv file almost immediately.
# this will be key in two major commands in mare-bot, for normal users, this will delete their OWN profile.
# but for admin level entities, there will be an admin level command, that deletes the TARGET profile.
def delete_profile():
    pass

# others trying to view someone else's profile
def view_limited_profile():
    pass



# Bugs and other goofs documentation
# 7/18/22 -- realized my functions were failing as they treated the create_new_profile() as a brand new dataframe. I forgot python is weird with affecting globals, so i had to return the values from the functions, AND THEN pass the results into the desired dataframe safely.


# *** testing purposes ***
'''
for things in os.walk(os.getcwd()):
    print(things)
'''

'''
# checking if files exist/importing data from .csv, creating a new profile, updating .csv with all current profiles.
__user_data = profile_data_dir_exist()
print("before create new profile...", __user_data.index, "\n", __user_data)
__user_data = create_new_profile(__user_data, "sam", "sample", "23-26", "f", "she/her", "I hate trains and pie")
print("after create new profile...", __user_data.index, "\n", __user_data)
update_profile_csv()
'''

# *** end of testing purposes ***