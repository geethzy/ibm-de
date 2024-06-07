from datetime import timedelta
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'geeth',
    'start_date': days_ago(0),
    'email': ['gee@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)

unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='unzip /home/project/airflow/dags/finalassignment/staging/tolldata.zip -d /home/project/airflow/dags/finalassignment/staging/',
    dag=dag,
)

extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command='cut -f1-4 -d"," /home/project/airflow/dags/finalassignment/staging/tolldata/vehicle-data.csv > /home/project/airflow/dags/finalassignment/staging/tolldata/csv_data.csv',
    dag=dag,
)

extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command='cut -f5-7 -d"," /home/project/airflow/dags/finalassignment/staging/tolldata/tollplaza-data.csv > /home/project/airflow/dags/finalassignment/staging/tolldata/tsv_data.csv',
    dag=dag,
)

extract_data_from_fixed_width = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command='cut -c58-60, -c61-66 -d"," /home/project/airflow/dags/finalassignment/staging/tolldata/payment-data.txt > /home/project/airflow/dags/finalassignment/staging/tolldata/fixed_width_data.csv',
    dag=dag,
)

consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command='paste /home/project/airflow/dags/finalassignment/staging/tolldata/csv_data.csv /home/project/airflow/dags/finalassignment/staging/tolldata/tsv_data.csv /home/project/airflow/dags/finalassignment/staging/tolldata/fixed_width_data.csv > /home/project/airflow/dags/finalassignment/staging/tolldata/extracted_data.csv',
    dag=dag,
)

transform_data = BashOperator(
    task_id='transform_data',
    bash_command='tr "[a-z]" "[A-Z]" < /home/project/airflow/dags/finalassignment/staging/tolldata/extracted_data.csv > /home/project/airflow/dags/finalassignment/staging/tolldata/transformed_data.csv',
    dag=dag,
)

unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data

