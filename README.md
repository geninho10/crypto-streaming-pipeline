#  Crypto-Streaming-Pipeline (BTC/USD)

Dieses Projekt realisiert eine hochperformante End-to-End Dateninfrastruktur zur Echtzeit-Verarbeitung und Analyse von ca. **7,45 Millionen** Bitcoin-Handelsdaten. Das System transformiert statische CSV-Daten mittels **Re-Timestamping** in einen dynamischen Live-Datenstrom und ermöglicht eine latenzarme Zeitreihen-Analyse.

##  Architektur & Highlights

Das System ist als Microservice-Architektur konzipiert und wird vollständig über **Docker Compose (Infrastructure as Code)** orchestriert.

* **Ingestion-Rate:** Kalibriert auf **100 Hz** (entspricht einer 6.000-fachen Beschleunigung der Realzeit).
* **Re-Timestamping:** Transformation historischer Daten (2012–2024) in aktuelle Systemzeit für echtes Live-Monitoring.
* **Stateful Stream Processing:** Berechnung eines **Moving Average (SMA 100)** und Echtzeit-**Anomalie-Erkennung** (>2% Abweichung) direkt im Arbeitsspeicher.
* **Performance:** Bewältigt Lastspitzen von bis zu **25.000 Datenpunkten/Sekunde** (Stresstest-erprobt).
* **I/O-Optimierung:** Reduzierter Overhead durch Meilenstein-Ausgaben (Logging alle 10.000 Punkte).

### Pipeline-Komponenten
1.  **Producer (Python):** Stream-Ingestion mit Taktsteuerung und Zeit-Transformation.
2.  **Message Broker (Apache Kafka):** Hochverfügbare Entkopplungsschicht und Datenpuffer.
3.  **Processor (Python):** Stateful Processing zur Berechnung von Trends und Alerts.
4.  **Consumer (Python):** Effiziente Persistierung der angereicherten Daten.
5.  **Datenbank (InfluxDB):** Time-Series Database für Hochfrequenz-Datenströme.

##  Tech Stack
* **Infrastruktur:** Docker, Docker Compose
* **Streaming:** Apache Kafka, Zookeeper
* **Datenbank:** InfluxDB 2.7
* **Sprache:** Python 3.9
* **Libraries:** `kafka-python`, `influxdb-client`, `pandas`

##  Datensatz
Verwendet wird der Bitstamp Historical BTC/USD Datensatz (1-min Intervall).
* **Umfang:** ~7,45 Millionen Datenpunkte.
* **Quelle:** [Kaggle - Bitcoin Historical Data](https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data)
* **Installation:** Die Datei `btcusd_1-min_data.csv` muss manuell im Hauptverzeichnis abgelegt werden (in der `.gitignore` aufgrund der Dateigröße ausgeschlossen).

##  Setup & Start

Das System ist "Ready-to-run" vorkonfiguriert (Initial-Tokens und Logins sind bereits in der `docker-compose.yml` hinterlegt).

### 1. Infrastruktur starten
```bash
docker-compose up -d

### 2. Pipeline aktivieren

Führen Sie die Skripte in separaten Terminals aus, um den Datenfluss zu starten:

# Terminal 1: Analyse-Logik
python processor.py

# Terminal 2: Datenbank-Persistierung
python consumer.py

# Terminal 3: Daten-Einspeisung (100 Hz)
python producer.py

Visualisierung & Monitoring
Das integrierte InfluxDB-Dashboard visualisiert den Rohpreis, den gleitenden Durchschnitt (SMA) und die identifizierten Anomalien in Echtzeit.

URL: http://localhost:8086

Login: admin / password12345

Organisation: crypto-org

Bucket: bitcoin-bucket

Token: my-super-crypto-token-2026 (bereits vorkonfiguriert)

Dashboard-Konfiguration:

Loggen Sie sich im InfluxDB-UI ein.

Navigieren Sie zum Data Explorer.

Wählen Sie den Bucket bitcoin-bucket.

Filtern Sie nach Measurement bitcoin_price und den Feldern price, sma und is_anomaly.

Klicken Sie auf Submit, um den Kursverlauf und die Alerts zu visualisieren.
