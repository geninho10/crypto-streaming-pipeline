import time
import json
import csv
from kafka import KafkaProducer

# KONFIGURATION
CSV_FILE = 'btcusd_1-min_data.csv' 
TOPIC = 'bitcoin-raw'

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    batch_size=65536, 
    linger_ms=5
)

print(f"🚀 Starte Echtzeit-Streaming von {CSV_FILE}...")

count = 0

try:
    with open(CSV_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        
        possible_columns = ['Weighted_Price', 'price', 'Close', 'close', 'Weighted Price']
        actual_columns = reader.fieldnames
        column_to_use = next((c for c in possible_columns if c in actual_columns), None)

        if not column_to_use:
            print(f"❌ Fehler: Keine Preis-Spalte gefunden! Vorhanden sind: {actual_columns}")
            exit()

        print(f"✅ Nutze Spalte: '{column_to_use}'")

        for row in reader:
            val = row[column_to_use]
            if not val or val.lower() == 'nan':
                continue
                
            try:
                price = float(val)
                data = {
                    'price': price,
                    'timestamp': time.time()
                }
                
                producer.send(TOPIC, data)
                count += 1
                
                
                time.sleep(0.01) 
                # -----------------------------

                if count % 1000 == 0:
                    print(f"📡 Streaming-Status: {count} Punkte gesendet (Echtzeit-Simulation)...")
            except ValueError:
                continue

    print(f"✅ Fertig! Insgesamt {count} Punkte gesendet.")

except FileNotFoundError:
    print(f"❌ Datei '{CSV_FILE}' nicht gefunden!")
except Exception as e:
    print(f"❌ Fehler: {e}")
finally:
    producer.flush()
    producer.close() 