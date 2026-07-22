import time
from scapy.layers.inet import IP, TCP, UDP

# Stores all active network flows
flows = {}

print("FLOW GENERATOR UPDATED VERSION LOADED")
# How long (seconds) an idle flow waits before being force-closed
# (handles UDP and TCP flows that never send FIN/RST)
FLOW_TIMEOUT = 5


def _get_flow_key(src, dst, sport, dport, protocol):
    """
    Build a DIRECTION-NORMALIZED flow key so that both directions
    of the same conversation (client->server and server->client)
    map to the SAME flow entry.

    Returns (flow_id, direction) where direction is 'fwd' or 'bwd'.
    'fwd' = the direction that started the flow (lower (ip, port) tuple).
    """
    a = (src, sport)
    b = (dst, dport)

    if a <= b:
        flow_id = (src, dst, sport, dport, protocol)
        direction = "fwd"
    else:
        flow_id = (dst, src, dport, sport, protocol)
        direction = "bwd"

    return flow_id, direction


def _new_flow(src, dst, sport, dport, protocol):
    return {
        "src": src,
        "dst": dst,
        "sport": sport,
        "dport": dport,

        "protocol": protocol,

        "start_time": time.time(),
        "last_seen": time.time(),

        # bidirectional counters
        "fwd_packets": 0,
        "bwd_packets": 0,
        "fwd_bytes": 0,
        "bwd_bytes": 0,

        "syn": 0,
        "ack": 0,
        "fin": 0,
        "rst": 0,

        # real TCP window size captured from the first SYN packet
        "init_win_bytes": 0,
    }


def update_flow(packet):
    """
    Update (or create) the flow this packet belongs to.

    Returns (flow, is_complete):
        flow        - the flow dict (current state)
        is_complete - True if this packet closed the flow (FIN/RST seen),
                      meaning it's ready for feature extraction + prediction.
                      False if the flow is still ongoing.
    """

    if IP not in packet:
        return None, False

    src = packet[IP].src
    dst = packet[IP].dst
    protocol = packet[IP].proto

    sport = 0
    dport = 0

    if TCP in packet:
        sport = packet[TCP].sport
        dport = packet[TCP].dport
    elif UDP in packet:
        sport = packet[UDP].sport
        dport = packet[UDP].dport

    flow_id, direction = _get_flow_key(src, dst, sport, dport, protocol)

    if flow_id not in flows:
        flows[flow_id] = _new_flow(src, dst, sport, dport, protocol)

    flow = flows[flow_id]
    flow["last_seen"] = time.time()

    pkt_len = len(packet)

    if direction == "fwd":
        flow["fwd_packets"] += 1
        flow["fwd_bytes"] += pkt_len
    else:
        flow["bwd_packets"] += 1
        flow["bwd_bytes"] += pkt_len

    is_complete = False

    if TCP in packet:
        flags = packet[TCP].flags

        if flags & 0x02:  # SYN
            flow["syn"] += 1
            # capture the real initial window size (only once, on first SYN)
            if flow["init_win_bytes"] == 0:
                flow["init_win_bytes"] = packet[TCP].window

        if flags & 0x10:  # ACK
            flow["ack"] += 1

        if flags & 0x01:  # FIN
            flow["fin"] += 1

        if flags & 0x04:  # RST
            flow["rst"] += 1

        # Close the flow once we see FIN or RST
        if flow["fin"] or flow["rst"]:
            is_complete = True

    if is_complete:
        # Remove from active table; caller is responsible for
        # extracting features / predicting on the returned copy.
        flows.pop(flow_id, None)

    return flow, is_complete


def pop_expired_flows(timeout=FLOW_TIMEOUT):
    """
    Force-close any flow that's been idle too long (handles UDP flows
    and TCP flows that never send FIN/RST, e.g. dropped connections).

    Call this periodically (e.g. every few seconds) from capture.py.
    Returns a list of finished flow dicts ready for prediction.
    """
    now = time.time()
    expired_ids = [
        flow_id for flow_id, flow in flows.items()
        if now - flow["last_seen"] > timeout
    ]

    expired_flows = [flows.pop(flow_id) for flow_id in expired_ids]
    return expired_flows