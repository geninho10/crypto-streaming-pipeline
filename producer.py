import pandas as pd
import json
import time
from kafka import KafkaProducer

# --- KONFIGURATION ---
FILE_NAME = "btcusd_1-min_data.csv" 
TOPIC_NAME = "crypto-prices"

# Kafka Setup
try:
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    print("✅ Verbindung zu Kafka steht!")
except Exception as e:
    print(f"❌ Kafka Fehler: {e}")
    exit()

def stream_data():
    print(f"📂 Lade {FILE_NAME} und starte Simulation...")
    
    try:
        # Wir lesen die 1 Mio.+ Zeilen in 1000er Schritten (Chunks)
        for chunk in pd.read_csv(FILE_NAME, chunksize=1000):
            for index, row in chunk.iterrows():
                # Wir wandeln die Zeile in JSON um
                message = row.to_dict()
                
                # Wir schicken es an das Kafka-Förderband
                producer.send(TOPIC_NAME, value=message)
                
                # Alle 1000 Zeilen ein Update, damit wir sehen, dass es läuft
                if index % 1000 == 0:
                    print(f"🚀 Datenpunkt {index} erfolgreich gestreamt...")
                    # Eine winzige Pause, damit dein Mac nicht glüht
                    time.sleep(0.01) 
                    
    except FileNotFoundError:
        print(f"❌ Fehler: '{FILE_NAME}' nicht gefunden! Liegt die Datei im Ordner?")

if __name__ == "__main__":
    stream_data() 
    