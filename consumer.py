from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os
from pyspark.sql import DataFrame
import time
import logging
from datetime import datetime

#Variable declaration

#cassandra database detail
KEYSPACE = "fraud"
TABLE="fraud_detection"

#kafka server detail
KAFKA_BOOTSTRAP_SERVER="kafka:9092"
KAFKA_TOPIC = "fraud"

#Cassandra database connectivity credentails
CASSANDRA_HOST="cassandra"
CASSANDRA_USER="cassandra"
CASSANDRA_PASSWORD="cassandra"

PROCESSING_INTERVAL = f"5 seconds"

#log file name
LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"
#log directory
LOG_FILE_DIR = os.path.join(os.getcwd(),"logs")
#create folder if not available
os.makedirs(LOG_FILE_DIR,exist_ok=True)


logging.basicConfig(
    filename=os.path.join(LOG_FILE_DIR,LOG_FILE_NAME),
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


#create spark session with cassandar configuration
sparkSesison = (SparkSession.builder
                 .config("spark.cassandra.connection.host","cassandra")
                 .config("spark.cassandra.auth.username","cassandra")
                 .config("spark.cassandra.auth.password","cassandra")
                 .appName("demo").getOrCreate()
                 )

schema = StructType([
    StructField(name="step", dataType=IntegerType()),
    StructField(name="type", dataType=StringType()),
    StructField(name="amount", dataType=FloatType()),
    StructField(name="name_orig", dataType=StringType()),
    StructField(name="old_balance_org", dataType=FloatType()),
    StructField(name="new_balance_orig", dataType=FloatType()),
    StructField(name="name_dest", dataType=StringType()),
    StructField(name="old_balance_dest", dataType=FloatType()),
    StructField(name="new_balance_dest", dataType=FloatType()),
    StructField(name="is_fraud", dataType=IntegerType()),
    StructField(name="is_flagged_fraud", dataType=IntegerType())
])


dataSink = os.path.join("fraud_detecion")

def processEachInterval(df:DataFrame,epoch_id):
    # print(epoch_id)
    # df.show(truncate=False)
    df = (df.withColumn("value",
        from_json(decode("value",charset="UTF-8"),schema=schema)
        .alias("value"))
        .select("value.*")
    )
    if df.count()>0:
        df.show(truncate=False)
        df.write.mode("append").parquet(dataSink)


if __name__ == "__main__":
    # Create SparkSession
    spark = SparkSession.builder.appName("Consumer").getOrCreate()

    # Read data from Kafka topic
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER) \
        .option("subscribe", KAFKA_TOPIC) \
        .option("startingOffsets", "earliest") \
        .load()
    
    # Extract required columns from Kafka value
    df = df.selectExpr("CAST(value AS STRING) as raw_value")
    schema = StructType([
        StructField("step", IntegerType()),
        StructField("type", StringType()),
        StructField("amount", DoubleType()),
        StructField("name_orig", StringType()),
        StructField("old_balance_org", DoubleType()),
        StructField("new_balance_orig", DoubleType()),
        StructField("name_dest", StringType()),
        StructField("old_balance_dest", DoubleType()),
        StructField("new_balance_dest", DoubleType()),
        StructField("is_fraud", IntegerType()),
        StructField("is_flagged_fraud", IntegerType())
    ])
    df = df.select(from_json(df.raw_value, schema).alias("data")).select("data.*")

    # Process the data
    query = df.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()
