import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
import matplotlib.pyplot as plt

data = pd.read_csv("dataset.csv")

print("\nDATASET PREVIEW:\n")
print(data.head())


X = data[["Activity", "Temperature"]]
y = data["Estrus"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


print("\nTraining model...\n")

model.fit(X_train, y_train)

print("Training completed!")


y_pred = model.predict(X_test)


accuracy = accuracy_score(y_test, y_pred)

print("\nMODEL ACCURACY:")
print(f"{accuracy * 100:.2f}%")


cm = confusion_matrix(y_test, y_pred)

print("\nCONFUSION MATRIX:")
print(cm)


print("\nCLASSIFICATION REPORT:\n")
print(classification_report(y_test, y_pred))


joblib.dump(model, "model.pkl")

print("\nModel saved as model.pkl")


importance = model.feature_importances_

features = ["Activity", "Temperature"]

plt.bar(features, importance)

plt.xlabel("Features")
plt.ylabel("Importance")
plt.title("Feature Importance")

plt.show()


print("\nSAMPLE LIVE PREDICTION:\n")

sample_activity = 24
sample_temperature = 38.7

prediction = model.predict([[sample_activity, sample_temperature]])

if prediction[0] == 1:
    print("Estrus Likely")
else:
    print("No Estrus")

print(f"\nActivity = {sample_activity}")
print(f"Temperature = {sample_temperature}")