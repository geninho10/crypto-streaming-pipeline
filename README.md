# Crypto-Streaming-Pipeline (BTC/USD)

Dieses Projekt realisiert eine containerisierte Data-Pipeline zur Verarbeitung und Visualisierung von ca. 7,45 Millionen historischen Bitcoin-Handelsdaten (Zeitraum 2012–2024). Das System transformiert statische CSV-Daten in einen kontinuierlichen Datenstrom und ermöglicht eine hocheffiziente Zeitreihen-Analyse.

## 🏗 Architektur

Das System basiert auf einer Microservice-Architektur, die mittels **Docker Compose** orchestriert wird:

1. **Producer (Python):** Liest Rohdaten aus einer CSV-Datei, transformiert diese in JSON und sendet sie an den Kafka-Broker.
2. **Message Broker (Apache Kafka & Zookeeper):** Dient als Puffer und Entkopplungsschicht zwischen Ingestion und Speicherung.
3. **Consumer (Python):** Abonniert das Kafka-Topic, validiert die Daten und persistiert sie in der Datenbank.
4. **Datenbank (InfluxDB):** Spezialisierte Time-Series Database zur Speicherung und Aggregation der Millionen Datenpunkte.
5. **Visualisierung:** Integriertes InfluxDB-Dashboard zur Analyse der Kursverläufe mittels Flux-Queries.



## 🛠 Tech Stack

* **Infrastruktur:** Docker, Docker Compose
* **Streaming:** Apache Kafka, Zookeeper
* **Datenbank:** InfluxDB 2.x
* **Sprache:** Python 3.9
* **Libraries:** `kafka-python`, `influxdb-client`, `pandas`

## 📊 Datensatz

Der zugrunde liegende Datensatz umfasst ca. 7,45 Millionen Datenpunkte im 1-Minuten-Intervall.
* **Quelle:** Bitstamp (Historical BTC/USD Data)
* **Download:** [Bitcoin Historical Data auf Kaggle](https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data) 
* **Hinweis:** Aufgrund der Dateigröße ist die Datei `btcusd_1-min_data.csv` nicht im Repository enthalten. Für eine lokale Ausführung muss die CSV-Datei im Hauptverzeichnis des Projekts abgelegt werden.

## 🚀 Setup & Start

### Voraussetzungen
* Docker & Docker Desktop installiert
* Python 3.9+ (lokal für die Skript-Ausführung)

### Ausführung der Pipeline
Führen Sie zuerst Schritt 1 aus, um die Container zu starten. Sobald diese laufen, führen Sie Schritt 2 in separaten Terminal-Fenstern aus:

```bash
# --- SCHRITT 1: Infrastruktur starten ---
docker-compose up -d

# --- SCHRITT 2: Skripte aktivieren ---
# Terminal A: Consumer starten
python consumer.py

# Terminal B: Producer starten
python producer.py```

## 📈 Visualisierung & Ergebnisse

Nachdem die Pipeline gestartet wurde, können die Daten über das InfluxDB-Webinterface visualisiert werden.

* **URL:** [http://localhost:8086](http://localhost:8086)
* **Login:** `admin` / `password12345` 
* **Organisation:** `crypto-org`
* **Bucket:** `bitcoin-bucket`

### Schritte zur Ansicht:
1. Navigieren Sie im Menü links zum **Data Explorer** (Graph-Icon).
2. Wählen Sie unter **Buckets** den `bitcoin-bucket`.
3. Wählen Sie unter **Filter** das Measurement `bitcoin_price` und das Feld `price`.
4. Klicken Sie auf **Submit**, um den Graphen anzuzeigen.






