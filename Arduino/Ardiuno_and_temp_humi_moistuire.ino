#include <Wire.h>
#include <U8g2lib.h>
#include <DHT.h>

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

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(SOIL_PIN, INPUT);

  oled.begin();
  oled.setFont(u8g2_font_7x14_tf);
  oled.clearBuffer();
  oled.drawStr(15, 30, "SOIL MONITOR");
  oled.drawStr(25, 50, "Initializing...");
  oled.sendBuffer();
  delay(2000);
}

void loop() {
  if (millis() - lastReadTime >= refreshInterval) {
    lastReadTime = millis();

    // ----- Soil Moisture -----
    int soilValue = analogRead(SOIL_PIN);
    moisturePercent = map(soilValue, 1023, 200, 0, 100);
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
  }
}
