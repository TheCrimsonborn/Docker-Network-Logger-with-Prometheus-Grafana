# Docker Network Logger with Prometheus, Grafana, Loki, and Tempo

## 📌 Overview
A fully containerized network monitoring, logging, and tracing solution.  
It captures network traffic, exposes Prometheus metrics, stores logs in Loki, and collects distributed traces with Tempo — all visualized in Grafana.

---

## ✨ Features
- **Real-time** network packet monitoring with Python
- **Prometheus metrics** for network data
- **Grafana dashboards** for metrics, logs, and traces
- **Loki + Promtail** for centralized log aggregation
- **Tempo** for distributed tracing (OTLP HTTP & gRPC)
- Blacklist support to ignore unwanted IPs
- Automatic log rotation when log file exceeds **1GB**

---

## 📂 Project Structure
```
📁 docker-network-monitor
│── 📂 src
│   ├── network_logger.py
│   ├── requirements.txt
│── 📂 logs
│── 📂 configs
│   ├── prometheus.yml
│   ├── loki-config.yml
│   ├── promtail-config.yml
│   ├── tempo-config.yml
│── Dockerfile
│── docker-compose.yml
│── grafana-dashboard.json
│── README.md
```

---

## 🚀 Setup & Installation

### 1️⃣ Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 2️⃣ Clone Repository
```bash
git clone https://github.com/your-username/docker-network-monitor.git
cd docker-network-monitor
```

### 3️⃣ Build & Run
```bash
docker compose up --build -d
```

**Containers started:**
- `network-logger` → Captures network traffic and exposes metrics
- `prometheus` → Collects and stores metrics
- `grafana` → Visualizes metrics, logs, and traces
- `loki` → Stores logs
- `promtail` → Ships logs to Loki
- `tempo` → Stores and queries distributed traces

---

## 🌐 Access Services
- Prometheus → [http://localhost:9090](http://localhost:9090)
- Grafana → [http://localhost:3000](http://localhost:3000) *(admin/admin)*
- Loki API → [http://localhost:3100](http://localhost:3100)
- Tempo API → [http://localhost:3200](http://localhost:3200)
- Network Logger Metrics → [http://localhost:8000/metrics](http://localhost:8000/metrics)

---

## 📊 Grafana Dashboard
1. Go to Grafana → Dashboards → Import
2. Upload `grafana-dashboard.json`
3. Set data sources:
   - Prometheus → `http://prometheus:9090`
   - Loki → `http://loki:3100`
   - Tempo → `http://tempo:3200`
4. Click Import ✅

---

## ⚙️ Custom Configuration

### Blacklist IPs
Edit `docker-compose.yml`:
```yaml
environment:
  BLACKLIST_SOURCE_IPS: "10.10.20.33,192.168.1.100"
  BLACKLIST_DESTINATION_IPS: "172.19.0.5,34.120.177.193"
```
Restart:
```bash
docker compose down && docker compose up -d
```

### Log Rotation
When `docker_network_logs.json` exceeds **1GB**, it resets automatically.

---

## 🛠 Troubleshooting

**No Logs?**
```bash
docker logs promtail -f
```
Ensure `./logs` contains files.

**No Metrics?**
```bash
docker logs prometheus -f
```
Check if `http://localhost:8000/metrics` works.

**No Traces?**
Verify your app sends OTLP data to Tempo on port `4317` (gRPC) or `4318` (HTTP).

---

## 📜 License
GNU GPL v3.0 — see LICENSE for details.
