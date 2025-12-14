from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

device_state = {
    "led": "OFF"
}

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>NodeMCU Dashboard</title>
    <style>
        body { font-family: Arial; text-align: center; margin-top: 50px; }
        button { font-size: 20px; padding: 10px 20px; margin: 10px; }
        .on { background: green; color: white; }
        .off { background: red; color: white; }
    </style>
</head>
<body>
    <h1>IoT Dashboard</h1>
    <h2>LED State: {{ led }}</h2>

    <form action="/set/ON" method="post">
        <button class="on">TURN ON</button>
    </form>

    <form action="/set/OFF" method="post">
        <button class="off">TURN OFF</button>
    </form>
</body>
</html>
"""

@app.route("/")
def home():
    return "IoT Server Running"

@app.route("/dashboard")
def dashboard():
    return render_template_string(HTML_PAGE, led=device_state["led"])

@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(device_state)

@app.route("/set/<value>", methods=["POST"])
def set_led(value):
    if value in ["ON", "OFF"]:
        device_state["led"] = value
    return dashboard()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
