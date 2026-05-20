# Cattle Estrus Detection

Missed estrus in cattle costs farmers ₹8,000–12,000 per cycle due to lost breeding opportunities. Manual monitoring is unreliable and labor-intensive.

This system attaches a battery-powered transmitter to cattle that continuously reads body temperature (DS18B20) and activity level (MPU6050), transmits data over LoRa (5+ km range) to a base station, runs it through a trained Random Forest classifier, and pushes results to a live Adafruit IO dashboard — all in real time.

## System Architecture

<img width="500" alt="System architecture diagram" src="https://github.com/user-attachments/assets/8a38f441-7505-4bd9-a72b-f5a588f53b1e" />

---

## Hardware

### Transmitter (Cattle Unit)

| Component | Purpose |
|-----------|---------|
| ESP32 | Main microcontroller |
| LoRa SX1278 | Long-range wireless transmission |
| DS18B20 | Body temperature sensing |
| MPU6050 | Activity / movement sensing |
| 18650 Battery Pack | Portable power supply |

### Receiver (Base Station)

| Component | Purpose |
|-----------|---------|
| ESP32 | Receives LoRa packets, sends via Serial |
| LoRa SX1278 | Long-range wireless reception |

### Photos

| Receiver Unit | Transmitter Unit |
|---|---|
| <img src="https://github.com/user-attachments/assets/55e9669b-4e53-416e-9ed1-c71a8850c358" width="350" alt="Receiver unit"/> | <img src="https://github.com/user-attachments/assets/7154b826-6155-4c0d-a869-53d229eaa1de" width="350" alt="Transmitter unit"/> |

---

## Project Structure

```
cattle-estrus-detection/
├── ml/
│   ├── TrainModel.py        # Train and evaluate the Random Forest model
│   ├── LivePrediction.py    # Real-time prediction from serial + push to cloud
│   ├── dataset.csv          # Training dataset (activity + temperature labels)
│   └── model.pkl            # Saved trained model
├── hardware/
│   ├── receiver.jpg
│   ├── transmitter.jpg
│   └── system_architecture.png
├── firmware/
│   └── (ESP32 .ino files)   # Arduino firmware for TX and RX units
└── README.md
```

---

## Machine Learning

- **Algorithm:** Random Forest Classifier (100 estimators)
- **Features:** Activity Index, Body Temperature (°C)
- **Target:** Estrus (1) / Normal (0)
- **Accuracy:** ~91% on held-out test set (80/20 split)

### Training the Model

```bash
pip install pandas scikit-learn matplotlib joblib
python ml/TrainModel.py
```

Output includes accuracy score, confusion matrix, classification report, and a feature importance chart.

---

## Live Prediction & Cloud Monitoring

`LivePrediction.py` reads incoming LoRa data from the receiver ESP32 over serial, runs the ML model, and pushes four live feeds to Adafruit IO:

| Feed | Description |
|------|-------------|
| `temperature` | Body temperature in °C |
| `activity` | Activity index from MPU6050 |
| `confidence-level` | Model prediction confidence (%) |
| `estrus` | Status: *Estrus Detected* or *Normal* |

### Setup

1. Create a `.env` file (never commit this):

```env
AIO_USERNAME=your_username
AIO_KEY=your_key_here
```

2. Install dependencies:

```bash
pip install pyserial joblib pandas adafruit-io python-dotenv
```

3. Update the serial port in `LivePrediction.py` to match your system (e.g. `COM7` on Windows, `/dev/ttyUSB0` on Linux).

4. Run:

```bash
python ml/LivePrediction.py
```

### Sample Output

```
LIVE ESTRUS MONITORING STARTED

Received: 26.4,39.1
-----------------------------------
Temperature       : 39.1 °C
Activity Index    : 26.4
Estrus Confidence : 94.00%
Status            : Estrus Detected
-----------------------------------
```

---

## Security

Never hardcode your Adafruit IO key. Use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

ADAFRUIT_IO_USERNAME = os.getenv("AIO_USERNAME")
ADAFRUIT_IO_KEY      = os.getenv("AIO_KEY")
```

---

## Results

| Metric | Value |
|--------|-------|
| ML Accuracy | ~91% |
| LoRa Range | 5+ km (open field) |
| Packet Loss | <3% |
| Monitoring Time Saved | ~2 hours/day per farmer |

---

## Author

**Abhay Rao**  
ECE Undergraduate — REVA University (2027)  
📧 rao546518@gmail.com
