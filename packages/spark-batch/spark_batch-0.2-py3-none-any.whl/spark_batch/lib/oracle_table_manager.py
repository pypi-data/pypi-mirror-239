from pyspark.sql import SparkSession
from .pxlogger import CustomLogger
from .util import parseSourceObject


"""
Oracle 테이블을 로드하고 저장하는 클래스.

:param spark: Spark 세션.
:param default_bucket: Delta 테이블이 저장된 기본 S3 버킷.
:param default_dpath: Delta 테이블의 기본 dpath 또는 하위 디렉토리.

사용 예시)
    # Oracle database connection settings
    oracle_connection_url = "jdbc:oracle:thin:@//<host>:<port>/<service_name>"
    oracle_properties = {
        "user": "<username>",
        "password": "<password>",
        "driver": "oracle.jdbc.OracleDriver"
    }
    q
    # Initialize OracleTableManager
    manager = OracleTableManager(spark, oracle_connection_url, oracle_properties)
"""

from pyspark.sql import SparkSession
from pyspark.sql import DataFrame

class OracleTableManager:
    def __init__(self, spark, oracle_connection_url, connection_properties, dbname=None):
        self.spark = spark
        self.oracle_connection_url = oracle_connection_url
        self.connection_properties = connection_properties
        self.dbname = dbname
        self.logger = CustomLogger("OracleTableManager")
       
    def getTablePath(self, tableName):
        return tableName if self.dbname is None else self.dbname + "." + tableName
    
    def loadTable(self, tableName, offset=None, chunk_size=100000):
        self.logger.debug(("loadTable = ", tableName, offset, chunk_size))
        
        target_table = self.getTablePath(tableName)
        self.logger.debug(("target_table = ", target_table))
        
        if offset == None:
            query = f"(SELECT * FROM {target_table})"
        else:
            query = f"(SELECT * FROM {target_table} OFFSET {offset} ROWS FETCH NEXT {chunk_size} ROWS ONLY)"
            
        oracle_df = self.spark.read \
            .format("jdbc") \
            .option("driver", "oracle.jdbc.OracleDriver") \
            .option("url", self.oracle_connection_url) \
            .option("dbtable", query) \
            .option("user", self.connection_properties["user"]) \
            .option("password", self.connection_properties["password"]) \
            .option("isolationLevel", "NONE") \
            .load()
    
        return oracle_df

    # def saveTable(self, data_frame, mode="append"):
    #     data_frame.write.jdbc(url=self.connection_properties['url'],
    #                           table=self.tableName,
    #                           mode=mode,
    #                           properties=self.connection_properties)

    
    def loadTables(self, tableNames):
        tableNames = parseSourceObject(tableNames)

        dataframes = {}

        for tableName in tableNames:
            target_table = self.getTablePath(tableName)

            df = self.spark.read.jdbc(self.oracle_connection_url, 
                                      table=target_table, 
                                      properties=self.oracle_properties)

            df.createOrReplaceTempView(tableName)
            dataframes[tableName] = df

        return dataframes
    
    
    def queryTable(self, query, tableNames=None):
        self.logger.debug(("queryTable = ", query, tableNames))
        
        oracle_df = self.spark.read \
            .format("jdbc") \
            .option("driver", "oracle.jdbc.OracleDriver") \
            .option("url", self.oracle_connection_url) \
            .option("query", query) \
            .option("user", self.connection_properties["user"]) \
            .option("password", self.connection_properties["password"]) \
            .load()
    
        return oracle_df
