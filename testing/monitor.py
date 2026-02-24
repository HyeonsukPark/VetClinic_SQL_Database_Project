import psutil
import time
import csv
from datetime import datetime

# monitoring script for checking CPU, momery. 

output_file = "system_metrics_100.csv"

print("Starting system monitoring... Press Ctrl+C to stop.")

with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "cpu_percent", "memory_percent"])

    try:
        while True:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            writer.writerow([timestamp, cpu, memory])
            f.flush()

            print(f"{timestamp} | CPU: {cpu}% | Memory: {memory}%")

    except KeyboardInterrupt:
        print("Monitoring stopped.")