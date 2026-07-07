from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Default arguments mimicking an enterprise aviation tracking environment
default_args = {
'owner': 'luel_data_ops',
'depends_on_past': False,
'start_date': datetime(2026, 7, 1),
'email_on_failure': False,
'email_on_retry': False,
'retries': 2,
'retry_delay': timedelta(minutes=5),
}

# Define the core production workflow scheduler
with DAG(
'aviation_live_flight_orchestration',
default_args=default_args,
description='Automated orchestration pipeline extracting live transponder logs for global fleets',
schedule_interval=timedelta(days=1), # Run automatically every single day
catchup=False,
tags=['aviation', 'multi_cloud', 'mlops'],
) as dag:

# Task 1: Initialize environment check
verify_env = BashOperator(
task_id='verify_pipeline_environment',
bash_command='echo "Initializing environment verification at $(date)"',
)

# Task 2: Trigger our containerized Python extraction engine script
extract_live_telemetry = BashOperator(
task_id='execute_flight_data_extraction',
bash_command='python /app/extract_flight_data.py',
)

# Define the absolute chronological execution roadmap
verify_env >> extract_live_telemetry
