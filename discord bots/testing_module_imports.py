import profile_builderV2
from profile_builderV2 import profile_database

# i just realized what i did wrong. i was importing the .py module... but not
# specifying that i wanted the profile_builderV2 class as well!
# i had the class named the same as the .py file before this too btw.
# i needed to do FROM-IMPORT to get it to work right!

profile_builderV2()
profile_builderV2.profile_database.create_new_profile()