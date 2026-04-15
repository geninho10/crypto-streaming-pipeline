import json
from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# --- KONFIGURATION ---
KAFKA_TOPIC = 'crypto-prices'
INFLUX_URL = "http://localhost:8086"
# Synchronisierter Token aus der docker-compose.yml
INFLUX_TOKEN = "my-super-crypto-token-2026"
INFLUX_ORG = "crypto-org"
INFLUX_BUCKET = "bitcoin-bucket"

# 1. InfluxDB Client Setup
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

# 2. Kafka Consumer Setup
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='crypto-group'
)

print("📥 Consumer aktiv: Warte auf Datenströme aus Kafka...")

try:
    for message in consumer:
        data = message.value
        
        # Extraktion der Daten
        raw_price = data.get('Close')
        raw_time = data.get('Timestamp')

        if raw_price is not None and raw_time is not None:
            # Erstellung des Datenpunktes
            point = Point("bitcoin_price") \
                .tag("symbol", "BTC") \
                .field("price", float(raw_price)) \
                .time(int(raw_time), WritePrecision.S)
            
            # Schreiben in InfluxDB
            write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        
        # Status-Update alle 1000 Zeilen
        if message.offset % 1000 == 0:
            print(f"✅ Fortschritt: {message.offset} Datenpunkte erfolgreich persistiert.")

except Exception as e:
    print(f"❌ Fehler während der Laufzeit: {e}")
finally:
    client.close()
    print("🔌 Verbindung zur InfluxDB getrennt.")
