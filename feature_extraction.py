def extract_features(flow):
    """
    Extract the same 10 features used to train the ML model.

    IMPORTANT: this must be called ONLY on a completed flow
    (is_complete == True from update_flow / pop_expired_flows),
    never on an in-progress flow. Calling it mid-flow will give
    unstable duration/rate values that don't match training data.
    """

    duration = flow["last_seen"] - flow["start_time"]

    if duration <= 0:
        duration = 0.001

    total_packets = flow["fwd_packets"] + flow["bwd_packets"]
    total_bytes = flow["fwd_bytes"] + flow["bwd_bytes"]

    flow_bytes_per_sec = total_bytes / duration
    flow_packets_per_sec = total_packets / duration

    features = [

        flow["protocol"],             # Protocol

        duration,                     # Flow Duration

        flow["fwd_packets"],          # Total Forward Packets

        flow["bwd_packets"],          # Total Backward Packets (now real)

        flow["fwd_bytes"],            # Total Forward Bytes

        flow_bytes_per_sec,           # Flow Bytes/s

        flow_packets_per_sec,         # Flow Packets/s

        flow["syn"],                  # SYN Flag Count

        flow["ack"],                  # ACK Flag Count

        flow["init_win_bytes"],       # Init Fwd Win Bytes (now real, from SYN)
    ]

    return features