## To launch producer script

```
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,com.datastax.spark:spark-cassandra-connector_2.12:3.0.0  producer.py 
```

## To launch consumer script

```
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 consumer.py 
```
