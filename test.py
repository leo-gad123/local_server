# app.py
import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

lamp_state = "OFF"

html_template =  '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ESP8266 Data Display</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                animation: gradientShift 15s ease infinite;
                background-size: 200% 200%;
            }
            
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            .container {
                max-width: 1000px;
                margin: 0 auto;
            }
            
            h1 {
                text-align: center;
                color: white;
                font-size: 3em;
                margin-bottom: 30px;
                text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
                animation: fadeInDown 0.8s ease;
            }
            
            @keyframes fadeInDown {
                from {
                    opacity: 0;
                    transform: translateY(-30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .card {
                background: rgba(255, 255, 255, 0.95);
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                margin-bottom: 30px;
                backdrop-filter: blur(10px);
                animation: fadeInUp 0.8s ease;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 50px rgba(0,0,0,0.3);
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            h2 {
                color: #667eea;
                margin-bottom: 20px;
                font-size: 1.8em;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .status-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            
            .status-item {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 15px;
                color: white;
                text-align: center;
                animation: pulse 2s ease infinite;
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            .status-item i {
                font-size: 3em;
                margin-bottom: 10px;
                animation: bounce 2s ease infinite;
            }
            
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
            
            .status-item .label {
                font-size: 0.9em;
                opacity: 0.9;
                margin-bottom: 5px;
            }
            
            .status-item .value {
                font-size: 2em;
                font-weight: bold;
            }
            
            .lamp-on {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
            }
            
            .lamp-off {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                overflow: hidden;
                border-radius: 10px;
            }
            
            th, td {
                padding: 15px;
                text-align: left;
            }
            
            th {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                font-weight: 600;
            }
            
            tr {
                transition: all 0.3s ease;
            }
            
            tbody tr:nth-child(even) {
                background-color: #f8f9fa;
            }
            
            tbody tr:hover {
                background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
                transform: scale(1.02);
            }
            
            td i {
                margin-right: 8px;
            }
            
            .badge {
                display: inline-block;
                padding: 5px 15px;
                border-radius: 20px;
                font-weight: bold;
                animation: glow 2s ease infinite;
            }
            
            @keyframes glow {
                0%, 100% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.5); }
                50% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.8); }
            }
            
            .badge-on {
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                color: white;
            }
            
            .badge-off {
                background: linear-gradient(135deg, #636363 0%, #a2ab58 100%);
                color: white;
            }
            
            .loading {
                text-align: center;
                padding: 20px;
            }
            
            .loading i {
                font-size: 3em;
                color: #667eea;
                animation: spin 2s linear infinite;
            }
            
            @keyframes spin {
                100% { transform: rotate(360deg); }
            }
            
            .brightness-bar {
                width: 100%;
                height: 30px;
                background: #e0e0e0;
                border-radius: 15px;
                overflow: hidden;
                margin-top: 10px;
                position: relative;
            }
            
            .brightness-fill {
                height: 100%;
                background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
                border-radius: 15px;
                transition: width 0.5s ease;
                box-shadow: 0 0 20px rgba(245, 87, 108, 0.5);
            }
            
            .brightness-text {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-weight: bold;
                color: white;
                text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
            }
        </style>
        <script>
            setTimeout(function(){
                location.reload();
            }, 2000);
        </script>
    </head>
    <body>
        <div class="container">
            <h1><i class="fas fa-bolt"></i> ESP8266 Data Monitor</h1>
            
            <div class="card">
                <h2><i class="fas fa-gauge-high"></i> Current Status</h2>
                <div class="status-grid">
                    <div class="status-item {{ 'lamp-on' if current_data.lamp == 'on' else 'lamp-off' }}">
                        <i class="fas fa-lightbulb"></i>
                        <div class="label">Lamp Status</div>
                        <div class="value">{{ current_data.lamp|upper }}</div>
                    </div>
                    <div class="status-item">
                        <i class="fas fa-sun"></i>
                        <div class="label">Brightness</div>
                        <div class="value">{{ current_data.brightness }}%</div>
                        <div class="brightness-bar">
                            <div class="brightness-fill" style="width: {{ current_data.brightness }}%"></div>
                            <div class="brightness-text">{{ current_data.brightness }}%</div>
                        </div>
                    </div>
                    <div class="status-item">
                        <i class="fas fa-clock"></i>
                        <div class="label">Last Update</div>
                        <div class="value" style="font-size: 1.2em;">{{ current_data.last_update or 'N/A' }}</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2><i class="fas fa-history"></i> Recent History</h2>
                <table>
                    <thead>
                        <tr>
                            <th><i class="fas fa-calendar"></i> Time</th>
                            <th><i class="fas fa-lightbulb"></i> Lamp</th>
                            <th><i class="fas fa-sliders"></i> Brightness</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in data_history|reverse %}
                        <tr>
                            <td><i class="fas fa-clock"></i> {{ item.timestamp }}</td>
                            <td>
                                <span class="badge {{ 'badge-on' if item.data.lamp == 'on' else 'badge-off' }}">
                                    <i class="fas fa-{{ 'lightbulb' if item.data.lamp == 'on' else 'moon' }}"></i>
                                    {{ item.data.lamp|upper }}
                                </span>
                            </td>
                            <td><i class="fas fa-sun"></i> {{ item.data.brightness }}%</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    '''

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

