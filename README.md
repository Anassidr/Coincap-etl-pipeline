# Coincap-etl-pipeline
## Using Airflow and Docker to fetch bitcoin data from the Coincap API and store it in postgres on a daily basis. 

### Steps of this project: 

#### 1. Set up the [docker-compose file](https://github.com/Anassidr/Coincap-etl-pipeline/blob/main/coincap-project/docker-compose.yaml) for airflow.

#### 2. Set up the [DAG.py file](https://github.com/Anassidr/Coincap-etl-pipeline/blob/main/coincap-project/dags/ETL_dag.py) with the following sequence of tasks:
  - Use the HTTPSensor Operator to make sure the API is functional
  - Use the Postgres Operator to create a table in the postgres container
  - Use the SimpleHttp Operator to get the data from the endpoint and store it in Xcom
  - Use a Python Operator to pull the data from Xcom, process it with Pandas and store it in a .csv
  - Use a Python Operator to load the data from the .csv to my postgres database using PostgresHook
  - Use the PgAdmin2 interface to make queries on my postgres database 
  
![image](https://user-images.githubusercontent.com/109003970/222769342-7847983c-135a-41f5-a005-1c71df9295b4.png)


### Next steps for this project: 
#### 1. Deploy the containers on the cloud (GCP).
#### 2. Use the bitcoin hourly prices that we fetched for some DataScience 

