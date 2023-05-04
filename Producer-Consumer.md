## To launch producer script

```
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,com.datastax.spark:spark-cassandra-connector_2.12:3.0.0  producer.py 
```

# Producer Code breakdown 

Imports necessary modules and libraries, including SparkSession from pyspark.sql, various functions and types from pyspark.sql.functions and pyspark.sql.types, and other standard Python libraries.
Defines variables for Cassandra database details, Kafka server details, and Cassandra database connectivity credentials.
Sets up logging configuration to create log files with a timestamp in a specified directory.
Creates a Spark session with Cassandra configuration.
Defines a function dataFrameFromCassandaDbTable that reads a table from a Cassandra database and returns a Spark DataFrame.
Defines a function sendDataToKafkaTopic that sends data from a DataFrame to a Kafka topic.
Executes the main code block:
Reads data from a Cassandra database table into a DataFrame.
Prints the schema of the DataFrame.
Shows the content of the DataFrame.
Retrieves the count and columns of the DataFrame and logs the information.
If there are rows in the DataFrame, it calls the sendDataToKafkaTopic function to send the DataFrame data to a Kafka topic.

## To launch consumer script

```
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 consumer.py 
```
# Consumer code breakdown 

The PROCESSING_INTERVAL variable is declared, specifying the interval at which the streaming data will be processed.
A schema is defined using the StructType and StructField classes to define the structure of the DataFrame that will be created from the JSON data received from Kafka.
The dataSink variable is set to the directory where the processed data will be written as Parquet files.
The processEachInterval function is defined, which is a callback function that will be executed for each interval of processed data. It converts the binary value received from Kafka to JSON, applies the defined schema to extract the structured data, and writes it to the dataSink as Parquet files.
The main code block starts by reading the streaming data from Kafka using readStream and the specified options.
The schema of the DataFrame is printed using printSchema().
A streaming query is created using writeStream. It triggers the processing of data at the specified PROCESSING_INTERVAL and calls the processEachInterval function for each batch of processed data.
The streaming query is started using start().
The query awaits termination using awaitTermination().
This code sets up a streaming pipeline that reads data from Kafka, applies schema-based processing, and writes the processed data to Parquet files in a streaming fashion.
