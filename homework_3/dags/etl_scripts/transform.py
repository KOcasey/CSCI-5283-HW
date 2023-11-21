# Import Packages
import pandas as pd
from sklearn import preprocessing
from pathlib import Path

# TRANSFORM DATA
def transform_data(source_csv, target_dir):
    print('Transforming Data...')
    outcomes_df = pd.read_csv(source_csv)

    # # change column names
    # outcomes_df = outcomes_df.rename(columns={'Animal ID': 'animal_id', 'Name': 'animal_name', 'DateTime': 'ts', 'Date of Birth': 'dob', 'Outcome Type': 'outcome_type', 'Outcome Subtype': 'outcome_subtype',
    #                             'Animal Type':'animal_type', 'Sex upon Outcome':'sex_outcome', 'Age upon Outcome':'age', 'Breed':'breed', 'Color':'color'})
   # change column names
    outcomes_df = outcomes_df.rename(columns={'name': 'animal_name', 'datetime': 'ts', 'date_of_birth': 'dob', 'sex_upon_outcome':'sex_outcome', 'age_upon_outcome':'age'})

    # convert ts from string to datetime
    outcomes_df['ts'] = pd.to_datetime(outcomes_df['ts'])

    # drop 'MonthYear'
    outcomes_df = outcomes_df.drop(['monthyear'], axis=1)

    # 'outcome_subtype' has over 50% of values missing so will just remove that column
    #outcomes_df = outcomes_df.drop(['outcome_subtype'], axis=1)

    # there are 283 animals without names, this is fine since some animals in shelters don't have names yet, will replace NaN with 'Unnamed'
    outcomes_df['animal_name'] = outcomes_df['animal_name'].fillna('Unnamed')

    # there are '*' at beginning of some names, need to remove
    outcomes_df['animal_name'] = outcomes_df['animal_name'].str.replace('*', '')

    # -------------------------------------------------------------------------------------#
    ## animals_dim_df
    animals_dim_df = outcomes_df[['animal_id', 'animal_name', 'animal_type', 'breed', 'color', 'dob', 'sex_outcome', 'age']].copy()

    # change age to int
    animals_dim_df['age'] = animals_dim_df['age'].fillna('9999')

    animals_dim_df.age = animals_dim_df.age.apply(lambda x: x.replace(' years', '') if 'years' in x else x)
    animals_dim_df.age = animals_dim_df.age.apply(lambda x: x.replace(' year', '') if 'year' in x else x)
    animals_dim_df.age = animals_dim_df.age.apply(lambda x: str(int(x.replace(' months', '')) / 12) if 'months' in x else x)
    animals_dim_df.age = animals_dim_df.age.apply(lambda x: str(int(x.replace(' month', '')) / 12) if 'month' in x else x)
    animals_dim_df.age = animals_dim_df.age.apply(lambda x: str(int(x.replace(' weeks', '')) / 52) if 'weeks' in x else x)
    animals_dim_df.age = animals_dim_df.age.apply(lambda x: str(int(x.replace(' week', '')) / 52) if 'week' in x else x)
    animals_dim_df.age = animals_dim_df.age.apply(lambda x: str(int(x.replace(' days', '')) / 365) if 'days' in x else x)
    animals_dim_df.age = animals_dim_df.age.apply(lambda x: str(int(x.replace(' day', '')) / 365) if 'day' in x else x)

    animals_dim_df['age'] = pd.to_numeric(animals_dim_df['age']).round(2)

    # remove duplicates
    animals_dim_df = animals_dim_df.drop_duplicates(subset='animal_id')

    # sort and reset indices
    animals_dim_df = animals_dim_df.sort_values(by=['animal_id']).reset_index(drop=True)

    # -------------------------------------------------------------------------------------#
    ## outcome_type_dim_df
    outcome_type_dim_df = outcomes_df[['outcome_type']].copy()

    # create outcome_type_id
    outcome_type_dim_df['outcome_type_id'] = outcome_type_dim_df.replace({'outcome_type' : {'Adoption': 0, 'Died':1, 'Disposal':2, 'Euthanasia':3, 'Return to Owner':4, 'Rto-Adopt':5, 'Transfer':6}})

    # rearrange columns
    outcome_type_dim_df = outcome_type_dim_df[['outcome_type_id', 'outcome_type']]

    # remove duplicates
    outcome_type_dim_df = outcome_type_dim_df.drop_duplicates()

    # sort and reset indices
    outcome_type_dim_df = outcome_type_dim_df.sort_values(by=['outcome_type_id']).reset_index(drop=True)

    # -------------------------------------------------------------------------------------#
    ## outcome_subtype_dim_df
    outcome_subtype_dim_df = outcomes_df[['outcome_subtype']].copy()

    # create outcome_subtype_id
    le = preprocessing.LabelEncoder()
    le.fit(outcome_subtype_dim_df['outcome_subtype'])
    outcome_subtype_dim_df['outcome_subtype_id'] = le.transform(outcome_subtype_dim_df['outcome_subtype'])

    # rearrange columns
    outcome_subtype_dim_df = outcome_subtype_dim_df[['outcome_subtype_id', 'outcome_subtype']]

    # remove duplicates
    outcome_subtype_dim_df = outcome_subtype_dim_df.drop_duplicates()

    # sort and reset indices
    outcome_subtype_dim_df = outcome_subtype_dim_df.sort_values(by=['outcome_subtype_id']).reset_index(drop=True)

    # -------------------------------------------------------------------------------------#
    ## date_dim_df
    date_dim_df = outcomes_df[['ts']].copy()

    # extract day of week
    date_dim_df['day'] = outcomes_df['ts'].dt.day
    date_dim_df['month'] = outcomes_df['ts'].dt.month
    date_dim_df['year'] = outcomes_df['ts'].dt.year
    date_dim_df['dow'] = outcomes_df['ts'].dt.dayofweek

    # create date_id
    date_dim_df['date_id'] = date_dim_df.index

    # rearrange columns
    date_dim_df = date_dim_df[['date_id', 'year', 'month', 'day', 'dow']]

    # -------------------------------------------------------------------------------------#
    ## outcomes_fct_df
    outcomes_fct_df = outcomes_df[['animal_id', 'outcome_type', 'outcome_subtype']].copy()

    outcomes_fct_df['outcome_type'] = outcomes_fct_df['outcome_type'].fillna('N/A')
    outcomes_fct_df['outcome_subtype'] = outcomes_fct_df['outcome_subtype'].fillna('N/A')

    outcomes_fct_df = outcomes_fct_df.replace({'outcome_type' : {'Adoption': 0, 'Died':1, 'Disposal':2, 'Euthanasia':3, 'Return to Owner':4, 'Rto-Adopt':5, 'Transfer':6, 'Missing':7, 'Relocate':8, 'N/A':9, 'Stolen':10}})

    outcomes_fct_df = outcomes_fct_df.replace({'outcome_subtype' : {'Aggressive': 0, 'At Vet':1, 'Emergency':2, 'Enroute':3, 'Field':4, 'Foster':5, 'In Kennel':6, 'Offsite':7, 'Out State':8, 'Partner':9, 'Rabies Risk':10, 'SCRP':11, 'Snr':12, 'Suffering':13, 'Underage':14,
                                            'N/A':15, 'Court/Investigation':16, 'In Foster': 17, 'Behavior':18, 'Medical':19, 'Possible Theft':20, 'Barn':21, 'Customer S':22, 'Emer':23, 'In Surgery':24, 'In State':25, 'Prc':26}})

    outcomes_fct_df = outcomes_fct_df.rename(columns={'Animal ID': 'animal_id', 'outcome_type': 'outcome_type_id', 'outcome_subtype':'outcome_subtype_id'})

    outcomes_fct_df['outcome_subtype_id'] = outcomes_fct_df['outcome_subtype_id'].fillna(15)

    outcomes_fct_df['date_id'] = outcomes_fct_df.index

    # save transformed dataframes
    Path(target_dir).mkdir(parents=True, exist_ok=True)

    animals_dim_df.to_parquet(target_dir+'/animals_dim_df.parquet')
    outcome_type_dim_df.to_parquet(target_dir+'/outcome_type_dim_df.parquet')
    outcome_subtype_dim_df.to_parquet(target_dir+'/outcome_subtype_dim_df.parquet')
    date_dim_df.to_parquet(target_dir+'/date_dim_df.parquet')
    outcomes_fct_df.to_parquet(target_dir+'/outcomes_fct_df.parquet')