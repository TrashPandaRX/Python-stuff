import numpy as np
import pandas as pd
import xarray as xr
import os


# TODO i need to turn this into a singleton, i dont need like 50 of these popping up out of the blue

class xarray_database:

    def __init__(self):
        self.settings = []
        self.profile_builder_dir = os.getcwd()
        self.name_of_folder_containing_profile_data = "user_profiles_Xseries"   # change me if you want the directory's name different.
        self.profile_data_path = os.path.join(self.profile_builder_dir, self.name_of_folder_containing_profile_data)
        
        self.boilerplate = pd.DataFrame(columns=["profile_name", "age_range", "gender", "pronouns", "about_me"])
        
        # formerly initial_creation_of_profiles
        self.initial_profile_state = self.profile_data_dir_exist()
        #self.__user_data = self.initial_profile_state

        # dont forget that settings is a csv as well, and its increasing the number of csv files in this directory by 1.
        self.number_of_profile_types = len(os.listdir(self.profile_data_path))-1
        print(self.number_of_profile_types)
        print(self.settings)

        self.config_to_settings()

        self.__user_data = self.initial_profile_state
        print(self.__user_data)

        self.get_one_index("placeholder", "placeholder", "placeholder")

    # you would think this returns a bool, but i have it returning a dataframe/xarray
    def profile_data_dir_exist(self):
        if os.path.exists(self.profile_data_path):
            print("it exists!")
            try:
                error_check = self.parse_existing_user_data()
                # TODO need to finish building dependencies for the settings!
                folder_settings = self.settings_parser()
                # the most important info i need from a settings document is:
                # 1) what the names of each type of profile dataframe will be
                # 2) and by using the names, i can instantly know via len()
                # how many data frames there will need to be
                print("*** about to test the self.settings_parser() ***")
                self.settings = list(folder_settings)
                print("***\nself.settings:\n***\n", self.settings)

                if isinstance(error_check,  FileNotFoundError):
                    raise Exception("file not found error within 'parse_existing_user_data'")
                else:   # if error_check isnt a filenotfound error
                    users_xarray = error_check
                    return users_xarray

            except:
                print("1 Issue occured within 'profile_data_dir_exists()', if-statement")
                print("2 attempting to create .csv file to resolve issue...")
                try:
                    newcsv = self.boilerplate.to_csv(f"{self.profile_data_path}/user-data.csv")
                    print("3 except case's .csv creation resolved issue.")
                    return self.boilerplate
                except:
                        print("4 except case's .csv creation DID NOT RESOLVE issue.")


        else:
            print("making directory...")
            os.mkdir(self.profile_data_path)
            try:
                newcsv = self.boilerplate.to_csv(f"{self.profile_data_path}/user-data.csv", index_col = [0])
                return newcsv
            except:
                print("5 Issue occured within 'profile_data_dir_exists()', else-statement")
            
    # ********** Getter & setter setup **********
    # GETTER: give mare-bot a way to access user_profiles for manipulation
    def _get_user_profiles(self):
        return self.__user_data
    # SETTER

    def _set_user_profiles(self, profile_type: str, updated : pd.DataFrame):
        if (isinstance(updated, pd.DataFrame) == False) or (isinstance(updated, xr.Dataset) == False):
            raise TypeError("The 'updated' variable was not a pandas.DataFrame or xarray.Dataset")
        else:
            self.__user_data = updated

            self.__user_data
            print("FIX ME I NEED TO BE REMADE TO HANDLE MULTIDIMENSIONAL ARRAYSSSS (ps this is _set_user_profiles)")

    user_profiles = property(_get_user_profiles, _set_user_profiles)
    # ********** end of get and set setup **********

    # BUG FIXME @11:30am, 8/13/22 still working on as of 8/15
    # ISSUE with parse_existing_user_data
    # --> dim1 consists of 25 items, when i need this to be instead
    # however many fields for each profile type
    # ie if dating-profile, and it has
    # ["profile_name", "age_range", "gender", "pronouns", "about_me"]
    # it should have a length of only 5
    
    # UPDATE I REALIZED THERES NOTHING WRONG WITH THE CODE!!! @ 2:54pm 8/16/22
    # After experimenting in jupyter notebook i realized that the issue was the .csv files
    # contents! me setting some of the names of the columns different from other .csv's
    # forced xarray to add all those differently named columns to EACH dataarray/dataframe
    # as they got added to my dataset containing all of them.
    # they had to be equivalent across the board

    # manipulating user-data dataframe from mare-bot.py
    # this reads in the profiles from user-data.csv
    def parse_existing_user_data(self):
        try:
            # going to need to return each of these as a pd dataframe, but collectively as a list of dataframes for now
            csv_files = []
            dataFrames = []
            for file in os.listdir(self.profile_data_path):
                if (file.endswith(".csv")) and (file.startswith("settings") is False):
                    csv_files.append(file)
                    dataFrames.append(pd.read_csv(f"{self.profile_data_path}/{file}", index_col=[0])) # temp -- experimenting put list() in to force the data to be saved as nested lists
            dict_of_df = dict()
            for df, file in zip(dataFrames, csv_files): # remember you need zip() if you want to iterate over more than one list at the same time.
                dict_of_df[file] = df
            print(dict_of_df)
            
            # checking for duplicates
            '''
            broken, i need to not use a dict() here
            
            dupe_test = pd.DataFrame(dict_of_df)
            get_dupes = dupe_test.index.has_duplicates
            print(get_dupes)
            '''
            
            
            profiles = xr.Dataset(dict_of_df)
            print("*****\n",profiles)
            return profiles

            #return pd.read_csv(f"{self.profile_data_path}/user-data.csv", index_col=[0])
        except FileNotFoundError as e:
            print("Issue occured within 'parse_existing_user_data()'")
            return e

    def settings_parser(self):
        try:
            if (os.path.exists(self.profile_data_path)):
                if ("settings.csv" in os.listdir(self.profile_data_path)):
                    settings = pd.read_csv(f"{self.profile_data_path}/settings.csv")
                    return settings
                
                # if path exists but settings.csv not present
                else:
                    # TODO?
                    # just now thinking about this... @ 8:06 am 8/13/22
                    # but i should probably make settings 2 rows in length with
                    # the first row -- profile types
                    # second row -- columns that needs to be in each profile's dataframe
                    blank_file = pd.DataFrame(list())
                    blank_file.to_csv(f"{self.profile_data_path}/settings.csv")
                    settings = self.settings_parser()
                    return settings
            else:
                raise Exception("an error occured within settings_parser()")
        except:
            print(f"Path {self.name_of_folder_containing_profile_data} does not exist at this directory.")

    def config_to_settings(self):
        #num_of_profiles = len(self.settings)
        for profile_type in self.settings:
            self.boilerplate.to_csv(f"{self.profile_data_path}/{profile_type}.csv")

    # Check if a user already has a profile
    def profiles_exist_checker(self, user_name : str):
        does_profile_exist = False

        
        return does_profile_exist
    
    # create a new row for user across each profile type
    def create_new_profile(self, existing_user_data: pd.DataFrame, profile_name: str = None, profile_type: str= None, age_range: str= None, gender: str= None, pronouns: str= None, about_me: str= None):
        pass

    # someone trying to view their own profile
    def view_profile(self):
        pass

    # user sharing their almost full profile with others within the server (barring the 4-digit discord identification number)
    def share_profile(self):
        pass

    # this updates the dataframe user_data
    def update_profile(self):
        pass

    # this actually updates the .csv file based on the current contents of user_data.
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


    def get_all_indexes(self, column_name : str , cell_value):
        return self._get_user_profiles().loc[self._get_user_profiles()[column_name] == cell_value].index

    # TODO LAST WORKED ON @ 9:30am 7/30/22 --> 8/3/22 2:11pm --> 8/16/22 4:16pm
    # ...at this point i realized it would be best to move to a newer cleaner
    # version where i properly handled the profiles as "panels"
    # or more modernly known as multiIndex or XARRAY
    def get_one_index(self, username: str, column_name: str, cell_value):
        # might be smart to just base this off of dataarray[0] aka basic-profiles in the dataset
        # since everything will be forcefully synced up in terms of column and index dimensions
        # NOTE DataSet.xs() might be useful
        testing = self._get_user_profiles()["default-profile.csv"]
        '''
        fucked this up, it was writing 'd''i''m''_''1'
        testing = []
        for x in self._get_user_profiles()["default-profile.csv"].dims[1]:
            testing.append(x)
        '''

        print(")()()()()(\n",testing)


    # TODO
    # modify existing profile values in dataframe
    # will need to:
    # 1) determine which row we are modifying
    # 2) modify the column indicated (this will need to be passed from the bot to this script as a param)
    # 3) use this information to update the appropriate cell to the new value
    # 4) return the updated values to the bot so that they can be updated by the _set_user_profiles() & database.update_profile_csv()
    def edit_personal_data(self, username : str, column_name : str, row_index: int, new_value):
        df = self._get_user_profiles()
        pass



    # Bugs and other goofs documentation
    # 7/18/22 -- realized my functions were failing as they treated the create_new_profile() as a brand new dataframe. I forgot python is weird with affecting globals, so i had to return the values from the functions, AND THEN pass the results into the desired dataframe safely.


# *** testing purposes ***
'''
for things in os.walk(os.getcwd()):
    print(things)
'''
x = xarray_database()
print("done")


# *** end of testing purposes ***