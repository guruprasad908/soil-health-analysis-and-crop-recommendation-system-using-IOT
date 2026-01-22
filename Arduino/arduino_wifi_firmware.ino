#include <Wire.h>
#include <U8g2lib.h>
#include <DHT.h>
#include <WiFiS3.h> // Arduino UNO R4 WiFi Library
#include <ArduinoHttpClient.h> // Library for HTTP requests

// ----- WiFi Credentials -----
const char* ssid = "Sneha";
const char* password = "12345678";

// ----- Server Details -----
const char* serverAddress = "10.120.223.241"; // Your Laptop IP
const int serverPort = 8000;

// ----- OLED (SH1106 I2C) -----
U8G2_SH1106_128X64_NONAME_F_HW_I2C oled(U8G2_R0, U8X8_PIN_NONE);

// ----- DHT22 Sensor -----
#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// ----- Soil Moisture Sensor -----
#define SOIL_PIN A0

// ----- Timers -----
unsigned long lastReadTime = 0;
const unsigned long refreshInterval = 5000; // 5 seconds

// ----- Variables -----
int moisturePercent = 0;
float tempC = 0.0;
float humidity = 0.0;
int status = WL_IDLE_STATUS;

// Initialize WiFi Client
WiFiClient wifi;
HttpClient client = HttpClient(wifi, serverAddress, serverPort);

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(SOIL_PIN, INPUT);

  // Initialize OLED
  oled.begin();
  oled.setFont(u8g2_font_7x14_tf);
  oled.clearBuffer();
  oled.drawStr(15, 30, "SOIL MONITOR");
  oled.drawStr(25, 50, "Initializing...");
  oled.sendBuffer();
  delay(2000);

  // ----- WiFi Connection -----
  oled.clearBuffer();
  oled.drawStr(10, 30, "Connecting to:");
  oled.drawStr(10, 50, ssid);
  oled.sendBuffer();

  // Check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    oled.clearBuffer();
    oled.drawStr(0, 30, "WiFi Module Error!");
    oled.sendBuffer();
    while (true);
  }

  // Attempt to connect to WiFi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    
    status = WiFi.begin(ssid, password);
    
    // Wait 10 seconds for connection:
    delay(10000);
  }

  Serial.println("Connected to WiFi");
  printWifiStatus();

  // Show Connected Status on OLED
  oled.clearBuffer();
  oled.drawStr(10, 20, "WiFi Connected!");
  oled.drawStr(0, 40, "IP Address:");
  
  // Convert IP to string for OLED
  IPAddress ip = WiFi.localIP();
  char ipStr[20];
  sprintf(ipStr, "%d.%d.%d.%d", ip[0], ip[1], ip[2], ip[3]);
  oled.drawStr(0, 60, ipStr);
  oled.sendBuffer();
  
  delay(3000); // Show IP for 3 seconds
}

void loop() {
  if (millis() - lastReadTime >= refreshInterval) {
    lastReadTime = millis();

    // ----- Soil Moisture -----
    int soilValue = analogRead(SOIL_PIN);
    Serial.print("DEBUG: Raw Soil Value: ");
    Serial.println(soilValue);
    
    // Adjusted mapping (Dry=1023, Wet=0 to cover full range)
    moisturePercent = map(soilValue, 1023, 0, 0, 100);
    moisturePercent = constrain(moisturePercent, 0, 100);

    // ----- DHT22 -----
    tempC = dht.readTemperature();
    humidity = dht.readHumidity();

    if (isnan(tempC) || isnan(humidity)) {
      Serial.println("❌ DHT22 Error - Check wiring!");
      return;
    }

    // ----- Serial Output -----
    Serial.print("{\"Soil\":");
    Serial.print(moisturePercent);
    Serial.print(",\"Temp\":");
    Serial.print(tempC, 1);
    Serial.print(",\"Hum\":");
    Serial.print(humidity, 1);
    Serial.println("}");

    // ----- OLED Display -----
    oled.firstPage();
    do {
      // Show WiFi Status Icon (simple 'W' if connected)
      if (WiFi.status() == WL_CONNECTED) {
        oled.drawStr(115, 10, "W");
      } else {
        oled.drawStr(115, 10, "X");
      }

      char soilStr[25];
      sprintf(soilStr, "Soil: %d %%", moisturePercent);
      oled.drawStr(0, 20, soilStr);

      char tempStr[25];
      sprintf(tempStr, "Temp: %.1f C", tempC);
      oled.drawStr(0, 40, tempStr);

      char humStr[25];
      sprintf(humStr, "Hum : %.1f %%", humidity);
      oled.drawStr(0, 60, humStr);
    } while (oled.nextPage());

    // ----- Send Data to Backend -----
    sendDataToBackend(tempC, humidity, moisturePercent);
  }
}

void sendDataToBackend(float temperature, float humidity, int moisture) {
  Serial.println("Sending data to backend...");
  
  String contentType = "application/json";
  String postData = "{\"temperature\": " + String(temperature) + 
                    ", \"humidity\": " + String(humidity) + 
                    ", \"moisture\": " + String(moisture) + 
                    ", \"device_id\": \"ArduinoUNO\"}";

  client.post("/api/sensor/uno-data", contentType, postData);

  // Read the status code and body of the response
  int statusCode = client.responseStatusCode();
  String response = client.responseBody();

  Serial.print("Status code: ");
  Serial.println(statusCode);
  Serial.print("Response: ");
  Serial.println(response);

  if (statusCode == 200) {
    Serial.println("✅ Data sent successfully!");
  } else {
    Serial.println("❌ Failed to send data.");
  }
}

void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}
