import requests
import time
import json
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago


def get_data(**kwargs):
    api_key = 'API_KEY'
    tickers = kwargs['tickers']
    for ticker in tickers:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}'
        response = requests.get(url)
        

default_dag_args = {
    'start_date': datetime(2022, 9, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'project_id': 1
}


with DAG("market_data_alphavantage_dag", schedule_interval='@daily', catchup=False, default_args=default_dag_args) as dag:
    
    task_0 = PythonOperator(
        task_id="get_market_data",
        python_callable=get_data,
        op_kwargs={'tickers': ['AAPL', 'GOOGL', 'AMZN']}  
    )
