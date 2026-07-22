import argparse
import socket
import threading
import time

from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP

from flow_generator import update_flow, pop_expired_flows
from feature_extraction import extract_features
from models.predictor import predict
print("CAPTURE FILE LOADED")
# ----------------------------
# DNS cache (avoid blocking lookup on every packet)
# ----------------------------
_dns_cache = {}


def resolve_hostname(ip):
    if ip in _dns_cache:
        return _dns_cache[ip]
    try:
        name = socket.gethostbyaddr(ip)[0]
    except Exception:
        name = "Unknown"
    _dns_cache[ip] = name
    return name


def report_flow(flow):
    """
    Run feature extraction + prediction on a COMPLETED flow,
    then print the result. Wrapped in try/except so one bad
    flow can't crash the whole capture.
    """
    try:
        features = extract_features(flow)
        result = predict(features)
    except Exception as e:
        print(f"[!] Error during feature extraction / prediction: {e}")
        return

    src = flow["src"]
    dst = flow["dst"]
    sport = flow["sport"]
    dport = flow["dport"]

    src_name = resolve_hostname(src)
    dst_name = resolve_hostname(dst)

    if flow["protocol"] == 6:
        proto = "TCP"
    elif flow["protocol"] == 17:
        proto = "UDP"
    else:
        proto = str(flow["protocol"])

    print("\n" + "=" * 70)
    print("AI NETWORK INTRUSION DETECTION SYSTEM")
    print("=" * 70)

    print("Source IP       :", src)
    print("Destination IP  :", dst)

    print("Protocol        :", proto)

    print("Source Port     :", sport)
    print("Destination Port:", dport)

    print("Source Host     :", src_name)
    print("Destination Host:", dst_name)

    print("-" * 70)

    print("Prediction      :", result["attack"])
    print("Confidence      :", result["confidence"], "%")
    print("Risk Level      :", result["risk"])

    print("=" * 70)

def process_packet(packet):

    if IP not in packet:
        return

    try:
        flow, is_complete = update_flow(packet)

    except Exception as e:
        print("[!] Flow error:", e)
        return

    if flow is None:
        return

    print("\nSending flow to AI model...")

    report_flow(flow)
    print("AI PREDICTION STARTED")

def sweep_expired_flows(interval=5, timeout=30):
    """
    Background thread: periodically force-close flows that have
    gone idle too long (handles UDP and dropped TCP connections
    that never send FIN/RST), then reports them.
    """
    while True:
        time.sleep(interval)
        try:
            expired = pop_expired_flows(timeout=timeout)
            for flow in expired:
                report_flow(flow)
        except Exception as e:
            print(f"[!] Error sweeping expired flows: {e}")


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--interface", default=None)
    parser.add_argument("-f", "--filter", default=None)
    parser.add_argument("--idle-timeout", type=int, default=30,
                        help="Seconds of inactivity before a flow is force-closed")
    parser.add_argument("--sweep-interval", type=int, default=5,
                        help="How often (seconds) to check for idle flows")

    args = parser.parse_args()

    # Start background sweeper so UDP / non-terminated TCP flows
    # still eventually get predicted on, instead of sitting forever.
    sweeper = threading.Thread(
        target=sweep_expired_flows,
        kwargs={"interval": args.sweep_interval, "timeout": args.idle_timeout},
        daemon=True,
    )
    sweeper.start()

    print("\nListening for packets...\n")

    sniff(
        iface=args.interface,
        filter=args.filter,
        prn=process_packet,
        store=False
    )


if __name__ == "__main__":
    main()
