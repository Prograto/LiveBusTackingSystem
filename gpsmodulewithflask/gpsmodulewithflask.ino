#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <TinyGPSPlus.h>
#include <HardwareSerial.h>

const char* ssid = "PROGRATO";
const char* password = "Chandugad89!";
const char* serverUrl = "https://livebustackingsystem.onrender.com/submit_location";

// GPS setup
HardwareSerial GPS(2);
TinyGPSPlus gps;

// WiFiClientSecure to handle HTTPS
WiFiClientSecure client;

void setup() {
  Serial.begin(115200);
  GPS.begin(9600, SERIAL_8N1, 16, -1); // RX: GPIO16, no TX
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("WiFi connected.");
  
  client.setInsecure(); // Disable SSL certificate verification (use this only for testing)
}

void loop() {
  while (GPS.available()) {
    gps.encode(GPS.read());

    if (gps.location.isUpdated()) {
      float lat = gps.location.lat();
      float lng = gps.location.lng();

      if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(client, serverUrl);  // Use WiFiClientSecure for HTTPS
        http.addHeader("Content-Type", "application/json");

        String payload = "{\"latitude\": " + String(lat, 6) + ", \"longitude\": " + String(lng, 6) + "}";
        int httpResponseCode = http.POST(payload);
        
        Serial.print("Sent GPS data: ");
        Serial.println(payload);
        Serial.print("Server response: ");
        Serial.println(httpResponseCode);
        
        http.end();
      } else {
        Serial.println("WiFi disconnected!");
      }
    }
  }
  delay(2000); 
}
