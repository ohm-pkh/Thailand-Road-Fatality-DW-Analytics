from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta
from src.extract.extract_date import extract_date
from src.extract.extract_icd10 import extract_icd10
from src.extract.extract_location import extract_location
from src.extract.extract_province_shortname import extract_province_shortname
from src.extract.extract_nationality import extract_adjectival_nationality,extract_main_nationality
from src.extract.extract_fatality import extract_accident

default_args = {
    'owner': 'Owner',
    'start_date': datetime(2026,7,7),
    'retries': 1,
    'retry_delay':timedelta(minutes=5)
}

dag = DAG(
    dag_id="Accident_fatality_DAG",
    description="ETL pipeline for handle accident fatality data",
    default_args=default_args,
    schedule=None,
)

task_extract_date = PythonOperator(
    task_id="extract_date",
    python_callable=extract_date,
    dag = dag
)

task_extract_icd_10 = PythonOperator(
    task_id="extract_ICD10",
    python_callable=extract_icd10,
    dag = dag
)

task_extract_location = PythonOperator(
    task_id="extract_location",
    python_callable=extract_location,
    dag = dag
)

task_extract_province_shortname = PythonOperator(
    task_id="extract_province_shortname",
    python_callable=extract_province_shortname,
    dag=dag
)

task_extract_nationality_ISO3166 = PythonOperator(
    task_id="extract_nationality_ISO3166",
    python_callable=extract_main_nationality,
    dag=dag
)

task_extract_nationality_adjectival = PythonOperator(
    task_id="extract_nationality_adjectival",
    python_callable=extract_adjectival_nationality,
    dag=dag
)

task_extract_main_dataset = PythonOperator(
    task_id="extract_accident_data",
    python_callable=extract_accident,
    dag=dag
)

task_extract_date

task_extract_icd_10

task_extract_location

task_extract_province_shortname

task_extract_nationality_ISO3166

task_extract_nationality_adjectival

task_extract_main_dataset