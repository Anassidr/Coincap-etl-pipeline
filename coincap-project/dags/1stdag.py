import airflow
from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor


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

with DAG('coincap_pipeline', default_args=default_args, schedule_interval="@daily", catchup=False) as dag:


    # Dag #1 - Check if the API is available
    is_api_available = HttpSensor(
        task_id='is_api_available',
        method='GET',
        http_conn_id='is_api_available',
        endpoint= 'v2/assets/bitcoin/history?interval=d1',
        response_check= lambda response: 'Usd' in response.text,
        poke_interval = 5
    )