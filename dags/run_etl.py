from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from configparser import ConfigParser

config = ConfigParser()
config.read("/usr/local/app/configuration.conf")
host_dir = config.get('host_dir', 'path')

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
        network_mode="weather_de_default",
        mounts=[
            Mount(
                source=f"{host_dir}/data",
                target="/usr/local/app/data",          # path in container
                type="bind",
            ),
            Mount(
            source=f"{host_dir}/configuration.conf",
            target="/usr/local/app/configuration.conf",
            type="bind",
            ),
        ],
        force_pull=False,
    )

    transform_task = DockerOperator(
        task_id="transform",
        image="weather_de-app:latest",
        command="python weather_etl/transform.py",
        docker_url="unix://var/run/docker.sock",
        mounts=[
            Mount(
                source=f"{host_dir}/data",
                target="/usr/local/app/data",         
                type="bind",
            ),
        ],
        network_mode="weather_de_default",
    )

    load_task = DockerOperator(
        task_id="load",
        image="weather_de-app:latest",
        command="python weather_etl/load.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="weather_de_default",
        mounts=[
            Mount(
                source=f"{host_dir}/data",
                target="/usr/local/app/data",         
                type="bind",
            ),
            Mount(
            source=f"{host_dir}/configuration.conf",
            target="/usr/local/app/configuration.conf",
            type="bind",
            ),
        ],
    )

    extract_task >> transform_task >> load_task