from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator


with DAG(
    dag_id="Weather_etl",
    start_date=datetime(year=2025, month=2, day=18),
    schedule="@hourly",
    catchup=False,
    max_active_runs=1,
    render_template_as_native_obj=True,
) as dag:
    extract_task = DockerOperator(
        task_id="extract",
        image="weather_de-app:latest",  
        command="python weather_etl/extract.py",
        docker_url="unix://var/run/docker.sock",  # Ensure Airflow can communicate with Docker daemon
        network_mode="bridge",
        force_pull=False,
    )

    transform_task = DockerOperator(
        task_id="transform",
        image="weather_de-app:latest",
        command="python weather_etl/transform.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
    )

    load_task = DockerOperator(
        task_id="load",
        image="weather_de-app:latest",
        command="python weather_etl/load.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
    )

    extract_task >> transform_task >> load_task