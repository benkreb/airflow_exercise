import time
import json
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from datetime import timedelta
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

create_query = """
CREATE TABLE employee (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    age INT
);
"""

insert_data_query = """
INSERT INTO employee (name, age)
VALUES
    ('John', 30),
    ('Jane', 25),
    ('Michael', 28);
"""

calculating_average_age = """
SELECT AVG(age) FROM employee;
"""


dag_postgres = DAG(
    dag_id="postgres_dag_connection",
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1)
)

create_table = PostgresOperator(
    task_id="creation_of_table",
    sql=create_query,
    dag=dag_postgres,
    postgres_conn_id="postgres_pedro_local"
)

insert_data = PostgresOperator(
    task_id="insertion_of_data",
    sql=insert_data_query,
    dag=dag_postgres,
    postgres_conn_id="postgres_pedro_local"
)

calculate_average_age = PostgresOperator(
    task_id="calculating_average_age",
    sql=calculating_average_age,
    dag=dag_postgres,
    postgres_conn_id="postgres_pedro_local"
)

create_table >> insert_data >> calculate_average_age
