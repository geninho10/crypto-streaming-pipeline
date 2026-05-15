from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point, WriteOptions
import json


url = "http://localhost:8086"
token = "my-super-crypto-token-2026"
org = "crypto-org"
bucket = "bitcoin-bucket"

client = InfluxDBClient(url=url, token=token, org=org)

write_api = client.write_api(write_options=WriteOptions(
    batch_size=1000,       
    flush_interval=5000,   
    retry_interval=2000
))

consumer = KafkaConsumer(
    'bitcoin-metrics',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest'
) 

print("🚀 Consumer gestartet und bereit zum Schreiben in InfluxDB...")

total_count = 0 

try:
    for message in consumer:
        data = message.value
        
        point = Point("bitcoin_price") \
            .field("price", data['raw_price']) \
            .field("average", data['average_price']) \
            .field("anomaly", int(data['volatility_alert']))
        
        write_api.write(bucket=bucket, org=org, record=point)
        
        total_count += 1
        if total_count % 10000 == 0:
            print(f"✅ Meilenstein: {total_count} Punkte gespeichert.")

except Exception as e:
    print(f"❌ Fehler im Consumer: {e}")
finally:
    write_api.close()
    client.close()