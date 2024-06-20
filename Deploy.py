import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pickle
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, learning_curve
import os

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

# Salvar o modelo treinado
def save_model(model, filepath):
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)
    print(f'Modelo salvo em {filepath}')

# Função principal
def main():
    data_filepath = 'Data/kc_house_data.csv'
    model_filepath = 'Data/modelo.pkl'
    
    # Verificar se o diretório Data existe
    if not os.path.exists('Data'):
        os.makedirs('Data')
    
    df = load_data(data_filepath)
    
    plot_correlation_heatmap(df)
    
    model, X_test, y_test, y_pred = train_and_evaluate(df)
    
    # Salvar o modelo na pasta Data
    save_model(model, model_filepath)

# Executar o script principal
if __name__ == "__main__":
    main()
