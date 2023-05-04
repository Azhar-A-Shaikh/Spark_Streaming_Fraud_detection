```
CREATE KEYSPACE fraud
	WITH REPLICATION = {
		'class': 'org.apache.cassandra.locator.SimpleStrategy',
		'replication_factor': '3'
	}
	AND DURABLE_WRITES = true;
```

```
CREATE TABLE fraud_detection (
   step INT,
   type TEXT,
   amount FLOAT,
   name_orig TEXT,
   old_balance_org FLOAT,
   new_balance_orig FLOAT,
   name_dest TEXT,
   old_balance_dest FLOAT,
   new_balance_dest FLOAT,
   is_fraud INT,
   is_flagged_fraud INT,
   PRIMARY KEY (name_orig, name_dest)
);
```

## Loading the data from my local file system to the cassandra DB into the table fraud_detection 

### First we do this to load the data into the container after creating a all_data Directory 

command to create a all_data directory 

```
docker exec -it <container_name> mkdir /all_data
```

```
docker cp "C:/Users/Azhar/Desktop/Fraud Detection/fraud_detection.csv" aef154fdf59d342339aebcec16c9d0a48071244a34afaa59948c1e896164fe2d:/all_data/fraud_detection.csv

```

### Use powershell to exec this commands 

```
docker exec -it aef154fdf59d342339aebcec16c9d0a48071244a34afaa59948c1e896164fe2d cqlsh -u cassandra -p cassandra
```

### Use the key space you created and input this command in the powershell 

```
COPY fraud_detection (step, type, amount, name_orig, old_balance_org, new_balance_orig, name_dest, old_balance_dest, new_balance_dest, is_fraud, is_flagged_fraud)
FROM '/all_data/fraud_detection.csv'
WITH DELIMITER=',' AND HEADER=TRUE;

```

### Now the data is loaded into the table

SELECT * FROM fraud_detection LIMIT 10;












