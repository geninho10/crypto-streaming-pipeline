import pandas as pd
import json
import time
from kafka import KafkaProducer

# --- KONFIGURATION ---
FILE_NAME = "btcusd_1-min_data.csv" 
TOPIC_NAME = "crypto-prices"

# 1. Kafka Producer Initialisierung
try:
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    print("✅ Verbindung zu Apache Kafka erfolgreich hergestellt.")
except Exception as e:
    print(f"❌ Kritischer Kafka-Fehler: {e}")
    exit()

def stream_data():
    """
    Liest historische Daten aus einer CSV und simuliert einen Echtzeit-Stream
    via Kafka. Nutzt Chunking zur Optimierung des Arbeitsspeichers.
    """
    print(f"📂 Datei {FILE_NAME} wird geladen. Initialisiere Simulation...")
    
    try:
        # Effizientes Einlesen großer Datensätze in Chunks (1000 Zeilen pro Schritt)
        for chunk in pd.read_csv(FILE_NAME, chunksize=1000):
            for index, row in chunk.iterrows():
                # Transformation der Zeile in ein Dictionary (JSON-kompatibel)
                message = row.to_dict()
                
                # Senden der Nachricht an den Kafka-Broker
                producer.send(TOPIC_NAME, value=message)
                
                # Status-Monitoring und Drosselung alle 1000 Datensätze
                if index % 1000 == 0:
                    print(f"🚀 Status: {index} Datenpunkte erfolgreich übertragen.")
                    # Kurze Latenz zur Steuerung der CPU-Last
                    time.sleep(0.01) 
            
            # Stellt sicher, dass alle Nachrichten gesendet wurden
            producer.flush()
                    
    except FileNotFoundError:
        print(f"❌ Fehler: Die Quelldatei '{FILE_NAME}' wurde nicht im Verzeichnis gefunden.")
    except Exception as e:
        print(f"❌ Unvorhergesehener Fehler beim Streaming: {e}")

if __name__ == "__main__":
    stream_data()
