import airflow
from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator

import json


from datetime import datetime, timedelta
from pendulum import date

# Grab current date
current_date = datetime.today().strftime('%Y-%m-%d')


# Default settings for all the dags in the pipeline
default_args = {

    "owner": "Airflow", 
    "start_date" : datetime(2023,3,1),
    "retries" : 1,
    "retry_delay": timedelta(minutes=5)

}

with DAG('api_dag', default_args=default_args, schedule_interval="@daily", catchup=False) as dag:


    # Dag #1 - Check if the API is available
    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='api_call',
        endpoint= '/bitcoin/history?interval=d1'
    )