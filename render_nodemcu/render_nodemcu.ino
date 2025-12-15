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
  server.handleClient();
}
