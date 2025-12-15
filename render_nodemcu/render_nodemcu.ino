#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h>

const char* ssid = "EdNet";
const char* password = "Huawei@123";

const char* serverURL = "https://local-server-st9q.onrender.com/status";

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  pinMode(LED_BUILTIN,OUTPUT);
}

void loop() {
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
}
