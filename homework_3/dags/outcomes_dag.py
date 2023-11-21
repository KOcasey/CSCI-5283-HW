# Imports
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from etl_scripts.extract import extract_data
from etl_scripts.transform import transform_data
from etl_scripts.load import load_data
from etl_scripts.load import load_fact_data



from datetime import datetime
import os

# ----------------------------------------------------- #
# ----------------------------------------------------- #


#https://data.austintexas.gov/api/views/9t4d-g238/rows.csv?date=20231118&accessType=DOWNLOAD

# ----------------------------------------------------- #
SOURCE_URL = 'https://data.austintexas.gov/api/views/9t4d-g238/rows.csv'
AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/opt/airflow')
CSV_TARGET_DIR = AIRFLOW_HOME + '/data/{{ ds }}/downloads'
CSV_TARGET_FILE = CSV_TARGET_DIR + '/outcomes_{{ ds }}.csv'

PQ_TARGET_DIR = AIRFLOW_HOME + '/data/{{ ds }}/processed'

with DAG(
    dag_id="outcomes_dag",
    start_date=datetime(2023,11,1),
    schedule_interval='@daily'
)as dag:

# ......operators
    #download data not using API
    # extract = BashOperator(
    #     task_id="extract",
    #     bash_command=f"curl --create-dirs -o {CSV_TARGET_FILE} {SOURCE_URL}"
    # )
    #download data using api
    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_data,
        op_kwargs = {
            'target_dir': CSV_TARGET_DIR,
            'date': '{{ ds }}',
            'start_date': '2023-11-01'
        }
    )
    #transform data
    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_data,
        op_kwargs = {
            'source_csv': CSV_TARGET_FILE,
            'target_dir': PQ_TARGET_DIR
        }
    )
    # load animals dim data
    load_animals_dim = PythonOperator(
        task_id="load_animals_dim",
        python_callable=load_data,
        op_kwargs = {
            'table_file': PQ_TARGET_DIR + '/animals_dim_df.parquet',
            'table_name': 'animals_dim',
            'key': 'animal_id'
        }
    )
    # load outcome type dim data
    load_outcome_type_dim = PythonOperator(
        task_id="load_outcome_type_dim",
        python_callable=load_data,
        op_kwargs = {
            'table_file': PQ_TARGET_DIR + '/outcome_type_dim_df.parquet',
            'table_name': 'outcome_type_dim',
            'key': 'outcome_type_id'
        }
    )
    # load outcome subtype type dim data
    load_outcome_subtype_dim = PythonOperator(
        task_id="load_outcome_subtype_dim",
        python_callable=load_data,
        op_kwargs = {
            'table_file': PQ_TARGET_DIR + '/outcome_subtype_dim_df.parquet',
            'table_name': 'outcome_subtype_dim',
            'key': 'outcome_subtype_id'
        }
    )
    # load date dim data
    load_date_dim = PythonOperator(
        task_id="load_date_dim",
        python_callable=load_data,
        op_kwargs = {
            'table_file': PQ_TARGET_DIR + '/date_dim_df.parquet',
            'table_name': 'date_dim',
            'key': 'date_id'
        }
    )
    # load outcomes fact data
    load_outcomes_fct = PythonOperator(
        task_id="load_outcomes_fct",
        python_callable=load_fact_data,
        op_kwargs = {
            'table_file': PQ_TARGET_DIR + '/outcomes_fct_df.parquet',
            'table_name': 'outcomes_fct'
        }
    )


extract >> transform >> [load_animals_dim, load_outcome_type_dim, load_outcome_subtype_dim, load_date_dim] >> load_outcomes_fct