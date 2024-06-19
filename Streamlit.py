import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib

# Função para carregar e treinar o modelo (para simplicidade, treinaremos o modelo a cada vez que o script rodar)
def train_model():
    # Carregar os dados
    df = pd.read_csv('Data/kc_house_data.csv')
    df = df.drop(['id', 'date', 'sqft_living15', 'sqft_lot15'], axis=1)  # Excluindo as variáveis

    # Separar variáveis independentes e dependentes
    X = df.drop('price', axis=1)
    y = df['price']

    # Dividir os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinar o modelo
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Salvar o modelo treinado
    joblib.dump(model, 'house_price_model.pkl')

    return X_train, model  # Retorna X_train para ser usado fora da função

# Função para carregar o modelo treinado
def load_model():
    return joblib.load('house_price_model.pkl')

# Treinar o modelo (isso geralmente seria feito separadamente, não dentro do app Streamlit)
X_train, model = train_model()  # Chama a função e atribui X_train e model

# Configurar a interface do Streamlit
st.title('King County House Price Prediction')
st.write("Insira os detalhes da casa para prever o preço:")

# Coletar entradas do usuário
bedrooms = st.number_input('Number of Bedrooms', min_value=0)
bathrooms = st.number_input('Number of Bathrooms', min_value=0.0, max_value=10.0, value=2.0)
sqft_living = st.number_input('Square Feet Living Area', min_value=0, max_value=10000, value=2000)
sqft_lot = st.number_input('Square Feet Lot Area', min_value=0, max_value=100000, value=5000)
floors = st.number_input('Number of Floors', min_value=1.0, max_value=3.0, value=1.0)
waterfront = st.selectbox('Waterfront View', options=[0, 1])
view = st.selectbox('View', options=[0, 1, 2, 3, 4])
grade = st.selectbox('Grade', options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
sqft_above = st.number_input('Square Feet Above', min_value=0, max_value=10000, value=1500)
sqft_basement = st.number_input('Square Feet Basement', min_value=0, max_value=5000, value=500)
yr_built = st.number_input('Year Built', min_value=1900, max_value=2024, value=1970)
zipcode = st.number_input('Zipcode', min_value=98001, max_value=98199, value=98103)
lat = st.number_input('Latitude', min_value=47.0, max_value=48.0, value=47.5)
longitude = st.number_input('Longitude', min_value=-122.0, max_value=-121.0, value=-122.0)

# Prever o preço quando o botão é clicado
if st.button('Predict Price'):
    # Criar um array numpy com os dados de entrada
    input_data = np.array([[bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, view, grade, 
                            sqft_above, sqft_basement, yr_built, zipcode, lat, longitude]])
    
    # Certificar-se de que o número de features (colunas) seja o mesmo que o modelo espera
    if input_data.shape[1] == X_train.shape[1]:
        predicted_price = model.predict(input_data)
        st.write(f'O preço previsto para a casa é: ${predicted_price[0]:,.2f}')
    else:
        st.error('Erro: O número de características inseridas não corresponde ao modelo treinado.')
