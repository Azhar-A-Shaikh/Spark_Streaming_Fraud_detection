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

```
COPY fraud_detection (step, type, amount, name_orig, old_balance_org, new_balance_orig, name_dest, old_balance_dest, new_balance_dest, is_fraud, is_flagged_fraud)
FROM 'fraud_detection.csv'
WITH DELIMITER=',' AND HEADER=TRUE;
```

### Now the data is loaded into the table

SELECT * FROM fraud_detection LIMIT 10;














