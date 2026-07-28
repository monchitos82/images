import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.exceptions import InfluxDBError
import re
import time
import os
import subprocess
import logging


ORG = os.getenv("ORG", "local")
URL = os.getenv("INFLUX_SERVER_URL", "http://host.containers.internal:8086")
USER = os.getenv("INFLUX_USER", "influxadmin")
BUCKET = os.getenv("INFLUX_BUCKET", "local")
TOKEN = os.getenv("INFLUX_TOKEN", "")

write_client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = write_client.write_api(write_options=SYNCHRONOUS)
log = logging.getLogger(__name__)

def measure_ping(dest: str = "127.0.0.1", ttl: int = 60) -> str | None:
    try:
        command = ["ping", "-c", "5", "-t", str(ttl), dest]
        ping = subprocess.run(command, capture_output=True, text=True, check=True)
        value = ping.stdout
    except subprocess.CalledProcessError as e:
        log.error(f"Something is wrong: {e}")
        value = None
    return value


def summarize_ping(output: str):
    summary = {}
    packet_loss_match = re.search(
        r"(\d+) packets transmitted, (\d+) received, (\d+)% packet loss", output
    )
    if packet_loss_match:
        summary["transmitted"] = int(packet_loss_match.group(1))
        summary["received"] = int(packet_loss_match.group(2))
        summary["packet_loss_percentage"] = int(packet_loss_match.group(3))

    rtt_match = re.search(
        r"rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+) ms", output
    )
    if rtt_match:
        summary["rtt_min"] = float(rtt_match.group(1))
        summary["rtt_avg"] = float(rtt_match.group(2))
        summary["rtt_max"] = float(rtt_match.group(3))
        summary["rtt_mdev"] = float(rtt_match.group(4))
    return summary


def emit_points():
    for value in os.getenv("HOSTS", "").split(","):
        if not value:
            continue
        value = value.strip()
        measurement = measure_ping(dest=value)
        if measurement:
            summary = summarize_ping(measurement)
            if summary:
                point = Point("ping").tag("dest", value).field(
                    "results", summary.get("rtt_avg", -1)
                )
                log.debug(f"Writting results: {point}")
                try:
                    write_api.write(bucket=BUCKET, org=ORG, record=point)
                except InfluxDBError as error:
                    log.error(f"Failed to write datapoint: {error}")


if __name__ == "__main__":
    while True:
        emit_points()
        time.sleep(60)
