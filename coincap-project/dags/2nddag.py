from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime

def get_data():
    return True 



with DAG("data_extraction", start_date =datetime(2023,3,2), schedule_interval="@daily", catchup=False) as dag:
    data_extractor= PythonOperator(
        task_id="data_extractor",
        python_callable=get_data
    )

