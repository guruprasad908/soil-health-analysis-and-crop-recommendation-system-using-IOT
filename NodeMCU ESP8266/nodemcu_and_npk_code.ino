#include <Wire.h>
#include <U8g2lib.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h> // Make sure to install ArduinoJson library

// --- OLED (SH1106 I2C) ---
U8G2_SH1106_128X64_NONAME_F_HW_I2C oled(U8G2_R0, U8X8_PIN_NONE);

// --- WIFI CONFIGURATION ---
const char* ssid = "Sneha";
const char* password = "12345678";
// REPLACE WITH YOUR PC IP
const char* serverBaseUrl = "http://10.120.223.241:8000/api/sensor"; 

// --- NPK SAMPLE DATA (REALISTIC VALUES) ---
struct NPKSet {
  int N, P, K;
};

NPKSet npkData[] = {
  {27, 71, 24},
  {33, 58, 24},
  {30, 60, 21},
  {11, 41, 19},
  {35, 38, 19},
  {39, 36, 22},
  {32, 48, 18},
  {29, 54, 16},
  {26, 54, 17},
  {36, 38, 15}
};

int npkIndex = 0;

// Realistic bounds
const int MIN_N = 10, MAX_N = 40;
const int MIN_P = 35, MAX_P = 75;
const int MIN_K = 15, MAX_K = 30;

// Button Configuration (D3 = FLASH button)
const int buttonPin = D3;
bool lastButtonState = HIGH;

// Current displayed values
int baseN, baseP, baseK;
int dispN, dispP, dispK;

// Jitter config
unsigned long lastJitterTime = 0;
const unsigned long jitterInterval = 2000;  // jitter every 2 sec
int jitterCycles = 5;                      // number of jitters after button press
int jitterLeft = 0;

// Polling config
unsigned long lastPollTime = 0;
const unsigned long pollInterval = 2000; // Poll every 2 seconds

// Clamp helper
int clampVal(int v, int lo, int hi) {
  return v < lo ? lo : v > hi ? hi : v;
}

// OLED Display
void displayNPK(int N, int P, int K) {
  oled.clearBuffer();
  oled.setFont(u8g2_font_6x13_tr);

  oled.setCursor(22, 15);
  oled.print("SOIL NPK STATUS");
  oled.drawHLine(0, 20, 128);

  oled.setCursor(10, 38);
  oled.printf("N : %3d mg/kg", N);

  oled.setCursor(10, 52);
  oled.printf("P : %3d mg/kg", P);

  oled.setCursor(10, 63);
  oled.printf("K : %3d mg/kg", K);
  
  // WiFi Status Indicator
  if (WiFi.status() == WL_CONNECTED) {
    oled.drawStr(110, 63, "W");
  } else {
    oled.drawStr(110, 63, "X");
  }

  oled.sendBuffer();
}

// Send Data to Backend
void sendDataToBackend(int n, int p, int k) {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;

    String url = String(serverBaseUrl) + "/npk";
    http.begin(client, url);
    http.addHeader("Content-Type", "application/json");

    String payload = "{\"n\": " + String(n) + ", \"p\": " + String(p) + ", \"k\": " + String(k) + "}";
    
    int httpResponseCode = http.POST(payload);

    if (httpResponseCode > 0) {
      Serial.print("Data Sent. Code: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("Error sending data: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }
}

// Check for Server Commands
bool checkServerCommand() {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;

    String url = String(serverBaseUrl) + "/command";
    http.begin(client, url);
    
    int httpResponseCode = http.GET();
    bool commandReceived = false;

    if (httpResponseCode == 200) {
      String payload = http.getString();
      // Simple string check to avoid heavy JSON parsing if possible, but JSON is safer
      // Expected: {"command": "next"} or {"command": null}
      if (payload.indexOf("\"next\"") > 0) {
        Serial.println("Command 'next' received from server!");
        commandReceived = true;
      }
    }
    http.end();
    return commandReceived;
  }
  return false;
}

// Clear Server Command
void clearServerCommand() {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;

    String url = String(serverBaseUrl) + "/command/clear";
    http.begin(client, url);
    http.POST(""); // Empty POST to clear
    http.end();
    Serial.println("Command cleared on server.");
  }
}

// Core Logic: Cycle NPK
void cycleNPK() {
    // Next base value
    npkIndex = (npkIndex + 1) % (sizeof(npkData) / sizeof(npkData[0]));

    baseN = npkData[npkIndex].N;
    baseP = npkData[npkIndex].P;
    baseK = npkData[npkIndex].K;

    dispN = baseN;
    dispP = baseP;
    dispK = baseK;

    displayNPK(dispN, dispP, dispK);
    
    // Send new base data to backend
    sendDataToBackend(dispN, dispP, dispK);

    Serial.printf("New Base → N:%d P:%d K:%d\n", baseN, baseP, baseK);

    jitterLeft = jitterCycles;       // enable jitter
    lastJitterTime = millis();
}

// Apply one ±1 jitter
void applyJitter() {
  dispN = clampVal(baseN + random(-1, 2), MIN_N, MAX_N);
  dispP = clampVal(baseP + random(-1, 2), MIN_P, MAX_P);
  dispK = clampVal(baseK + random(-1, 2), MIN_K, MAX_K);

  displayNPK(dispN, dispP, dispK);
  Serial.printf("Jitter → N:%d P:%d K:%d\n", dispN, dispP, dispK);
}

// --- SETUP ---
void setup() {
  Serial.begin(9600);

  oled.begin();
  oled.setContrast(200);

  pinMode(buttonPin, INPUT_PULLUP);

  randomSeed(analogRead(A0));
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  int retry = 0;
  while (WiFi.status() != WL_CONNECTED && retry < 20) {
    delay(500);
    Serial.print(".");
    retry++;
  }
  Serial.println();
  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("Connected, IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("Connection failed");
  }

  // Initialize base values
  baseN = npkData[npkIndex].N;
  baseP = npkData[npkIndex].P;
  baseK = npkData[npkIndex].K;

  dispN = baseN;
  dispP = baseP;
  dispK = baseK;
  displayNPK(dispN, dispP, dispK);
  
  // Send initial data
  sendDataToBackend(dispN, dispP, dispK);

  Serial.println("Ready with Dual Trigger System!");
}

// --- LOOP ---
void loop() {
  bool buttonState = digitalRead(buttonPin);
  bool triggered = false;

  // 1. Check Physical Button (LOW → pressed)
  if (buttonState == LOW && lastButtonState == HIGH) {
    Serial.println("Trigger: Physical Button");
    triggered = true;
    delay(350); // debounce
  }

  // 2. Check Server Command (Polling)
  if (!triggered && millis() - lastPollTime >= pollInterval) {
    if (checkServerCommand()) {
      Serial.println("Trigger: Remote Command");
      triggered = true;
      clearServerCommand(); // Acknowledge and clear
    }
    lastPollTime = millis();
  }

  // Execute Logic if Triggered
  if (triggered) {
    cycleNPK();
  }

  lastButtonState = buttonState;

  // Perform micro jitter
  if (jitterLeft > 0 && millis() - lastJitterTime >= jitterInterval) {
    applyJitter();
    jitterLeft--;
    lastJitterTime = millis();
  }
}
