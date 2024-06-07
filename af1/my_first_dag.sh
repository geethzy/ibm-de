#!/bin/bash
echo "extract_transform_and_load"
cut -d":" -f1,3,6 /etc/passwd > /home/project/airflow/dags/extracted-data.txt

tr ":" "," < /home/project/airflow/dags/extracted-data.txt > /home/project/airflow/dags/transformed-data.csv

# The shell script extracts the first,third and sixth fields from /etc/passwd file using the cut command and writes to a new file extracted-data.txt
# Next the extracted-data.txt is transformed to a csv file and loaded into a new file called transformed-data.csv using tr command.
# this shell script can be called by dag.py

#  cp my_first_dag.sh $AIRFLOW_HOME/dags - copies the file 
#  cd airflow/dags - changes the current directory
#  chmod 777 my_first_dag.sh - allow read, write, and execute access for all users