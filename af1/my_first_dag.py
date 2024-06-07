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
    dag_id='sample-etl-dag',
    default_args=default_args,
    description='Sample ETL DAG using Bash',
    schedule_interval=timedelta(days=1),
)

extract = BashOperator(
    task_id='extract',
    # bash_command='echo "extract"',
    bash_command='cut -d":" -f1,3,6 /etc/passwd > /home/project/airflow/dags/extracted-data.txt',
    dag=dag,
)

transform_load= BashOperator(
    task_id='transform',
    # bash_command='echo "transform"',
    bash_command='tr ":" "," < /home/project/airflow/dags/extracted-data.txt > /home/project/airflow/dags/transformed-data.csv',
    dag=dag,
)

# load = BashOperator(
#     task_id='load',
#     bash_command='echo "load"',
#     dag=dag,
# )

extract >> transform_load

# Airflow searches for Python source files within the specified DAGS_FOLDER
# cp my_first_dag.py $AIRFLOW_HOME/dags
# airflow dags list
# airflow dags list|grep "my-first-dag"
# airflow tasks list my-first-dag