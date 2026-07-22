from flask import Flask, jsonify
from flask_cors import CORS

from database import Session, AttackLog

app = Flask(__name__)

CORS(app)


@app.route("/")
def home():
    return """
    <h1>AI ML Real-Time NIDS</h1>
    <h2>System Status: 🟢 ONLINE</h2>
    <p>Your AI-based Intrusion Detection System is running successfully.</p>
    """



@app.route("/api/attacks")
def attacks():

    session = Session()

    try:

        rows = session.query(AttackLog).order_by(
            AttackLog.id.desc()
        ).limit(50).all()


        data = []


        for r in rows:

            data.append({

                "time": str(r.time),

                "src_ip": r.src_ip,

                "dst_ip": r.dst_ip,

                "protocol": r.protocol,

                "attack": r.attack,

                "confidence": r.confidence,

                "risk": r.risk

            })


        return jsonify(data)


    finally:

        session.close()



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )