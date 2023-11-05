# 소스 대상 초기화 
from lib.oracle_table_manager import OracleTableManager
from lib.delta_table_manager import DeltaTableManager
from lib.postgresql_table_manager import PostgreSQLTableManager
from lib.pxlogger import CustomLogger

import yaml

class ResourceManager:
    def __init__(self, spark, config_file="config.yaml"):
        self.spark = spark
        self.logger = CustomLogger("ResourceManager")
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
            self.logger.debug(("config keys=", config.keys()))
        return config

    def get_resource_manager(self, source_type, topic, *args, **kwargs):
        if source_type in self.config:
            source_config = self.config[source_type]
            connection_url = source_config.get("connection_url")
            connection_properties = source_config.get("connection_properties", {})
            source_type_name = source_config.get("source_type")
            
            #self.logger.debug(("source_type=", source_type, "source_type_name=", source_type_name))
            
            if source_type_name == "oracle":
                return self._get_OracleTableManager(connection_url, connection_properties, topic)
            elif source_type_name == "postgresql":
                return self._get_PostgreSQLTableManager(connection_url, connection_properties, topic)
            elif source_type_name == "delta":
                dpath = kwargs.get("dpath", None)
                return self._get_DeltaTableManager(topic, dpath)
            else:
                raise ValueError("Unsupported source type: " + source_type)
        else:
            raise ValueError("Source type not found in config: " + source_type)

    def _get_OracleTableManager(self, connection_url, connection_properties, topic):
        return OracleTableManager(self.spark, connection_url, connection_properties, topic)

    def _get_PostgreSQLTableManager(self, connection_url, connection_properties, topic):
        return PostgreSQLTableManager(self.spark, connection_url, connection_properties, topic)

    def _get_DeltaTableManager(self, topic, dpath=None):
        return DeltaTableManager(self.spark, bucket=topic, dpath=dpath)

  
# ## Samples
# from ResourceManager import ResourceManager
# config_file = "config.yaml"  # 설정 파일의 경로
# resource_manager = ResourceManager(spark, config_file)
#
# config.yaml
# ---- 
# oracle-pj1:
#   source_type: oracle
#   connection_url: jdbc:oracle:thin:@10.2.0.14:1521:ORCLCDB
#   connection_properties:
#     user: user
#     password: password
#     driver: oracle.jdbc.OracleDriver
# postgresql-pj1:
#   source_type: postgresql
#   connection_url: jdbc:postgresql://10.43.113.64:5432/mart
#   connection_properties:
#     user: user
#     password: password
#     driver: org.postgresql.Driver

# delta_manager = resource_manager.get_source_manager("delta", topic="my_bucket", dpath="aaa")
# delta_manager.loadTable("my_table")

# # OracleTableManager 객체 생성 및 함수 호출
# oracle_manager = resource_manager.get_source_manager("oracle")
# oracle_manager.loadTable("my_oracle_table")


