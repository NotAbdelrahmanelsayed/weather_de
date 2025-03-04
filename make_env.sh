cat > .env << EOL
AIRFLOW_UID=50000
AIRFLOW_GID=0
DOCKER_GID=$(getent group docker | cut -d: -f3)
DATA_DIR=$(pwd)/data
CONFIG_PATH=$(pwd)/configuration.conf
AIRFLOW_IMAGE_NAME=apache/airflow:2.10.5
EOL