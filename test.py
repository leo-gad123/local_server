import os
from flask import Flask, request, render_template_string
import db
import html_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string(
        html_template.html_template,
        state=db.get_state()
    )

@app.route("/set")
def set_lamp():
    state = request.args.get("state")
    if state in ["ON", "OFF"]:
        db.set_state(state)

    return render_template_string(
        html_template.html_template,
        state=db.get_state()
    )

@app.route("/status")
def status():
    return db.get_state()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
