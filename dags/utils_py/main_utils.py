import time
from loguru import logger
import os
import json

from utils_py.preprocssing_data_utils import prepare_data_to_insert

def load_raw_data(hdfs_conn, config):
    if config["hdfs"]["load_raw_data"] == True:
        for ticker in config["data_conf"]["ticker_list"]:

            logger.info(ticker)

            # make dir in HDFS
            dir_hdfs_ticker = f"/data_pulse_api/{ticker}"
            logger.debug(f"Check dir hdfs exists {dir_hdfs_ticker}")
            logger.debug("Status:")
            hdfs_conn.mkdir(dir_hdfs_ticker)

            logger.debug("start load data...")
            path_data = "/opt/airflow/airflow_data/data_samples"
            files = os.listdir(path_data)
            for json_file in files:
                file_path = os.path.join(path_data, json_file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                hdfs_file_write = f"""{dir_hdfs_ticker}/{data["id"]}-{data["inserted"][:10]}.json"""
                hdfs_conn.write_file(data, hdfs_file_path=hdfs_file_write)
                logger.debug(f"save raw file to hdfs: {hdfs_file_write}")
                time.sleep(1)
    else:
        logger.info("Skip raw data")

def load_core_data(hdfs_conn, pg_conn, config):
    if config["postgres"]["load_core_data"] == True:
        for ticker in config["data_conf"]["ticker_list"]:

            # list HDFS files in dir
            list_files = hdfs_conn.list_files(f"""/data_pulse_api/{ticker}""")
            for file_i in list_files:

                hdfs_file_load = f"""/data_pulse_api/{ticker}/{file_i}"""

                # read files from hdfs
                data_raw = hdfs_conn.read_files(hdfs_file_load)
                logger.debug(f"read raw file: {data_raw}")

                # preproc data to core data
                logger.debug(f"preproc raw to core")
                data_core = prepare_data_to_insert(data_raw)

                # write core data to PG
                logger.debug(f"insert core to PG")
                pg_conn.insert_data(data_core, schema_name="core_data", table_name="content_table")
    else:
        logger.info("Skip core data")