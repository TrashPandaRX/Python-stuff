from numpy import NaN, indices
import pandas as pd
import os

from profile_builder import parse_existing_user_data, profile_data_dir_exist


# TODO i need to turn this into a singleton, i dont need like 50 of these popping up out of the blue

class profile_database:

    def __init__(self):
        self.profile_builder_dir = os.getcwd()
        self.name_of_folder_containing_profile_data = "user_profiles"
        self.profile_data_path = os.path.join(self.profile_builder_dir, self.name_of_folder_containing_profile_data)
        self.__user_data = pd.DataFrame(columns=["profile_name", "profile_type", "age_range", "gender", "pronouns", "about_me"])

        # formerly initial_creation_of_profiles
        self.initial_profile_state = profile_data_dir_exist()
        self.__user_data = self.initial_profile_state

    def profile_data_dir_exist(self):
        if os.path.exists(self.profile_data_path):
            print("it exists!")
            try:
                self.__user_data = pd.read_csv(f"{self.profile_data_path}/user-data.csv", index_col=[0])
            except:
                print("Issue occured within 'profile_data_dir_exists()', if-statement")

            #print(self.__user_data)
            return self.__user_data
        else:
            print("making directory...")
            os.mkdir(self.profile_data_path)

            try:
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

    # FIXED 7/26/22
    # after several long painstaking hours i finally realized that i was passing in basically nothing from the
    # new_data object aside from the fact that it was a series. i needed to access .values or .array to
    # get the actual data fucking values...
    # restrict users from having more than 2 profiles. 1 for dating, 1 for normal
    def create_new_profile(self, existing_user_data: pd.DataFrame, profile_name: str = None, profile_type: str= None, age_range: str= None, gender: str= None, pronouns: str= None, about_me: str= None):
        # https://www.geeksforgeeks.org/how-to-add-one-row-in-an-existing-pandas-dataframe/ fast reminder, i was stupidly trying to use .add() earlier which is literally just linear algebra addition
        # reminder for future me, index are the rows in a dataframe. whilst columns are well the columns
        #https://stackoverflow.com/questions/59406045/convert-pandas-series-into-a-row
        new_data = pd.Series([profile_name, profile_type, age_range, gender, pronouns, about_me])        
        existing_user_data.loc[len(existing_user_data.index)] = new_data.values
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
            print("inside update_profile_csv()", self.__user_data)
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


    def get_all_indexes(self, column_name : str , cell_value):
        return self._get_user_profiles().loc[self._get_user_profiles()[column_name] == cell_value].index

    # TODO LAST WORKED ON @ 9:30am 7/30/22 --> 8/3/22 2:11pm
    # ...at this point i realized it would be best to move to a newer cleaner
    # version where i properly handled the profiles as "panels"
    # or more modernly known as multiIndex or XARRAY
    def get_one_index(self, username: str, column_name: str, cell_value):
        df = self._get_user_profiles()
        print("in get_one_index(), the value we want to search for is: ", cell_value)
        

        # ---------- NaN / None Handling -------------
        '''
        print("checking to see if cell_value is nan (using this for nan/None testing) or None\n")
        if cell_value is NaN:
            print(True)
        else:
            print(False)

        if cell_value is None:
            print(True)
        else:
            print(False)

        if cell_value == NaN:
            print(True)
        else:
            print(False)

        if cell_value == None:
            print(True)
        else:
            print(False)
        '''
        
        print("checking if getoneindex successfully detect NoneTypes\n")
        print(df[column_name].values)
        print(pd.isna(df[column_name].values))  # useful test. good, detected all the NaN's values in the arraylike

        '''        
        if ((cell_value is NaN) or (cell_value is None)) and ((None in df[column_name].values) or (df[column_name].values.isna())):
            print(True)
        else:
            print(False)
        '''

        if (cell_value is NaN):
            # zeroing in on index number
            indicies = self._get_user_profiles().loc[self._get_user_profiles()[column_name] == cell_value].index
            for row in indicies:
                if username in df.iloc[row]["profile_name"]:
                    # gave up on a broken idea, need to make sure this shit scales and doesnt fk me hard down the line
                    # as i try to maintain this or if some other poor bastard has to look at this mess
                    pass
        # ---------- NaN / None Handling END -------------

        '''
        # original contents for V3
        indicies = self._get_user_profiles().loc[self._get_user_profiles()[column_name] == cell_value].index
        # right now i just want all the rows with the indicated cell_values
        print(indicies)
        for row in indicies:
            if username in df.iloc[row]["profile_name"]:    # index based loc[] and i realized you need to also account for the profile_name column
                print(True, "IT WORKS!! index is ", df.iloc[row], " with an index # of ", row)
                return df.iloc[row], row    # returns as a list both the contents of that row and the row's index value
         '''

    # TODO
    # modify existing profile values in dataframe
    # will need to:
    # 1) determine which row we are modifying
    # 2) modify the column indicated (this will need to be passed from the bot to this script as a param)
    # 3) use this information to update the appropriate cell to the new value
    # 4) return the updated values to the bot so that they can be updated by the _set_user_profiles() & database.update_profile_csv()
    def edit_personal_data(self, username : str, column_name : str, row_index: int, new_value):
        df = self._get_user_profiles()
        #print("current dataframe: \n", df)
        #print("current cell intersection of: ", column_name, " and ", row_index, "\n")
        #df.at[df[column_name][row_index]] = new_value   # was using .loc before but it would create a brand new row full of the new value with a NaN for index value, .at is specifically for single cell access. NEW NOTE still does the same thing... but its just better practice to use .at for single operations moving forward anyway.
        
        # FIXED BUG -- more user lack of caffine more than anything...
        df.at[row_index, column_name] = new_value   # finally got it working as expected. Forgot that you need a comma to express coordinates and also had my column & row variables in each other's place. ie was using column x index instead of index x column

        #print("successfully survived .loc")
        #print("hopefully edited contents of dataframe\n", df)
        #print("new: ", df.loc[df[column_name][row_index]])
        self._set_user_profiles(df)
        #print("checking __user_profiles:\n",self._get_user_profiles())
        self.update_profile_csv()

        # then finally add the part of code that saves the newly update dataframe to .csv



    # Bugs and other goofs documentation
    # 7/18/22 -- realized my functions were failing as they treated the create_new_profile() as a brand new dataframe. I forgot python is weird with affecting globals, so i had to return the values from the functions, AND THEN pass the results into the desired dataframe safely.


    # *** testing purposes ***
    '''
    for things in os.walk(os.getcwd()):
        print(things)
    '''

    
# checking if files exist/importing data from .csv, creating a new profile, updating .csv with all current profiles.

#testing edit_personal_data()
x = profile_database()
print(x,"\n\n")
y = x.initial_profile_state         # formerly x._get_user_profiles()

print(y.columns.values, "\n\n")    # this is how you get your column names
#print(y , "\n vs \n", x._get_user_profiles())


# if you need to test stuff, using 'jupyter notebook' in the terminal is helpful
# as of 7/30/22 @ 7:48am, there should be NO difference in
# _get_user_profiles() vs parse_existing_user_data()
# so long as you are looking to get data straight from the CSV
# otherwise if you edit stuff in __user_data, _get_user_profiles() should be most up to date (REQUIRES CONFIRMATION OF VALIDITY)
print(y)
print("normal" in y["profile_type"].tolist())
print(x._get_user_profiles())

# extract the row for a given cell value.
print(x._get_user_profiles().loc[x._get_user_profiles()["profile_name"] == "Regulus#8269"].index)
print(x.get_all_indexes("profile_type", "dating"))
print(x.get_one_index("Regulus#8269", "age_range", NaN))

#temp removed below line
# print(x.get_one_index("Regulus#8269", "profile_type", "normal"))

# testing if there is an error in one over the other, and why
#x.edit_personal_data("Regulus#8269", "age_range", 1, "18-20")
#temp removed below line
#x.edit_personal_data("Regulus#8269", "age_range", x.get_one_index("Regulus#8269", "age_range", None)[1], "18-20")

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