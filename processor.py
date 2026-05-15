from kafka import KafkaConsumer, KafkaProducer
import json


consumer = KafkaConsumer(
    'bitcoin-raw', 
    bootstrap_servers='localhost:9092', 
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest' 
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092', 
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

prices = []
window_size = 100
count = 0

print("🧠 Processor läuft: Berechne SMA und Anomalien...")

for message in consumer:
    raw_data = message.value
    current_price = raw_data['price']
    prices.append(current_price)
    
    if len(prices) > window_size:
        prices.pop(0)
    
    avg_price = sum(prices) / len(prices)
    
    
    is_anomaly = 1 if abs(current_price - avg_price) / avg_price > 0.02 else 0
    
    processed_data = {
        'raw_price': current_price,
        'average_price': avg_price,
        'volatility_alert': is_anomaly
    }
    
    producer.send('bitcoin-metrics', processed_data)
    
    count += 1

    if count % 10000 == 0:
        print(f"⚙️  {count} Analysen abgeschlossen. Aktueller Preis: {current_price:.2f}")