import pandas as pd
import os

from profile_builder import profile_data_dir_exist


# TODO i need to turn this into a singleton, i dont need like 50 of these popping up out of the blue

class profile_database:

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

    def __init__(self):
        self.profile_builder_dir = os.getcwd()
        self.name_of_folder_containing_profile_data = "user_profiles"
        self.profile_data_path = os.path.join(self.profile_builder_dir, self.name_of_folder_containing_profile_data)
        self.__user_data = pd.DataFrame(columns=["a_profile_name", "a_profile_type", "a_age_range", "a_gender", "a_pronouns", "a_about_me"])

        profile_data_dir_exist()

    # NOTE i might need to intergrate this function into the __init__ since im having issues with my dataframe length. im honestly at present
    # skipping out on a lot of the parsing and shit that i did when i WAS using this function...
    # i at the very least need to utilize this function in the bot
    def profile_data_dir_exist(self):
        if os.path.exists(self.profile_data_path):
            print("it exists!")
            try:
                self.__user_data = pd.read_csv(f"{self.profile_data_path}/user-data.csv", index_col=[0])
            except:
                print("Issue occured within 'profile_data_dir_exists()', if-statement")

            print(self.__user_data)
            return self.__user_data
        else:
            print("making directory...")
            os.mkdir(self.profile_data_path)

            try:
                '''
                # didnt complete this bit because it just makes more sense at least as of (7/16/22) to let pandas write this
                with open(f"{profile_data_path}/user-profiles.csv", "w") as user_data_file:
                    user_data_file.
                    pass
                '''
                self.__user_data.to_csv(f"{self.profile_data_path}/user-data.csv", index_col = [0])
                return self.__user_data
            except:
                print("Issue occured within 'profile_data_dir_exists()', else-statement")
            

    # GETTER: give mare-bot a way to access user_profiles for manipulation
    #@property
    def _get_user_profiles(self):
        return self.__user_data
    # SETTER
    #@_user_profiles.setter
    def _set_user_profiles(self, updated : pd.DataFrame):
        if isinstance(updated, pd.DataFrame) == False:
            raise TypeError("The 'updated' variable was not a pandas.DataFrame")
        else:
            self.__user_data = updated

    user_profiles = property(_get_user_profiles, _set_user_profiles)

    # manipulating user-data dataframe from mare-bot.py
    # this reads in the profiles from user-data.csv
    def parse_existing_user_data(self):
        try:
            self.__user_data = pd.read_csv(f"{self.profile_data_path}/user-data.csv", index_col=[0])
            return self.__user_data
        except:
            print("Issue occured within 'parse_existing_user_data()'")


    # Check if a user already has a profile
    def profiles_exist_checker():
        pass

    # create an empty profile -- needs work
    def create_mostly_empty_profile(self, existing_user_data: pd.DataFrame, profile_name: str):
        # this isnt working out, because pandas is trying to constantly add the fucking column for each index's row value its throwing my shit off, but ik it might be useful later down the line...UGH
        # so at the moment... we are just going to suspend this code and instead use .concat() and create a NEW data frame for the new profile, and attatch it to the existing __user_profiles
        existing_user_data.loc[len(existing_user_data.index)] = pd.Series([profile_name, None, None, None, None, None])

        #new_data = [profile_name, profile_type, age_range, gender, pronouns, about_me]
        #existing_user_data = pd.concat([existing_user_data, new_data])
        
        return existing_user_data

    # restrict users from having more than 2 profiles. 1 for dating, 1 for normal
    def create_new_profile(self, existing_user_data: pd.DataFrame, profile_name: str = None, profile_type: str= None, age_range: str= None, gender: str= None, pronouns: str= None, about_me: str= None):
        # https://www.geeksforgeeks.org/how-to-add-one-row-in-an-existing-pandas-dataframe/ fast reminder, i was stupidly trying to use .add() earlier which is literally just linear algebra addition
        # reminder for future me, index are the rows in a dataframe. whilst columns are well the columns
        #https://stackoverflow.com/questions/59406045/convert-pandas-series-into-a-row
  
        print(existing_user_data.index)

        #existing_user_data.loc[len(existing_user_data.index)] = [profile_name, profile_type, age_range, gender, pronouns, about_me]
        
        #new_data = pd.Series([profile_name, profile_type, age_range, gender, pronouns, about_me]).to_frame().T # NOTE IMPORTANT: axis =0 is for adding data as a row, while axis = 1 adds dat as columns
        
        # I got fucking tired of fighting this piece of shit and just lazy boy oven added a new column to represent the fucking index
        new_data = pd.Series([existing_user_data.index + 1, profile_name, profile_type, age_range, gender, pronouns, about_me])
        print("the list of data to append to df:", new_data)
        #existing_user_data = existing_user_data([existing_user_data, new_data], axis = 0)
        print(len(existing_user_data.index), " compared to ", len(new_data.index))
        existing_user_data.loc[len(existing_user_data.index)] = new_data
        

        return existing_user_data


    # someone trying to view their own profile
    def view_full_profile(self):
        pass

    # user sharing their almost full profile with others within the server (barring the 4-digit discord identification number)
    def share_profile(self):
        pass

    # this updates the dataframe user_data
    def update_profile(self):
        pass

    # this actually updates the .csv file every few minutes based on the current contents of user_data.
    # this should occur every time the users modify existing data.
    # of course should the server become very populated it would instead be ideal to instead back this data up every few hrs or so.
    def update_profile_csv(self):
        try:
            self.__user_data.to_csv(f"{self.profile_data_path}/user-data.csv")
        except:
            print("Issue occured within 'update_profile_csv()'")


    # purge a profile from the user_data and then call update_profile_csv. this should always update the csv file almost immediately.
    # this will be key in two major commands in mare-bot, for normal users, this will delete their OWN profile.
    # but for admin level entities, there will be an admin level command, that deletes the TARGET profile.
    def delete_profile(self):
        pass

    # others trying to view someone else's profile
    def view_limited_profile(self):
        pass



    # Bugs and other goofs documentation
    # 7/18/22 -- realized my functions were failing as they treated the create_new_profile() as a brand new dataframe. I forgot python is weird with affecting globals, so i had to return the values from the functions, AND THEN pass the results into the desired dataframe safely.


    # *** testing purposes ***
    '''
    for things in os.walk(os.getcwd()):
        print(things)
    '''

    
# checking if files exist/importing data from .csv, creating a new profile, updating .csv with all current profiles.
'''
x = profile_database()
__user_data = x.profile_data_dir_exist()
print("before create new profile...", __user_data.index, "\n", __user_data)
__user_data = x.create_new_profile(__user_data, "sam", "sample", "23-26", "f", "she/her", "I hate trains and pie")
# --> REPLACING 'create_new_profile' variant above <-- __user_data = create_mostly_empty_profile(__user_data, "sam", "sample", "23-26", "f", "she/her", "I hate trains and pie")  
print("after create new profile...", __user_data.index, "\n", __user_data)
x.update_profile_csv()
'''

# *** end of testing purposes ***