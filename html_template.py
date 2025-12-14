
# ---------- HTML TEMPLATE ----------
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
<br><br><br>
<h1>&copycopy Leogad Server</h1>
</body>
</html>
"""