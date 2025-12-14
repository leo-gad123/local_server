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
        body { font-family: Arial; text-align: center; margin-top: 50px; }
        a { display: inline-block; padding: 15px 30px; font-size: 20px; margin: 10px; text-decoration: none; background: #4CAF50; color: white; border-radius: 5px; }
        a.off { background: #f44336; }
        #status { font-size: 24px; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>Lamp Control</h1>
    <a href="/set?state=ON">Turn ON</a>
    <a href="/set?state=OFF" class="off">Turn OFF</a>
    <div id="status">Current State: {{state}}</div>
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

