# this module is to be used in conjunction with one of the "mare.bot"s and "profile_builders" of the xseries
import pandas as pd
import numpy as np
import xarray as xr
import os

class automator:

    # IMPORTANT each kwargs should be a separate xr.dataarray or xr.dataset.dataarray
    def __init__(self, **kwargs):
        self.proflies = []
        self.other_profile_params = {}      # this is a dictionary of dictionaries structured like largest_profile_params aka self.profile_standard

        # will need data from the largest profile like:
        # number of indicies, number of columns, 
        largest_profile_params = {
            'name': str,
            'indicies' : 0,
            'columns' : 0,
            'data' : pd.DataFrame()
        }
        print("\n\n->***REVEALING KWARGS***<-\n\n")
        print(kwargs.keys())

        # adjusted at 10:57am so that its more based on pandas atm
        # why the fuck is this shit still name kwargs...
        for profile_type, actual_profile in zip(kwargs.keys(),kwargs.values()):
            self.proflies.append(actual_profile)
            print("outside if comparator")
            if len(actual_profile) > largest_profile_params['indicies']:
                print("inside if comparator")
                print(profile_type)
                print(actual_profile)
                largest_profile_params['name'] = profile_type

                # last debugged sept 1 at 10:13am
                # cant use .shape.x or shape.y because they are tuples and actual profile has these coded under the dimensions.
                # that is to say...instead of doing .shape.x do .shape[0] and .shape[1] for .y
                # also dropped the len() because the new change to the code already yields ints
                largest_profile_params['indicies'] = actual_profile.shape[0] # number of indicies in this dataarray --> # formely had actual_profile.shape.x but that didnt work because i was treating the dict as a dataframe. instead of it holding the dataframes
                largest_profile_params['columns'] = actual_profile.shape[1] # number of columns in this dataarray
                largest_profile_params['data'] = actual_profile
            # added 3:56pm 9/2
            else:
                self.other_profile_params[profile_type] = {}
                self.other_profile_params[profile_type]['name'] = profile_type
                self.other_profile_params[profile_type]['indicies'] = actual_profile.shape[0] # number of indicies in this dataarray --> # formely had actual_profile.shape.x but that didnt work because i was treating the dict as a dataframe. instead of it holding the dataframes
                self.other_profile_params[profile_type]['columns'] = actual_profile.shape[1] # number of columns in this dataarray
                self.other_profile_params[profile_type]['data'] = actual_profile

        print("=================================\n", self.other_profile_params)

        '''
        # old (bad) notion of what above if-conditional should look like
        for profile_type in kwargs:
            self.proflies.append(profile_type)
            if len(profile_type) > largest_profile_params['indicies']:
                print(profile_type)
                largest_profile_params['name'] = profile_type.name
                largest_profile_params['indicies'] = len(profile_type.dim_0) # number of indicies in this dataarray
                largest_profile_params['columns'] = len(profile_type.dim_1) # number of columns in this dataarray
                largest_profile_params['data'] = profile_type
        '''
        self.profile_standard = largest_profile_params
        # added at 3:56pm 9/3, didnt work. on the right track though i think
        #self.profile_standard['data'].reindex(np.arange(self.profile_standard['indicies']-1), copy = True)


    '''
    # THEORETICAL VERSION OF scale_profiles_to_largest()

    # forcefully upscale all other dataarrays dimensions up to the dimensions of the 'largest profile'
    # then return the freshly rescaled results
    # @3:12pm sept 2 - i acknowledge that i will likely need to pass in affiliated data from each .csv file and pass it back in here after
    # i remake the dataframes so that they are all the same size as 'default' aka the dataframe with the largest dimensions aka
    # my golden standard for a lot of this script's logic.
    def scale_profiles_to_largest(self, list_of_profile_types : list()):
        # alright so xarray.Dataarray is being a little **** so
        # im going to just have to take the old dataarray
        # and create a new one based off of it...
        dataset = xr.Dataset()
        updated_arrays = {
            'default' : self.profile_standard['data']
        }

        # adding the keys but no values yet
        for current_p_type in list_of_profile_types:
            updated_arrays[current_p_type] = None

        print("adding the keys but no values yet:\n", updated_arrays)

        for profile_type in self.proflies:
            print(type(profile_type))
            print(profile_type)
            # skip if this profile is the same as the one being used as the golden standard
            # @ 2:19pm sept 2 - forgot dataframes in pandas dont possess names, thats xarray exclusive.
            # @ 3:08pm - BUT past me wasnt a total jacktard, I made a 'data' key in self.profile_standard, which
            # i can use to compare the contents of one DataFrame to another DataFrame and it worked!! 
            if profile_type is self.profile_standard['data']:
                print('found the biggie!\n', self.profile_standard['name'])
                continue
            else:
                # reforge the profile_type with the dimensions of the profile_standard
                # while retaining the data and adding new indicies to match the standard.
                
                # remember index and columns need list-like values which is why arange is good
                upgraded_array = pd.DataFrame(profile_type, index = np.arange(self.profile_standard['indicies']), columns = np.arange(self.profile_standard['columns']))
                print(upgraded_array)
                upgraded_array.columns = ['profile_name', 'age_range', 'gender', 'pronouns', 'about_me']
                updated_arrays[''] = upgraded_array
                print(upgraded_array)
                


                #updated_arrays[''] = upgraded_array

            # does this look at each key value pair or is it just the key? or just the value?
            # TODO 
            #for array in updated_arrays:
            #    dataset[] = array
            #return dataset
    '''

    # https://stackoverflow.com/questions/51571350/proper-way-to-replace-nan-value-from-another-dataframe-on-column-match-in-pandas
    def apply_numerical_indicies(self, df : pd.DataFrame | xr.DataArray):
        new_df = pd.DataFrame(index= np.arange(df.shape[0]), columns = df.columns)
        # pd.combine() has potential as well, need to practice that in the future.
        #new_df = df.combine()
        #print(new_df['profile_name'])
        df.index = np.arange(df.shape[0])   # NOTE jesus fucking christ, something this simple works... im a fucking idiot
        #print(df['profile_name'], "\n\n", df.index)
        
        # im dumb again i forgot this produces a new dataframe.
        # if i want it to modify new_df directly i have to tell it to make the process inplace, via inplace=True
        new_df['profile_name'].fillna(pd.Series(df['profile_name']), inplace=True)
        print("merged:\n", new_df)

        return new_df


    # when im not dealing with these empty sample profiles... it might be better to do the concatination method
    # where i take the existing data and add a new dataframe that would make the .shape of the dataframe match the
    # largest one being used at the standard.
    def scale_profiles_to_largest(self):
        #dataset = xr.Dataset()
        updated_arrays = {
            # 'default' : self.profile_standard['data']
            self.profile_standard['name'] : self.profile_standard['data'],
        }

        # adding the keys but no values yet
        # LAST THING I POKED AT BEFORE HANGING OUT WITH GF ON 9/2 @ 5:39pm
        for current_p_type in self.other_profile_params:
            print(current_p_type)
            updated_arrays[current_p_type] = None       # if you wanted to start putting the existing data in, just say self.other_profile_params[current_p_type]['data']

        print("adding the keys but no values yet:\n", updated_arrays)

        # changed this because i want to access both the 'names' and 'data' from my dictionaries containing this info
        # profile_name ended up acting as the key, profile_type ended up acting as the value
        for key, value  in self.other_profile_params.items():
            print(key)
            print(type(value['data']))
            print(value['data'])

            # honestly i can remove this if statement now because ive got one variable for just the
            # profile_standard and another just for the non-standard profiles
            if value['data'] is self.profile_standard['data']:
                print('found the biggie!\n', self.profile_standard['name'])
                continue
            else:
                # updated_arrays IS NOT THE SAME AS upgraded_array
                # older version -- upgraded_array = pd.DataFrame(value['data'], index = np.arange(self.profile_standard['indicies']), columns = np.arange(self.profile_standard['columns']))
                upgraded_array = pd.DataFrame(value['data'], index = np.arange(self.profile_standard['indicies']-self.other_profile_params[key]['indicies']), columns = np.arange(self.profile_standard['columns']))
                print(upgraded_array)
                upgraded_array.columns = self.profile_standard['data'].columns
                updated_arrays[key] = pd.concat([self.other_profile_params[key]['data'], upgraded_array])
                print(upgraded_array)
                
                '''
                #pre-rework

                # updated_arrays IS NOT THE SAME AS upgraded_array
                upgraded_array = pd.DataFrame(value['data'], index = np.arange(self.profile_standard['indicies']), columns = np.arange(self.profile_standard['columns']))
                print(upgraded_array)
                upgraded_array.columns = self.profile_standard['data'].columns
                updated_arrays[key] = upgraded_array
                print(upgraded_array)
                
                '''
# -----------------------------------------------------------------
# pulled this out of the exception case to see if it will help 
        for profile_type in updated_arrays.keys():
            if profile_type is self.profile_standard['name']:
                #if profile type is default, skip this iteration
                continue
            else:
                print("\nprofile type:\n", profile_type)
                # partially works... im going to have to have a triple or quad nested loop at this rate...
                # todo
                for names_to_replicate, index_value, fields_to_overwrite  in zip(self.profile_standard['data']['profile_name'].values, np.arange(updated_arrays[profile_type].shape[0]), updated_arrays[profile_type]['profile_name']):
                    print("\nnames to replicate:\n", names_to_replicate, "\nfields to overwrite:\n", fields_to_overwrite)
                    print("DOES THIS WORK?\n trying to get the value at a specific index & column value.\n -->", updated_arrays[profile_type].iloc[index_value]['profile_name'], "<--")
                    print("CONTROL TEST\n -->", updated_arrays['default'].iloc[index_value]['profile_name'], "<--")
                    updated_arrays[profile_type].iloc[index_value]['profile_name'] = names_to_replicate

        print(updated_arrays)
        dataset = xr.Dataset(updated_arrays)
        print("RESULTS:\n\n<<<<<<<<<000000000>>>>>>>>>>\n")
        return dataset
# -----------------------------------------------------------------

        '''
        #updated_arrays[''] = upgraded_array
        #print('<<<<<<<<<<< Updated arrays >>>>>>>>>>>>\n', updated_arrays)   
        try:
            dataset = xr.Dataset(updated_arrays)
            print('<<<<<<<<<<< Updated arrays as xr.Dataset >>>>>>>>>>>>\n', dataset)
            return dataset

        # enter here because of duplicate values in dataframes
        # now to resolve this you need to look at each profile_type and then view each
        # profile_name and change it so that it matches the 'profile_standard' names in order
        except Exception as e:
            #dataset['new'] = xr.DataArray()
            print(e)
            for profile_type in updated_arrays.keys():
                if profile_type is self.profile_standard['name']:
                    #if profile type is default, skip this iteration
                    continue
                else:
                    print("\nprofile type:\n", profile_type)
                    # partially works... im going to have to have a triple or quad nested loop at this rate...
                    # todo
                    for names_to_replicate, index_value, fields_to_overwrite  in zip(self.profile_standard['data']['profile_name'].values, np.arange(updated_arrays[profile_type].shape[0]), updated_arrays[profile_type]['profile_name']):
                        print("\nnames to replicate:\n", names_to_replicate, "\nfields to overwrite:\n", fields_to_overwrite)
                        print("DOES THIS WORK?\n trying to get the value at a specific index & column value.\n -->", updated_arrays[profile_type].iloc[index_value]['profile_name'], "<--")
                        print("CONTROL TEST\n -->", updated_arrays['default'].iloc[index_value]['profile_name'], "<--")
                        updated_arrays[profile_type].iloc[index_value]['profile_name'] = names_to_replicate

            print(updated_arrays)
            dataset = xr.Dataset(updated_arrays)
            print("RESULTS:\n\n<<<<<<<<<000000000>>>>>>>>>>\n")
            return dataset
        '''

                


        
          

# testing setup
if __name__ == '__main__':
    profile_builder_dir = os.getcwd()
    name_of_folder_containing_profile_data = "test folder"
    profile_data_path = os.path.join(profile_builder_dir, name_of_folder_containing_profile_data)
    
    csv_profiles = ['gaming', 'dating', 'default', 'mental']
    dictionary_of_profiles = dict()

    for file, name  in zip(os.listdir(profile_data_path), csv_profiles):
        print(file)
        dictionary_of_profiles[name] = pd.read_csv(f"{profile_data_path}/{file}", index_col=[0])

    for key,value in zip(dictionary_of_profiles.keys(), dictionary_of_profiles.values()):
        print(f"{key} : {value}")

    #dictionary_of_profiles['default']
    # this might also be an okay spot to DataFrame.reindex() if you know the number of indicies you will have.

    # testing
    # i think i fucked up with how i passed the dictionary into the constructor for KWARGS to be used...
    # maybe i should be using key value pairs to bring the dictionary elements in
    # instead of a full fucking dictionary.
    initializer = automator(**dictionary_of_profiles)                   # THIS WAS WRONG
    initializer.profile_standard['default'] = initializer.apply_numerical_indicies(initializer.profile_standard['data'])  # testing new func
    convert_us_to_csv = initializer.scale_profiles_to_largest()

    for dataarray_label, dataarray in convert_us_to_csv.items():
        print(dataarray_label)
        print(dataarray)


    '''
    # initializer = automator(kwargs = dictionary_of_profiles)   # THIS WAS WRONG
    # basically what i had before was a KEY named kwargs, that contained the dictionary, 'dictionary_of_profiles'
    # which meant that kwargs whenever i referred to it later on, was literally just the string-key to the dictionary-value
    # example for my dumb ass:
    def sample_kwarg(**kwargs):
        print(kwargs)
        print(type(kwargs))

    sample_kwarg(kwargs = sample_dict)  

    # returns the following
    {'kwargs': {'name': 'rory', 'age': 22, 'height': 162, 'weight': 140}}
    <class 'dict'>
    '''          