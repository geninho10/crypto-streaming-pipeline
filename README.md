<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub README Vorschau</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            background-color: #f6f8fa;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        }
        .markdown-body {
            background-color: white;
            padding: 45px;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            max-width: 1012px;
            margin: 20px auto;
            line-height: 1.5;
        }
        .markdown-body h1 {
            font-size: 2em;
            padding-bottom: 0.3em;
            border-bottom: 1px solid #d0d7de;
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
        }
        .markdown-body h2 {
            font-size: 1.5em;
            padding-bottom: 0.3em;
            border-bottom: 1px solid #d0d7de;
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
        }
        .markdown-body h3 {
            font-size: 1.25em;
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
        }
        .markdown-body code-block {
            background-color: #f6f8fa;
            border-radius: 6px;
            padding: 16px;
            display: block;
            font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
            font-size: 85%;
            margin-bottom: 16px;
            white-space: pre;
            overflow-x: auto;
        }
        .markdown-body ul {
            padding-left: 2em;
            margin-bottom: 16px;
            list-style-type: disc;
        }
        .markdown-body ol {
            padding-left: 2em;
            margin-bottom: 16px;
            list-style-type: decimal;
        }
        .markdown-body p {
            margin-bottom: 16px;
        }
        .github-header {
            background-color: #f6f8fa;
            border: 1px solid #d0d7de;
            border-bottom: none;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            padding: 8px 16px;
            max-width: 1012px;
            margin: 40px auto 0;
            display: flex;
            align-items: center;
            font-size: 14px;
            color: #24292f;
        }
    </style>
</head>
<body>

    <div class="github-header">
        <svg class="mr-2" height="16" viewBox="0 0 16 16" width="16"><path d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7a.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"></path></svg>
        <span class="font-semibold">README.md</span>
    </div>

    <div class="markdown-body">
        <h1>Crypto-Streaming-Pipeline (BTC/USD)</h1>
        <p>Dieses Projekt realisiert eine containerisierte Data-Pipeline zur Verarbeitung und Visualisierung von ca. 7,45 Millionen historischen Bitcoin-Handelsdaten (Zeitraum 2012–2024). Das System transformiert statische CSV-Daten in einen kontinuierlichen Datenstrom und ermöglicht eine hocheffiziente Zeitreihen-Analyse.</p>

        <h2>🏗 Architektur</h2>
        <p>Das System basiert auf einer Microservice-Architektur, die mittels <strong>Docker Compose</strong> orchestriert wird:</p>
        <ol>
            <li><strong>Producer (Python):</strong> Liest Rohdaten aus einer CSV-Datei, transformiert diese in JSON und sendet sie an den Kafka-Broker.</li>
            <li><strong>Message Broker (Apache Kafka & Zookeeper):</strong> Dient als Puffer und Entkopplungsschicht zwischen Ingestion und Speicherung.</li>
            <li><strong>Consumer (Python):</strong> Abonniert das Kafka-Topic, validiert die Daten und persistiert sie in der Datenbank.</li>
            <li><strong>Datenbank (InfluxDB):</strong> Spezialisierte Time-Series Database zur Speicherung und Aggregation der Millionen Datenpunkte.</li>
            <li><strong>Visualisierung:</strong> Integriertes InfluxDB-Dashboard zur Analyse der Kursverläufe mittels Flux-Queries.</li>
        </ol>

        <h2>🛠 Tech Stack</h2>
        <ul>
            <li><strong>Infrastruktur:</strong> Docker, Docker Compose</li>
            <li><strong>Streaming:</strong> Apache Kafka, Zookeeper</li>
            <li><strong>Datenbank:</strong> InfluxDB 2.x</li>
            <li><strong>Sprache:</strong> Python 3.9</li>
            <li><strong>Libraries:</strong> <code>kafka-python</code>, <code>influxdb-client</code>, <code>pandas</code></li>
        </ul>

        <h2>🚀 Setup & Start</h2>
        <h3>Voraussetzungen</h3>
        <ul>
            <li>Docker & Docker Desktop installiert</li>
            <li>Python 3.9+ (lokal für die Skript-Ausführung)</li>
        </ul>

        <h3>Schritt 1: Infrastruktur starten</h3>
        <p>Starten Sie die Container im Detached-Mode:</p>
        <code-block>docker-compose up -d</code-block>

        <h3>Schritt 2: Pipeline aktivieren</h3>
        <p>Starten Sie zuerst den Consumer, damit dieser auf Nachrichten wartet, und anschließend den Producer in zwei separaten Terminal-Fenstern:</p>
        <code-block># Terminal 1: Consumer starten
python consumer.py

# Terminal 2: Producer starten
python producer.py</code-block>

        <h2>📈 Besonderheiten & Design-Entscheidungen</h2>
        <p>Im Verlauf der Entwicklung wurde ein strategischer Technologiewechsel vollzogen:</p>
        <ul>
            <li><strong>Effizienz:</strong> Statt Apache Flink wurde ein schlanker Python-Consumer implementiert, um den RAM-Verbrauch in der Docker-Umgebung zu minimieren und eine stabilere Ingestion der 7,45 Mio. Datenpunkte zu gewährleisten.</li>
            <li><strong>Server-side Aggregation:</strong> Die Visualisierung nutzt die Abfragesprache <strong>Flux</strong>, um Daten direkt auf der Datenbankebene zu aggregieren, was die Performance des Dashboards bei großen Zeiträumen massiv verbessert.</li>
        </ul>

        <h2>📄 Datenquelle</h2>
        <p>Die verwendeten Daten basieren auf dem Bitstamp BTC/USD Datensatz (Minute-by-Minute), der die historische Kursentwicklung von 2012 bis 2024 abdeckt.</p>
    </div>

</body>
</html>
