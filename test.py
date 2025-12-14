import os
from flask import Flask, render_template_string, request
from datetime import datetime

app = Flask(__name__)

# Data storage
current_data = {
    "lamp": "off",
    "brightness": 0,
    "last_update": None
}

data_history = []
MAX_HISTORY = 20  # Keep last 20 readings

html_template = '''
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

            .no-data {
                text-align: center;
                padding: 40px;
                color: #666;
                font-style: italic;
            }
        </style>
        <script>
            setTimeout(function(){
                location.reload();
            }, 5000);
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
                {% if data_history %}
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
                {% else %}
                <div class="no-data">
                    <i class="fas fa-inbox" style="font-size: 3em; margin-bottom: 10px; display: block; color: #ccc;"></i>
                    No data received yet. Waiting for ESP8266 to send data...
                </div>
                {% endif %}
            </div>
        </div>
    </body>
    </html>
'''

@app.route("/")
def index():
    return render_template_string(
        html_template, 
        current_data=current_data,
        data_history=data_history
    )

@app.route("/update")
def update_data():
    """
    ESP8266 sends data here
    Example: /update?lamp=on&brightness=75
    """
    global current_data, data_history
    
    lamp = request.args.get("lamp", "").lower()
    brightness = request.args.get("brightness", "0")
    
    # Validate lamp state
    if lamp not in ["on", "off"]:
        return "ERROR: Invalid lamp state. Use 'on' or 'off'", 400
    
    # Validate brightness
    try:
        brightness_val = int(brightness)
        if not 0 <= brightness_val <= 100:
            return "ERROR: Brightness must be between 0 and 100", 400
    except ValueError:
        return "ERROR: Invalid brightness value", 400
    
    # Update current data
    current_data["lamp"] = lamp
    current_data["brightness"] = brightness_val
    current_data["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add to history
    data_history.append({
        "timestamp": current_data["last_update"],
        "data": {
            "lamp": lamp,
            "brightness": brightness_val
        }
    })
    
    # Keep only last MAX_HISTORY items
    if len(data_history) > MAX_HISTORY:
        data_history.pop(0)
    
    return "OK"

@app.route("/status")
def get_status():
    """
    ESP8266 can fetch current status
    Returns: lamp_state,brightness (e.g., "on,75")
    """
    return f"{current_data['lamp']},{current_data['brightness']}"

@app.route("/set")
def set_lamp():
    """
    Manual control endpoint (optional)
    Example: /set?lamp=on&brightness=50
    """
    global current_data, data_history
    
    lamp = request.args.get("lamp", "").lower()
    brightness = request.args.get("brightness")
    
    if lamp in ["on", "off"]:
        current_data["lamp"] = lamp
        current_data["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if brightness:
            try:
                brightness_val = int(brightness)
                if 0 <= brightness_val <= 100:
                    current_data["brightness"] = brightness_val
            except ValueError:
                pass
        
        # Add to history
        data_history.append({
            "timestamp": current_data["last_update"],
            "data": {
                "lamp": current_data["lamp"],
                "brightness": current_data["brightness"]
            }
        })
        
        if len(data_history) > MAX_HISTORY:
            data_history.pop(0)
    
    return render_template_string(
        html_template,
        current_data=current_data,
        data_history=data_history
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
