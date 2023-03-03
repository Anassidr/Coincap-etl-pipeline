# Coincap-etl-pipeline
## Using Airflow and Docker to ingest bitcoin data daily from the Coincap API to a postgres database

### Steps of this project: 

#### 1. Set up the docker-compose file for airflow.

#### 2. Set up the DAG.py file with the following sequence of tasks:
  - Use the HTTPSensor Operator to make sure the API is functional
  - Use the Postgres Operator to create the table in the postgres container
  - Use the SimpleHttpOperator to get the data from the endpoint and store it in Xcom
  - Use a PythonOperator to pull the data from Xcom, process it with Pandas and store it in a .csv
  - Use a PythonOperator to load the data from the .csv to my postgres database using PostgresHook
  - Use the PgAdmin2 interface to make queries on my postgres database 
  
  ![image](https://user-images.githubusercontent.com/109003970/222764614-ae9913da-4fd1-475f-860f-a729c1b3601c.png)


### Next step for this project: 
#### - Deploy the containers on the cloud (GCP). 
