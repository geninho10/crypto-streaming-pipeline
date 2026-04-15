Crypto-Streaming-Pipeline (BTC/USD)

Dieses Projekt realisiert eine containerisierte Data-Pipeline zur Verarbeitung und Visualisierung von ca. 7,45 Millionen historischen Bitcoin-Handelsdaten (Zeitraum 2012–2024). Das System transformiert statische CSV-Daten in einen kontinuierlichen Datenstrom und ermöglicht eine hocheffiziente Zeitreihen-Analyse.

🏗 Architektur

Das System basiert auf einer Microservice-Architektur, die mittels Docker Compose orchestriert wird:

Producer (Python): Liest Rohdaten aus einer CSV-Datei, transformiert diese in JSON und sendet sie an den Kafka-Broker.

Message Broker (Apache Kafka & Zookeeper): Dient als Puffer und Entkopplungsschicht zwischen Ingestion und Speicherung.

Consumer (Python): Abonniert das Kafka-Topic, validiert die Daten und persistiert sie in der Datenbank.

Datenbank (InfluxDB): Spezialisierte Time-Series Database zur Speicherung und Aggregation der Millionen Datenpunkte.

Visualisierung: Integriertes InfluxDB-Dashboard zur Analyse der Kursverläufe mittels Flux-Queries.

🛠 Tech Stack

Infrastruktur: Docker, Docker Compose

Streaming: Apache Kafka, Zookeeper

Datenbank: InfluxDB 2.x

Sprache: Python 3.9

Libraries: kafka-python, influxdb-client, pandas

🚀 Setup & Start

Voraussetzungen

Docker & Docker Desktop installiert

Python 3.9+ (lokal für die Skript-Ausführung)

Schritt 1: Infrastruktur starten

Starten Sie die Container im Detached-Mode:

docker-compose up -d


Schritt 2: Pipeline aktivieren

Starten Sie zuerst den Consumer, damit dieser auf Nachrichten wartet, und anschließend den Producer in zwei separaten Terminal-Fenstern:

# Terminal 1: Consumer starten
python consumer.py

# Terminal 2: Producer starten
python producer.py


📈 Besonderheiten & Design-Entscheidungen

Im Verlauf der Entwicklung wurde ein strategischer Technologiewechsel vollzogen:

Effizienz: Statt Apache Flink wurde ein schlanker Python-Consumer implementiert, um den RAM-Verbrauch in der Docker-Umgebung zu minimieren und eine stabilere Ingestion der 7,45 Mio. Datenpunkte zu gewährleisten.

Server-side Aggregation: Die Visualisierung nutzt die Abfragesprache Flux, um Daten direkt auf der Datenbankebene zu aggregieren, was die Performance des Dashboards bei großen Zeiträumen massiv verbessert.

📄 Datenquelle

Die verwendeten Daten basieren auf dem Bitstamp BTC/USD Datensatz (Minute-by-Minute), der die historische Kursentwicklung von 2012 bis 2024 abdeckt.
