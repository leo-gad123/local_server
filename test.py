# app.py

import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

lamp_state = "OFF"

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Lamp Control</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 60px;
            background: linear-gradient(135deg, #1d2671, #c33764);
            color: white;
        }

        h1 {
            font-size: 40px;
            margin-bottom: 30px;
            animation: fadeIn 1.5s ease-in-out;
        }

        a {
            display: inline-block;
            padding: 18px 40px;
            font-size: 22px;
            margin: 15px;
            text-decoration: none;
            color: white;
            border-radius: 50px;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        }

        a:hover {
            transform: scale(1.08);
            box-shadow: 0 12px 25px rgba(0,0,0,0.4);
        }

        a.on {
            background: linear-gradient(135deg, #00c853, #64dd17);
        }

        a.off {
            background: linear-gradient(135deg, #d50000, #ff5252);
        }

        #status {
            font-size: 26px;
            margin-top: 40px;
            padding: 15px;
            display: inline-block;
            border-radius: 12px;
            background: rgba(255,255,255,0.15);
            animation: pulse 2s infinite;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 rgba(255,255,255,0.2); }
            50% { box-shadow: 0 0 20px rgba(255,255,255,0.6); }
            100% { box-shadow: 0 0 0 rgba(255,255,255,0.2); }
        }
    </style>
</head>
<body>

    <h1>💡 Smart Lamp Control</h1>

    <a href="/set?state=ON" class="on">Turn ON</a>
    <a href="/set?state=OFF" class="off">Turn OFF</a>

    <div id="status">
        Current State: <b>{{state}}</b>
    </div>

</body>
</html>

"""

@app.route("/")
def index():
    return render_template_string(html_template, state=lamp_state)

@app.route("/set")
def set_lamp():
    global lamp_state
    state = request.args.get("state")
    if state in ["ON", "OFF"]:
        lamp_state = state
    return render_template_string(html_template, state=lamp_state)

@app.route("/status")
def get_status():
    # NodeMCU can fetch this to get lamp state
    return lamp_state

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
