# spark-batch

Install
```
pip install spark-batch==0.2

python -m spark_batch.run
```


Full load
```
python -m spark_batch.run ingest_full --config src/spark_batch/lib/config.yaml   --source_type oracle1 --source_topic bcparking --target_type delta1 --target_topic bronze-bcparking --source_objects tb_tmparking --target_object tb_tmparking --batch_size 500000
```


Config
```
oracle1:
  source_type: oracle
  connection_url: jdbc:oracle:thin:@10.2.0.14:1521:ORCLCDB
  connection_properties:
    user: user
    password: password
    driver: oracle.jdbc.OracleDriver

postgresql1:
  source_type: postgresql
  connection_url: jdbc:postgresql://10.43.113.64:5432/mart
  connection_properties:
    user: user
    password: password
    driver: org.postgresql.Driver

delta1:
  source_type: delta
```
