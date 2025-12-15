💡 Smart Lamp Control (IoT)

A simple IoT lamp control system using Flask, SQLite, and NodeMCU (ESP8266).
The lamp can be turned ON/OFF from a web page, and the state is stored permanently in a database and fetched by NodeMCU.

🚀 Features

Web-based ON/OFF control

Permanent state storage (SQLite)

NodeMCU fetches lamp state via HTTP/HTTPS

Animated UI (no JavaScript)

Modular Flask design

🗂️ Project Structure
app.py
db.py
html_template.py
init_db.py
lamp.db
static/
README.md

▶️ How to Run
pip install flask
python init_db.py
python app.py


Open:

http://localhost:5000

🌐 API

/ → Web UI

/set?state=ON|OFF → Change lamp state

/status → Returns ON or OFF

📡 NodeMCU

NodeMCU polls /status and controls a relay or built-in LED.

☁️ Hosting

✔ Render / PythonAnywhere
❌ Netlify / Vercel (SQLite not persistent)

👨‍💻 Author

Leo Gad – Embedded & IoT Developer
