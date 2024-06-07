from datetime import timedelta
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'chathu',
    'start_date': days_ago(0),
    'email': ['geethcy@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='sample-etl-dag',
    default_args=default_args,
    description='Sample ETL DAG using Bash',
    schedule_interval=timedelta(days=1),
)

extract_transform_and_load = BashOperator(
    task_id='extract_transform_and_load',
    bash_command='/home/project/airflow/dags/bashdag.sh "',
    dag=dag,
)

extract_transform_and_load

# When the task extract_transform_and_load is executed,
# the code in the shell script gets executed.
