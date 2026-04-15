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

## 🚀 Setup & Start

### Voraussetzungen
* Docker & Docker Desktop installiert
* Python 3.9+ (optional für lokale Ausführung)

### Schritt 1: Infrastruktur starten
Starten Sie die Container im Detached-Mode:
```bash
docker-compose up -d

