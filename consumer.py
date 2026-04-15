services:
  # --- MESSAGING LAYER ---
  # Zookeeper koordiniert die Kafka-Broker
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    networks:
      - crypto-network

  # Kafka fungiert als zentraler Message Broker für den Datenstrom
  kafka:
    image: confluentinc/cp-kafka:7.5.0
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    depends_on:
      - zookeeper
    networks:
      - crypto-network

  # --- SERVING LAYER ---
  # InfluxDB zur Speicherung und Visualisierung der Time-Series Daten
  influxdb:
    image: influxdb:2.7
    ports:
      - "8086:8086"
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=admin
      - DOCKER_INFLUXDB_INIT_PASSWORD=your_secure_password
      - DOCKER_INFLUXDB_INIT_ORG=crypto-org
      - DOCKER_INFLUXDB_INIT_BUCKET=bitcoin-bucket
      - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=your_secret_admin_token
    networks:
      - crypto-network

networks:
  crypto-network:
    driver: bridge
