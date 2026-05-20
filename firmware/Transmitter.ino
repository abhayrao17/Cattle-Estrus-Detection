#include <Wire.h>
#include <SPI.h>
#include <LoRa.h>

// ======================
// LoRa Pins
// ======================

#define SS 5
#define RST 14
#define DIO0 2

// ======================
// MPU6050
// ======================

const int MPU = 0x68;

int16_t AcX, AcY, AcZ;

void setup() {

  Serial.begin(115200);

  // RANDOM SEED FOR FAKE TEMP
  randomSeed(micros());

  // ======================
  // START I2C
  // ======================

  Wire.begin(21, 22);

  // WAKE UP MPU6050

  Wire.beginTransmission(MPU);

  Wire.write(0x6B);

  Wire.write(0);

  Wire.endTransmission(true);

  Serial.println("MPU6050 Ready");

  // ======================
  // START LORA
  // ======================

  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(433E6)) {

    Serial.println("LoRa init failed!");

    while (1);
  }

  Serial.println("LoRa Transmitter Ready");
}

void loop() {

  // ======================
  // READ MPU6050
  // ======================

  Wire.beginTransmission(MPU);

  Wire.write(0x3B);

  Wire.endTransmission(false);

  Wire.requestFrom(MPU, 6, true);

  AcX = Wire.read() << 8 | Wire.read();
  AcY = Wire.read() << 8 | Wire.read();
  AcZ = Wire.read() << 8 | Wire.read();

  // ======================
  // CALCULATE ACTIVITY
  // ======================

  float activity =
    (abs(AcX) +
     abs(AcY) +
     abs(AcZ)) / 1000.0;

  // ======================
  // FAKE TEMPERATURE
  // ======================

  float temperature =
    random(370, 395) / 10.0;

  // ======================
  // PRINT VALUES
  // ======================

  Serial.print("Activity: ");

  Serial.print(activity);

  Serial.print(" | Temp: ");

  Serial.println(temperature);

  // ======================
  // SEND THROUGH LORA
  // ======================

  LoRa.beginPacket();

  LoRa.print(activity);

  LoRa.print(",");

  LoRa.print(temperature);

  LoRa.endPacket();

  Serial.println("Packet Sent");

  delay(2000);
}