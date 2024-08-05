import json

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator

from datetime import datetime, timedelta
from loguru import logger

from utils_py.pg_utils import PostgresConnector
from utils_py.hdfs_utils import HDFSConnector
from utils_py.main_utils import load_raw_data, load_core_data

# Установите аргументы по умолчанию для DAG
default_args = {
    "owner": "Dobrin_dev",
    "depends_on_past": False,
    "start_date": datetime.now(),
    "email_on_failure": True,
    "email_on_retry": False,
    "email": "example@mail.ru",
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

# read config conn and setup
with open("/opt/airflow/dags/config_dag/config.json", "r", encoding="utf-8") as file:
    content = file.read()
    config = json.loads(content)
    file.close()
    logger.debug(config)

# Определите DAG
dag = DAG(
    "load_raw_data",
    default_args=default_args,
    description="Пример pipeline загрузки данных",
    tags=["etl", "hdfs", "postgres"],
    schedule_interval="0 3 * * *", 
)

# Python функция, которая будет выполнена в задаче task2
def load_raw_data_f():
    logger.add("airflow.log", mode="w", level="DEBUG")
    logger.debug("---LOG MODE DEBUG RUN---")
    
    # init object connectors to services
    logger.info("Init object connectors to services...")
    pg_conn = PostgresConnector(
        dbname=config["postgres"]["dbname"]
        ,user=config["postgres"]["user"]
        ,host=config["postgres"]["host"]
        ,password=config["postgres"]["password"]
    )
    logger.debug("Init pg_conn done")
    hdfs_conn = HDFSConnector(
        hdfs_host=config["hdfs"]["hdfs_host"]
    )
    logger.info("Init object DONE")

    # init db pg
    logger.info("Init database Postgres...")
    pg_conn.init_database(config["postgres"]["path_init_sql"], config["postgres"]["init_db"])
    logger.info("Init database DONE")

    # load data from API PULSE to HDFS
    logger.info("Load data...")
    load_raw_data(hdfs_conn, config)
    logger.info("Load raw data DONE")  
    
def load_core_data_f():
    
    pg_conn = PostgresConnector(
        dbname=config["postgres"]["dbname"]
        ,user=config["postgres"]["user"]
        ,host=config["postgres"]["host"]
        ,password=config["postgres"]["password"]
    )
    logger.debug("Init pg_conn done")
    hdfs_conn = HDFSConnector(
        hdfs_host=config["hdfs"]["hdfs_host"]
    )
    
    logger.info("Start load core data...")
    load_core_data(hdfs_conn, pg_conn, config)
    logger.info("Load core data DONE")

# Создание задачи с использованием PythonOperator
load_raw_data_step = PythonOperator(
    task_id="load_raw_data_step",
    python_callable=load_raw_data_f,
    dag=dag,
)

load_core_data_step = PythonOperator(
    task_id="load_core_data_step",
    python_callable=load_core_data_f,
    dag=dag,
)

preproc_core_data_step = PostgresOperator(
    task_id="preproc_core_data_step",
    postgres_conn_id="pg_conn",
    sql="""
    INSERT INTO core_data.count_content_by_user(nickname, cnt_content)
    SELECT nickname, count(id) AS cnt_content
    FROM core_data.content_table GROUP BY nickname;""",
    dag=dag,
)

# Определение порядка выполнения задач
load_raw_data_step >> load_core_data_step >> preproc_core_data_step