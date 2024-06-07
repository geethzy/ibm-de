from datetime import timedelta
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'chathu',
    'start_date': days_ago(0),
    'email': ['geethcy@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ETL_Server_Access_Log_Processing',
    default_args=default_args,
    description='My first DAG',
    schedule_interval=timedelta(days=1),
)

extract_transform_and_load = BashOperator(
    task_id="extract_transform_and_load",
    bash_command="/home/project/airflow/dags/ETL_Server_Access_Log_Processing.sh ",
    dag=dag,
)

extract_transform_and_load

# shell-------

# #!/bin/bash
# echo "extract_transform_load"
# # cut command to extract the fields timestamp and visitorid writes to a new file extracted.txt
# cut -f1,4 -d"#" /home/project/airflow/dags/web-server-access-log.txt > /home/project/airflow/dags/extracted.txt

# # tr command to transform by capitalizing the visitorid.
# tr "[a-z]" "[A-Z]" < /home/project/airflow/dags/extracted.txt > /home/project/airflow/dags/capitalized.txt

# # tar command to compress the extracted and transformed data.
# tar -czvf /home/project/airflow/dags/log.tar.gz /home/project/airflow/dags/capitalized.txt