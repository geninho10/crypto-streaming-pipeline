# Crypto-Streaming-Pipeline (BTC/USD)

Dieses Projekt realisiert eine containerisierte Data-Pipeline zur Verarbeitung und Visualisierung von ca. 7,45 Millionen historischen Bitcoin-Handelsdaten (Zeitraum 2012–2024).

## 🏗 Architektur
Das System basiert auf einer Microservice-Architektur mit Docker Compose:
1. **Producer:** Sendet Daten an Kafka.
2. **Kafka:** Message Broker.
3. **Consumer:** Schreibt in InfluxDB.
4. **InfluxDB:** Zeitreihen-Datenbank.

## 🚀 Setup & Start

Kopieren Sie die folgenden Befehle nacheinander in Ihr Terminal:

```bash
# SCHRITT 1: Infrastruktur starten
docker-compose up -d

# SCHRITT 2: Pipeline aktivieren
# Starten Sie den Consumer (Terminal 1):
python consumer.py

# Starten Sie den Producer (Terminal 2):
python producer.py
