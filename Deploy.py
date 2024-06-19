# Ativar o ambiente virtual (descomentar se necessário)
# source C:/Users/JUAN.MARTINS/Portifolio/House_Sales_in_King_County_USA/.venv/Scripts/activate

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import numpy as np
from yellowbrick.regressor import ResidualsPlot 
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, learning_curve

# Carregar dados
def load_data(filepath):
    data = pd.read_csv(filepath)
    data = data.drop(['id', 'date'], axis=1)
    return data

# Calcular correlação e plotar heatmap
def plot_correlation_heatmap(df):
    correlation = df.corr()
    plt.figure(figsize=(15, 8))
    sns.heatmap(correlation, annot=True, fmt=".1f", linewidths=.6)
    plt.title('Heatmap de Correlação')
    plt.show()

# Treinamento e avaliação do modelo
def train_and_evaluate(df):
    X = df.drop('price', axis=1).values
    y = df['price'].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    score = model.score(X_test, y_test)
    mse = mean_squared_error(y_test, y_pred)
    
    print(f"Intercepto do modelo: {model.intercept_}")
    print(f"Coeficientes do modelo: {model.coef_}")
    print(f"Coeficiente R^2: {score:.2f}")
    print(f'Mean Squared Error: {round(mse, 2)}')
    
    return model, X_test, y_test, y_pred

# Plotar os resíduos
def plot_residuals(model, X_train, y_train, X_test, y_test):
    visualizer = ResidualsPlot(model)
    visualizer.fit(X_train, y_train)
    visualizer.score(X_test, y_test)
    visualizer.show()

# Função principal
def main():
    filepath = 'Data/kc_house_data.csv'
    df = load_data(filepath)
    
    plot_correlation_heatmap(df)
    
    model, X_test, y_test, y_pred = train_and_evaluate(df)
    
    # Plotar resíduos
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop('price', axis=1), df['price'], test_size=0.2, random_state=42)
    plot_residuals(model, X_train.values, y_train.values, X_test.values, y_test.values)

# Executar o script principal
if __name__ == "__main__":
    main()
