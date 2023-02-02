# -*- coding: utf-8 -*-
"""Thesis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VNOBfleq6CsgfwHxz8IWaeWB00Bly0F1
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime as dt
import math

symbol = 'HPG'
date_milestone = '2021-01-01'

url = f'https://raw.githubusercontent.com/bachbnt/learn-stock_prediction-python/v2/data/{symbol}.csv'
dataset_all = pd.read_csv(url)
dataset_all.head()

dataset_train = dataset_all[dataset_all['Date'] < date_milestone]
dataset_test = dataset_all[dataset_all['Date'] >= date_milestone]

print(dataset_test.size)

training_set = dataset_train.iloc[:, 1:2].values
test_set = dataset_test.iloc[:, 1:2].values

# print(training_set)

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range=(0,1))
training_set_scaled = sc.fit_transform(training_set)

X_train = []
y_train = []
for i in range(60, len(dataset_train)):
    X_train.append(training_set_scaled[i-60:i, 0])
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Dense

model = Sequential()

model.add(LSTM(units=50,return_sequences=True,input_shape=(X_train.shape[1], 1)))
model.add(Dropout(0.2))

model.add(LSTM(units=50,return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units=50,return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units=50))
model.add(Dropout(0.2))

model.add(Dense(units=1))

model.compile(optimizer='adam',loss='mean_squared_error')

model.fit(X_train,y_train,epochs=100,batch_size=32)

dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
print(inputs)
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
print(inputs.size)
X_test = []
for i in range(60, len(inputs)):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_set = model.predict(X_test)
predicted_set = sc.inverse_transform(predicted_set)

real_price = test_set.flatten()
predicted_price = predicted_set.flatten()

# Root Mean Square Error - RMSE
total = 0
n = len(real_price)
for i in range(n):
  total += math.pow(real_price[i] - predicted_price[i], 2)
rmse = math.sqrt(total/n)

# 5.3526*1000
# 1119.8980646153511
print(rmse)

# Mean Absolute Error - MAE
total = 0
n = len(real_price)
for i in range(n):
  total += abs(real_price[i] - predicted_price[i])
mae = total/n

# 4.0268*1000
# 885.3326075819674
print(mae)

# Mean Absolute Percent Error MAPE
total = 0
n = len(real_price)
for i in range(n):
  total += abs(real_price[i] - predicted_price[i])/real_price[i]
mape = total/n

# 0.0168
# 0.027457068357071884
print(mape)

# Average Return - AR
total = 0
n = len(real_price)
for i in range(n - 1):
  if(predicted_price[i+1] > predicted_price[i]):
    total += real_price[i+1] - real_price[i]
ar = total/(n-1)

# -0.9632876712328429
print(ar)

# plt.plot(training_set, label = 'Training Price')
plt.plot(test_set, label = 'Test Price')
plt.plot(predicted_set, label = 'Predicted Price')
plt.title(f'{symbol} Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.legend()
plt.show()

# bổ sung thuế phí trong công thức tính lợi nhuận
# chạy sai số trên tập train => so sánh với tập test => overfit or underfit

# Average Return - AR
# Thuế phí
total = 0
n = len(real_price)
for i in range(n - 1):
  if(predicted_price[i+1] > predicted_price[i]):
    tax_fee = real_price[i]*0.0015 + real_price[i+1]*0.0015 + real_price[i+1]*0.001
    total += real_price[i+1] - real_price[i] - tax_fee
ar = total/(n-1)

# -66.13681150684927
print(ar)

dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis = 0)
inputs = dataset_total[0:len(dataset_total) - len(dataset_test) + 60].values
print(inputs)
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_train = []
for i in range(60, len(inputs)):
    X_train.append(inputs[i-60:i, 0])
X_train = np.array(X_train)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
predicted_set = model.predict(X_train)
predicted_set = sc.inverse_transform(predicted_set)

real_price = training_set.flatten()
predicted_price = predicted_set.flatten()

print(real_price.size)
print(predicted_price.size)

# Root Mean Square Error - RMSE
total = 0
n = len(real_price)
for i in range(n):
  total += math.pow(real_price[i] - predicted_price[i], 2)
rmse = math.sqrt(total/n)
print(rmse) # 2195.258106239992

# Mean Absolute Error - MAE
total = 0
n = len(real_price)
for i in range(n):
  total += abs(real_price[i] - predicted_price[i])
mae = total/n
print(mae) # 1496.0358359542136

# Mean Absolute Percent Error MAPE
total = 0
n = len(real_price)
for i in range(n):
  total += abs(real_price[i] - predicted_price[i])/real_price[i]
mape = total/n
print(mape) # 0.1576353579783943

# => overfit
# giảm số lớp
# giảm số epoch