#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

// Replace with your Wi-Fi credentials
const char* ssid = "EdNet";
const char* password = "Huawei@123";

ESP8266WebServer server(80);  // HTTP server on port 80
     // GPIO pin connected to relay

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH); // Lamp off initially

  WiFi.begin(ssid, password);
  Serial.println("Connecting to Wi-Fi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected. IP address: ");
  Serial.println(WiFi.localIP());

  // Define endpoints
  server.on("/lamp/on", [](){
    digitalWrite(LED_BUILTIN, LOW);  // Turn on lamp
    server.send(200, "text/plain", "Lamp is ON");
  });

  server.on("/lamp/off", [](){
    digitalWrite(LED_BUILTIN, HIGH);   // Turn off lamp
    server.send(200, "text/plain", "Lamp is OFF");
  });

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
<<<<<<< HEAD
  server.handleClient();
=======
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClientSecure client;
    client.setTimeout(15000); 
    
    HTTPClient http;
    
    Serial.println("Attempting to connect to: " + String(serverURL));
    
    if (http.begin(client, serverURL)) {
      Serial.println("HTTP begin successful");
      
      http.setTimeout(15000); 
      int httpCode = http.GET();
      
      Serial.print("HTTP Code: ");
      Serial.println(httpCode);
      
      if (httpCode > 0) { 
        if (httpCode == HTTP_CODE_OK) {
          String payload = http.getString();
          Serial.println("Lamp State: " + payload);
          if (payload=="ON"){
            digitalWrite(LED_BUILTIN,0);
          }
          else
          digitalWrite(LED_BUILTIN,1);
        } else {
          Serial.println("HTTP Code: " + String(httpCode));
        }
      } else {
        Serial.println("Error in HTTP request");
        Serial.println("Error: " + http.errorToString(httpCode));
      }
      http.end();
    } else {
      Serial.println("HTTP begin failed");
    }
  } else {
    Serial.println("WiFi Disconnected");
  }

  delay(5000); 
>>>>>>> a77b0581eca16979c92912bfa7812fe8df71c1c6
}
