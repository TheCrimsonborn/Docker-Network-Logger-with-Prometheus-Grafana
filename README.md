# Docker Network Monitor

## 📌 Overview
This project is a **containerized network monitoring and logging solution** that tracks **network traffic, bandwidth usage, and protocol analysis** using **Python, Prometheus, and Grafana**.

### **✨ Features**
- 🚀 **Real-time network packet monitoring**
- 📊 **Grafana dashboards for visualization**
- 📡 **Prometheus integration for metric collection**
- 📡 **Bandwidth usage & packet size monitoring**
- 🔥 **Blacklist support for filtering specific IPs**
- 🔄 **Automatic log rotation (1GB max)**

---

## 📂 **Project Structure**
```
📁 docker-network-monitor
│── 📂 src
│   ├── network_logger.py         # Python app for network monitoring
│   ├── requirements.txt          # Dependencies
│── 📂 logs
│── Dockerfile                    # Docker build configuration
│── docker-compose.yml            # Docker Compose setup
├── grafana-dashboard.json        # Grafana dashboard config
├── prometheus.yml                # Prometheus scrape config
│── README.md                     # Project Documentation
```

---

## 🚀 **Setup & Installation**
### **1️⃣ Prerequisites**
Make sure you have:
- **Docker** installed → [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** installed → [Install Compose](https://docs.docker.com/compose/install/)

### **2️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/docker-network-monitor.git
cd docker-network-monitor
```

### **3️⃣ Build & Run Containers**
```bash
docker compose up --build -d
```
- `-d` runs in **detached mode**
- **Containers started:**
  - `network-logger`: Captures network traffic
  - `prometheus`: Collects and stores network metrics
  - `grafana`: Displays network dashboards

### **4️⃣ Access Services**
- **Prometheus:** [`http://localhost:9090`](http://localhost:9090)
- **Grafana:** [`http://localhost:3000`](http://localhost:3000) *(Login: `admin/admin`)*
- **Network Logger Metrics:** [`http://localhost:8000/metrics`](http://localhost:8000/metrics)

---

## 📊 **Grafana Dashboard**
To import the **Grafana Dashboard**:
1. Open Grafana → Dashboards → **Import**
2. Upload **`grafana/grafana-dashboard.json`**
3. Set **Prometheus** as the data source
4. Click **Import** ✅

---

## 🔥 **Custom Configurations**
### **Blacklist IPs** (Edit `docker-compose.yml`)
```yaml
env:
  BLACKLIST_SOURCE_IPS: "10.10.20.33,192.168.1.100"
  BLACKLIST_DESTINATION_IPS: "172.19.0.5,34.120.177.193"
```
Restart to apply:
```bash
docker compose down
docker compose up -d
```

### **Log Rotation (Max 1GB)**
The script will automatically **reset logs** when `docker_network_logs.json` reaches **1GB**.

---

## 🛠 **Troubleshooting**
### **🔹 No Network Logs?**
Check logs:
```bash
docker logs network-logger -f
```
Make sure you run Docker with **network monitoring permissions**:
```bash
sudo setcap cap_net_raw,cap_net_admin=eip $(which dumpcap)
```

### **🔹 Grafana Not Showing Data?**
Check Prometheus logs:
```bash
docker logs prometheus -f
```
Verify that `http://localhost:8000/metrics` is accessible.

---

## 🚀 **Contributing**
Want to contribute? Open a pull request or submit an issue! 🚀

---

## 📜 **License**
MIT License. Free to use and modify!

---

## ⭐ **Like This Project?**
Give it a **star** ⭐ on GitHub to support development! 🙌

