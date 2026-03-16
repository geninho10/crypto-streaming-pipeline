import json
from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# --- KONFIGURATION ---
KAFKA_TOPIC = 'crypto-prices'
INFLUX_URL = "http://localhost:8086"
# Dein aktueller Token:
INFLUX_TOKEN = "dPoPGPY6RNulsnVUURkqWtZK3IqJNSDiUbS8L7QubKs1is-xgBm9_-9aZ5AAkqZ0JLaLj8HgZX3qBLWKFRzbyg=="
INFLUX_ORG = "crypto-org"  # Diese Zeile hat gefehlt!
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

print("📥 Consumer läuft und saugt Daten aus Kafka...")

try:
    for message in consumer:
        data = message.value
        
        # Wir nehmen 'Close' und 'Timestamp' (deine CSV-Spalten)
        raw_price = data.get('Close')
        raw_time = data.get('Timestamp')

        if raw_price is not None and raw_time is not None:
            point = Point("bitcoin_price") \
                .tag("symbol", "BTC") \
                .field("price", float(raw_price)) \
                .time(int(raw_time), WritePrecision.S)
            
            # Hier nutzen wir jetzt die oben definierte Variable INFLUX_ORG
            write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        
        # Alle 1000 Punkte ein Update im Terminal
        if message.offset % 1000 == 0:
            print(f"✅ Fortschritt: {message.offset} Datenpunkte verarbeitet (Preis: {raw_price})")

except Exception as e:
    print(f"❌ Fehler im Consumer: {e}")
finally:
    client.close() 