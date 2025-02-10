import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load dataset
df = pd.read_csv("https://raw.githubusercontent.com/jbrownlee/Datasets/master/shampoo.csv")
df.columns = ["Month", "Sales"]
df["Month"] = pd.to_datetime(df["Month"])
df.set_index("Month", inplace=True)

# Visualization
plt.figure(figsize=(10, 5))
plt.plot(df.index, df["Sales"], marker='o', linestyle='-', label="Sales Data")
plt.xlabel("Time")
plt.ylabel("Sales")
plt.title("Sales Over Time")
plt.legend()
plt.show()

# Splitting data into train and test sets
train_size = int(len(df) * 0.8)
train, test = df[:train_size], df[train_size:]

# Model training using SARIMA
model = SARIMAX(train["Sales"], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
model_fit = model.fit()

# Forecasting
forecast = model_fit.predict(start=len(train), end=len(train) + len(test) - 1, dynamic=False)

# Evaluation
mae = mean_absolute_error(test["Sales"], forecast)
mse = mean_squared_error(test["Sales"], forecast)
rmse = np.sqrt(mse)

print(f"MAE: {mae:.2f}")
print(f"MSE: {mse:.2f}")
print(f"RMSE: {rmse:.2f}")

# Plot results
plt.figure(figsize=(10, 5))
plt.plot(train.index, train["Sales"], label="Training Data")
plt.plot(test.index, test["Sales"], label="Actual Sales", color='green')
plt.plot(test.index, forecast, label="Predicted Sales", color='red', linestyle="dashed")
plt.xlabel("Time")
plt.ylabel("Sales")
plt.title("Sales Forecasting with SARIMA")
plt.legend()
plt.show()
