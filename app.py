from flask import Flask, jsonify
from flask_cors import CORS

from database import Session, AttackLog

app = Flask(__name__)

CORS(app)

@app.route("/api/attacks")
def attacks():

    session = Session()

    rows = session.query(AttackLog).order_by(AttackLog.id.desc()).limit(50)

    data = []

    for r in rows:

        data.append({

            "time": r.time,

            "src_ip": r.src_ip,

            "dst_ip": r.dst_ip,

            "protocol": r.protocol,

            "attack": r.attack,

            "confidence": r.confidence,

            "risk": r.risk

        })

    session.close()

    return jsonify(data)

if __name__ == "__main__":

    app.run(debug=True)