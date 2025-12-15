import os
from flask import Flask, request, render_template_string, jsonify
import db
import html_template

app = Flask(__name__)


sensor_data = {
    "temperature": "--",
    "humidity": "--"
}


@app.route("/")
def home():
    return render_template_string(
        html_template.html_template,
        state=db.get_state(),
        temperature=sensor_data["temperature"],
        humidity=sensor_data["humidity"]
    )

# ================= LAMP CONTROL =================
@app.route("/set")
def set_lamp():
    state = request.args.get("state")
    if state in ["ON", "OFF"]:
        db.set_state(state)

    return render_template_string(
        html_template.html_template,
        state=db.get_state(),
        temperature=sensor_data["temperature"],
        humidity=sensor_data["humidity"]
    )


@app.route("/status")
def status():
    return db.get_state()

@app.route("/update", methods=["POST"])
def update_dht():
    data = request.get_json()

    if data:
        sensor_data["temperature"] = data.get("temperature", "--")
        sensor_data["humidity"] = data.get("humidity", "--")

    return jsonify({"status": "success"})

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
