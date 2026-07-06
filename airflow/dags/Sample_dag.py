from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta
from src.extract.extract_try import try_extract
from src.transform.transform_try import try_transform
from src.load.try_load import try_load

default_args = {
    'owner': 'Owner',
    'start_date': datetime(2026,7,6),
    'retries': 1,
    'retry_delay':timedelta(minutes=5)
}

dag = DAG(
    'My_sample_DAG',
    description='A Sample dag use to test system setting',
    default_args= default_args,
    schedule = None
)

task1 = PythonOperator(
    task_id = "try_extract_with_minio",
    python_callable = try_extract,
    dag=dag
)

task2 = PythonOperator(
    task_id = "try_transform_with_minio",
    python_callable = try_transform,
    dag=dag
)

task3 = PythonOperator(
    task_id = "try_load_with_psql",
    python_callable = try_load,
    dag=dag
)


task1 >> task2 >> task3