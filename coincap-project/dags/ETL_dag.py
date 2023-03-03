import airflow
from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator



import pandas as pd 
import json


from datetime import datetime, timedelta
from pendulum import date

# Grab current date
current_date = datetime.today().strftime('%Y-%m-%d')

def _process_data(ti):
    data = ti.xcom_pull(task_ids = 'extract_data')
    df = pd.DataFrame.from_dict(json.loads(json.dumps(data['data'])))
    df['hour'] = pd.to_datetime(df['date']).dt.hour
    df['date'] = df['date'].apply(lambda x: pd.to_datetime(x).date())
    df.to_csv('/tmp/processed_data.csv', index=None, header=False)
    




# Default settings for all the dags in the pipeline
default_args = {

    "owner": "Airflow", 
    "start_date" : datetime(2023,3,1),
    "retries" : 1,
    "retry_delay": timedelta(minutes=5)

}

with DAG('ETL_dag', default_args=default_args, schedule_interval="@daily", catchup=False) as dag:


    # Task 1 : Check if the API is available
    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='api_call',
        endpoint= '/bitcoin/history?interval=h1'
    )


    # Task 2 : Create postgres table 
    create_table = PostgresOperator(
        task_id = 'create_table',
        postgres_conn_id='postgres',
        sql='''
            drop table if exists rates;
            drop table if exists bitcoin_data; 
            create table bitcoin_data(
                priceUsd float not null,
                time int not null,
                circulatingsupply float not null,
                date date not null,
                hour int not null
            );
        '''
    )

    extract_data = SimpleHttpOperator(
        task_id = 'extract_data',
        http_conn_id='api_call',
        method='GET',
        endpoint= '/bitcoin/history?interval=h1',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    transform_data = PythonOperator(
        task_id = 'transform_data',
        python_callable=_process_data

    )

    is_api_available >> create_table >> extract_data

