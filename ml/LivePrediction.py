import serial
import joblib
import pandas as pd
import os

from Adafruit_IO import Client
ADAFRUIT_IO_USERNAME = os.getenv("AIO_USERNAME")
ADAFRUIT_IO_KEY = os.getenv("AIO_KEY")
aio = Client(
    ADAFRUIT_IO_USERNAME,
    ADAFRUIT_IO_KEY
)


model = joblib.load("model.pkl")


ser = serial.Serial('COM7', 115200)


temp_feed = "temperature"
activity_feed = "activity"
confidence_feed = "confidence-level"
status_feed = "estrus"

print("\nLIVE ESTRUS MONITORING STARTED\n")


while True:

    try:

        

        line = ser.readline().decode().strip()

        print("Received:", line)

        values = line.split(",")

        activity = float(values[0])

        temperature = float(values[1])


        input_data = pd.DataFrame(
            [[activity, temperature]],
            columns=[
                "Activity",
                "Temperature"
            ]
        )


        prediction = model.predict(
            input_data
        )

        probability = model.predict_proba(
            input_data
        )

        confidence = max(
            probability[0]
        ) * 100


        if prediction[0] == 1:

            status = "Estrus Detected"

        else:

            status = "Normal"


        aio.send_data(
            temp_feed,
            temperature
        )

        aio.send_data(
            activity_feed,
            activity
        )

        aio.send_data(
            confidence_feed,
            confidence
        )

        aio.send_data(
            status_feed,
            status
        )

        print("-----------------------------------")

        print(
            f"Temperature       : "
            f"{temperature} °C"
        )

        print(
            f"Activity Index    : "
            f"{activity}"
        )

        print(
            f"Estrus Confidence : "
            f"{confidence:.2f}%"
        )

        print(
            f"Status            : "
            f"{status}"
        )

        print("-----------------------------------\n")

    except Exception as e:

        print("ERROR:", e)