from airflow import DAG
from airflow.operators.python import PythonOperator,BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime,timedelta
from src.extract.extract_date import extract_date
from src.extract.extract_icd10 import extract_icd10
from src.extract.extract_location import extract_location
from src.extract.extract_province_shortname import extract_province_shortname
from src.extract.extract_nationality import extract_adjectival_nationality,extract_main_nationality, move_nationality_to_stage
from src.extract.extract_fatality import extract_accident
from src.extract.extract_gov_2_raw import extract_data_set_from_gov

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

task_move_date = PythonOperator(
    task_id="Move_date_to_stage",
    python_callable=extract_date,
    dag = dag
)

task_move_icd_10 = PythonOperator(
    task_id="Move_ICD10_to_stage",
    python_callable=extract_icd10,
    dag = dag
)

task_move_location = PythonOperator(
    task_id="Move_location_to_stage",
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

task_move_nationality = PythonOperator(
    task_id="Move_nationality_to_stage",
    python_callable=move_nationality_to_stage,
    dag=dag,
    trigger_rule='all_success'
)

task_extract_main_dataset = PythonOperator(
    task_id="Move_accident_data_to_stage",
    python_callable=extract_accident,
    dag=dag
)

task_extract_gov = PythonOperator(
    task_id="extract_accident",
    python_callable=extract_data_set_from_gov,
    dag = dag
)

task_extract_gov >> task_extract_main_dataset

task_extract_province_shortname >> task_move_location

[task_extract_nationality_ISO3166,task_extract_nationality_adjectival] >> task_move_nationality

task_move_icd_10

task_move_date