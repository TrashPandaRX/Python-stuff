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

        self.profile_standard = largest_profile_params
        # added at 3:56pm 9/3, didnt work. on the right track though i think
        #self.profile_standard['data'].reindex(np.arange(self.profile_standard['indicies']-1), copy = True)

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
    initializer = automator(**dictionary_of_profiles)
    initializer.profile_standard['default'] = initializer.apply_numerical_indicies(initializer.profile_standard['data'])  # testing new func
    convert_us_to_csv = initializer.scale_profiles_to_largest()

    for dataarray_label, dataarray in convert_us_to_csv.items():
        print(dataarray_label)
        print(dataarray) 