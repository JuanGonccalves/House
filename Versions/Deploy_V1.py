#source C:/Users/JUAN.MARTINS/Portifolio/House_Sales_in_King_County_USA/.venv/Scripts/activate

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import numpy as np
from yellowbrick.regressor import ResidualsPlot 
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, learning_curve

arquivo = 'Data/kc_house_data.csv'
base = pd.read_csv(arquivo)
base = base.drop(['id', 'date'],axis=1)

df = base[['price', 'bedrooms', 'bathrooms', 'sqft_living',
       'sqft_lot', 'floors', 'waterfront', 'view', 'grade',
       'sqft_above', 'sqft_basement', 'yr_built','zipcode',
       'lat', 'long', 'sqft_living15', 'sqft_lot15']]

correlation = df.corr()
# Ajustar o tamanho da figura
plt.figure(figsize=(15, 8))  # Ajuste a largura e altura conforme necessário

# Criar o heatmap
plot = sns.heatmap(correlation, annot=True, fmt=".1f", linewidths=.6)

X = df.drop('price', axis=1).values
y = df['price'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
score = model.score(X_test,y_test)
mse = mean_squared_error(y_test, y_pred)

print(f"Visualização dos coeficientes: {model.intercept_}")
print(f"Visualização da inclinação da reta: {model.coef_}")
print(f"O Modelo possui um Coeficiente R^2 de: {score:.2f}")
print(f'Mean Squared Error: {round(mse,2)}')