# Use following syntax in bash shell:
# docker build -t container_name .
# winpty docker run -it container_name arg1 arg2

import sys
import pandas as pd

# ---------------------------------------------------------------------------------------- #
# READ IN DATA
def load_data(filename):
    print('Loading Data...')
    df = pd.read_csv(filename) # read in csv based on command line argument
    return df

# ---------------------------------------------------------------------------------------- #
# DATASET CHANGES
def transform_data(dataframe):
    print('Transforming Data...')
    altered_df = dataframe.copy()
    # select only cats that are of the domestic shorthair breed
    altered_df = altered_df.loc[altered_df['Animal Type'] == 'Cat']
    altered_df = altered_df.loc[(altered_df['Breed'] == 'Domestic Shorthair Mix') | (altered_df['Breed'] == 'Domestic Shorthair')]

    # drop rows with missing values
    altered_df.dropna(axis=0, inplace = True)
    # reset the index of the dataframe
    altered_df.reset_index(inplace=True, drop=True)

    return altered_df


# ---------------------------------------------------------------------------------------- #
# SAVE ALTERED DATA TO .CSV
def save_data(dataframe, filename):
    print('Saving Data...')
    dataframe.to_csv(filename)

# ---------------------------------------------------------------------------------------- #
# MAIN (Runs functions)
if __name__ == "__main__":
    print('Starting...')

    print(sys.argv) # prints the name of the file and the command line argument(s)
    # gets the first command line argument (name of the dataset file)
    filename = sys.argv[1]
    # gets the second command line argument (name of the altered dataset file to create)
    save_filename = sys.argv[2]

    df = load_data(filename)
    altered_df = transform_data(df)
    save_data(altered_df, save_filename)

    print(f'Job finished successfully!')