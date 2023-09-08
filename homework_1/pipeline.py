# Use following syntax in bash shell:
# docker build -t container_name .
# winpty docker run -it container_name arg1 arg2

import sys

import pandas as pd

print(sys.argv) # prints the name of the file and the command line argument(s)

filename = sys.argv[1] # gets the first command line argument (name of the dataset file)

# ---------------------------------------------------------------------------------------- #
# DATASET CHANGES

df = pd.read_csv(filename) # read in csv based on command line argument

altered_df = df.copy()

# select only cats that are of the domestic shorthair breed
altered_df = altered_df.loc[df['Animal Type'] == 'Cat']
altered_df = altered_df.loc[(df['Breed'] == 'Domestic Shorthair Mix') | (df['Breed'] == 'Domestic Shorthair')]

# drop rows with missing values
altered_df.dropna(axis=0, inplace = True)
# reset the index of the dataframe
altered_df.reset_index(inplace=True, drop=True)

# ---------------------------------------------------------------------------------------- #
# SAVE ALTERED DATA TO .CSV

# gets the second command line argument (name of the altered dataset file to create)
altered_filename = sys.argv[2]

altered_df.to_csv(altered_filename)

print(f'job finished successfully')