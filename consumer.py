import json
from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# --- KONFIGURATION ---
KAFKA_TOPIC = 'crypto-prices'
INFLUX_URL = "http://localhost:8086"
# Den Token für die Veröffentlichung ggf. kürzen oder als Platzhalter lassen
INFLUX_TOKEN = "dPoPGPY6RNulsnVUURkqWtZK3IqJNSDiUbS8L7QubKs1is-xgBm9_-9aZ5AAkqZ0JLaLj8HgZX3qBLWKFRzbyg=="
INFLUX_ORG = "crypto-org"
INFLUX_BUCKET = "bitcoin-bucket"

# 1. InfluxDB Client Setup
# Verbindung zur Time-Series Datenbank herstellen
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

# 2. Kafka Consumer Setup
# Konfiguration des Kafka-Clients für den Datenempfang
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='crypto-group'
)

print("📥 Consumer aktiv: Verarbeite Datenströme aus Kafka...")

try:
    for message in consumer:
        data = message.value
        
        # Extraktion der Kursdaten (Close) und des Zeitstempels
        raw_price = data.get('Close')
        raw_time = data.get('Timestamp')

        if raw_price is not None and raw_time is not None:
            # Erstellung des InfluxDB Datenpunktes
            point = Point("bitcoin_price") \
                .tag("symbol", "BTC") \
                .field("price", float(raw_price)) \
                .time(int(raw_time), WritePrecision.S)
            
            # Schreiben des Punktes in den definierten Bucket
            write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        
        # Status-Update im Terminal alle 1000 verarbeiteten Datensätze
        if message.offset % 1000 == 0:
            print(f"✅ Fortschritt: {message.offset} Datenpunkte erfolgreich persistiert.")

except Exception as e:
    print(f"❌ Fehler während der Laufzeit: {e}")
finally:
    client.close()
    print("🔌 Verbindung zur InfluxDB getrennt.") 

    
