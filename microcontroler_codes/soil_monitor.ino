#include <Wire.h>
#include <U8g2lib.h>
#include <DHT.h>
#include <WiFiS3.h>
#include <ArduinoHttpClient.h>

// ----- OLED -----
U8G2_SH1106_128X64_NONAME_F_HW_I2C oled(U8G2_R0, U8X8_PIN_NONE);

// ----- DHT22 -----
#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// ----- Soil Sensor -----
#define SOIL_PIN A0

// ----- WiFi -----
const char* ssid = "Apoorvaaa";
const char* password = "apoorvaaa";

char serverAddress[] = "10.238.141.218";
int port = 8000;
String endpoint = "/soil-data";

WiFiClient wifi;
HttpClient client = HttpClient(wifi, serverAddress, port);

// ----- Timers -----
unsigned long lastReadTime = 0;
const unsigned long refreshInterval = 5000;

// ----- Data -----
int moisturePercent = 0;
float tempC = 0.0;
float humidity = 0.0;

void safeDHTRead() {
  // Try 5 times
  for (int i=0; i<5; i++) {
    tempC = dht.readTemperature();
    humidity = dht.readHumidity();

    if (!isnan(tempC) && !isnan(humidity)) return;
    delay(100);
  }
  // If still invalid, keep old values and print warning
  Serial.println("⚠️ DHT22 unstable, using previous values...");
}

void connectWiFi() {
  Serial.println("🌐 Connecting...");
  WiFi.begin(ssid, password);

  unsigned long start = millis();
  while (millis() - start < 8000) {  // max 8 seconds
    if (WiFi.status() == WL_CONNECTED) break;
    Serial.print(".");
    delay(300);
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ WiFi Connected!");
  } else {
    Serial.println("\n❌ WiFi Timeout");
  }

  oled.clearBuffer();
  oled.setFont(u8g2_font_7x14_tf);
  oled.drawStr(10, 35, WiFi.status() == WL_CONNECTED ? "WiFi Connected!" : "WiFi Failed!");
  oled.sendBuffer();
  delay(1500);
}

void sendToServer() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("⚠️ Not connected, skip upload");
    return;
  }

  String json = "{\"Soil\":" + String(moisturePercent) +
                ",\"Temp\":" + String(tempC, 1) +
                ",\"Hum\":" + String(humidity, 1) + "}";

  client.beginRequest();
  client.post(endpoint);
  client.sendHeader("Content-Type", "application/json");
  client.sendHeader("Content-Length", json.length());
  client.beginBody();
  client.print(json);
  client.endRequest();

  int status = client.responseStatusCode();
  String response = client.responseBody();

  Serial.print("📤 POST ");
  Serial.println(json);
  Serial.print("🔁 Code: ");
  Serial.println(status);
}

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(SOIL_PIN, INPUT);

  oled.begin();
  oled.setFont(u8g2_font_7x14_tf);

  oled.clearBuffer();
  oled.drawStr(10, 35, "Initializing...");
  oled.sendBuffer();

  delay(2000);
  connectWiFi();
}

void loop() {
  // Always read sensors
  int rawSoil = analogRead(SOIL_PIN);
  moisturePercent = map(rawSoil, 1023, 200, 0, 100);
  moisturePercent = constrain(moisturePercent, 0, 100);

  safeDHTRead();  // replaces DHT error crash

  // OLED ALWAYS updates
  oled.firstPage();
  do {
    char s1[25], s2[25], s3[25];
    sprintf(s1, "Soil: %d %%", moisturePercent);
    sprintf(s2, "Temp: %.1f C", tempC);
    sprintf(s3, "Hum : %.1f %%", humidity);

    oled.drawStr(0, 20, s1);
    oled.drawStr(0, 40, s2);
    oled.drawStr(0, 60, s3);

  } while (oled.nextPage());

  // every 5 seconds → send
  if (millis() - lastReadTime >= refreshInterval) {
    lastReadTime = millis();
    sendToServer();
  }

  delay(200);
}