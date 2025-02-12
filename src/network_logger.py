import docker
import pyshark
import logging
import time
import os
import json
import subprocess
from threading import Thread
from logging.handlers import RotatingFileHandler
from prometheus_client import start_http_server, Counter, Gauge

log_file_path = "/logs/docker_network_logs.json"
max_log_size = 1 * 1024 * 1024 * 1024  # 1GB
blacklist_source_ips = os.getenv("BLACKLIST_SOURCE_IPS", "").split(",")
blacklist_destination_ips = os.getenv("BLACKLIST_DESTINATION_IPS", "").split(",")

# Prometheus metrics
packet_count = Counter('network_logger_packets_total', 'Total number of captured packets', ['protocol'])
bandwidth_usage = Counter('network_logger_bandwidth_bytes', 'Total network bandwidth usage in bytes', ['ip'])
avg_packet_size = Gauge('network_logger_avg_packet_size', 'Average packet size per IP', ['ip'])

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(log_file_path, maxBytes=max_log_size, backupCount=1),
        logging.StreamHandler()
    ]
)

docker_client = docker.from_env()

def get_active_network_interfaces():
    interfaces = []
    try:
        output = subprocess.run(["ip", "-j", "link", "show"], capture_output=True, text=True, check=True).stdout
        data = json.loads(output)
        for entry in data:
            iface = entry["ifname"]
            if iface.startswith("br-") or iface.startswith("docker") or iface.startswith("eth") or iface.startswith("ens") or iface.startswith("bond"):
                interfaces.append(iface)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error getting interfaces: {e.stderr}")
    except FileNotFoundError:
        logging.error("The 'ip' command is missing. Ensure iproute2 is installed.")
    except Exception as e:
        logging.error(f"Unexpected error getting interfaces: {e}")
    return interfaces

def capture_network_traffic(interface):
    logging.info(f"Starting capture on interface: {interface}")
    packet_sizes = {}
    packet_counts = {}
    try:
        capture = pyshark.LiveCapture(interface=interface, display_filter="ip")
        for packet in capture.sniff_continuously():
            if hasattr(packet, 'ip'):
                source_ip = getattr(packet.ip, 'src', 'Unknown')
                destination_ip = getattr(packet.ip, 'dst', 'Unknown')
                packet_size = int(getattr(packet, 'length', '0'))

                if source_ip in blacklist_source_ips or destination_ip in blacklist_destination_ips:
                    continue
                
                protocol = getattr(packet, 'highest_layer', 'Unknown')
                log_entry = {
                    "timestamp": time.time(),
                    "source_ip": source_ip,
                    "destination_ip": destination_ip,
                    "protocol": protocol,
                    "length": packet_size
                }
                logging.info(json.dumps(log_entry))
                packet_count.labels(protocol=protocol).inc()
                bandwidth_usage.labels(ip=source_ip).inc(packet_size)
                bandwidth_usage.labels(ip=destination_ip).inc(packet_size)

                # Track average packet size per IP
                if source_ip not in packet_sizes:
                    packet_sizes[source_ip] = 0
                    packet_counts[source_ip] = 0
                packet_sizes[source_ip] += packet_size
                packet_counts[source_ip] += 1
                avg_packet_size.labels(ip=source_ip).set(packet_sizes[source_ip] / packet_counts[source_ip])
    except pyshark.capture.capture.TSharkCrashException as e:
        logging.error(f"TShark crashed on {interface}: {str(e)}")
    except Exception as e:
        logging.error(f"Error capturing on {interface}: {str(e)}")

def monitor_docker_networks():
    active_threads = {}
    while True:
        interfaces = get_active_network_interfaces()
        if not interfaces:
            logging.warning("No active Docker network interfaces found. Retrying in 10 seconds...")
            time.sleep(10)
            continue
    
        for iface in interfaces:
            if iface not in active_threads:
                thread = Thread(target=capture_network_traffic, args=(iface,), daemon=True)
                thread.start()
                active_threads[iface] = thread
    
        time.sleep(10)

if __name__ == "__main__":
    start_http_server(8000, addr="0.0.0.0")  # Allow external access to metrics
    logging.info("Starting Docker Network Logger...")
    monitor_docker_networks()
