from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="Weather_etl",
    start_date=datetime(year=2025, month=2, day=18),
    schedule="@hourly",
    catchup=True,
    max_active_runs=1,
    render_template_as_native_obj=True
) as dag:
    extract = BashOperator(
        dag=dag,
        task_id="extract",
        bash_command="weather_etl-extract")
    transform = BashOperator(
        dag=dag,
        task_id="transform",
        bash_command="weather_etl-transform")
    load = BashOperator(
        dag=dag,
        task_id="load",
        bash_command="weather_etl-load")
    
    extract >> transform >> load