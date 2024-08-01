import hdfs
import json

from loguru import logger
from json import dump, dumps

class HDFSConnector:
    def __init__(self, hdfs_host="http://namenode:9870"):
        self.hdfs_host = hdfs_host
        logger.info("connect to hdfs...")
        logger.info(f"creds hdfs: {self.hdfs_host}")
        try:
            self.client = hdfs.InsecureClient(hdfs_host, timeout=60)
            self.client.status("/")
        except:
            logger.error("I am unable to connect to the HDFS")
            raise ConnectionAbortedError("I am unable to connect to the HDFS")
        # logger.add('logs/main_log.log', level='DEBUG')

    def mkdir(self, hdfs_dir_path: str) -> None:
        logger.debug(self.client.status(hdfs_dir_path, strict=False))
        # if not self.client.status(hdfs_dir_path, strict=False):
        #     self.client.makedirs(hdfs_dir_path)

    def write_file(self, data:dict, hdfs_file_path: str) -> None:
        self.client.write(hdfs_file_path, data=json.dumps(data), overwrite=True, encoding='utf-8')

    def read_files(self, hdfs_file_path: str) -> dict:
        with self.client.read(hdfs_file_path, encoding='utf-8') as reader:
            content = json.loads(reader.read())
        return content

    def clean_dir(self, hdfs_file_path: str) -> None:
        logger.debug(f"""clean path: {hdfs_file_path+"/*"}""")
        self.client.delete(hdfs_file_path+"/*")

    def list_files(self, hdfs_path: str) -> None:
        # get file list of directory
        file_list = self.client.list(hdfs_path)

        # print list
        logger.debug(f"HDFS ls dir: {hdfs_path}")
        for file_or_dir in file_list[:5]:
            logger.debug(file_or_dir)
        return file_list







