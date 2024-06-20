import streamlit as st
import pandas as pd
import numpy as np
import pickle
import folium
from streamlit_folium import folium_static
from sklearn.linear_model import LinearRegression

# Carregar o modelo treinado
@st.cache(allow_output_mutation=True)
def load_model(filepath='Data/modelo.pkl'):
    with open(filepath, 'rb') as f:
        model = pickle.load(f)
    return model

# Carregar dados para cálculo da média de preço da área
def load_data(filepath='Data/kc_house_data.csv'):
    data = pd.read_csv(filepath)
    return data

# Calcular média de preço da área baseado na latitude e longitude
def calculate_mean_price(data, lat, long, radius=0.1):  # Define a área de busca (em graus)
    lat_min = lat - radius
    lat_max = lat + radius
    long_min = long - radius
    long_max = long + radius
    
    filtered_data = data[(data['lat'] >= lat_min) & (data['lat'] <= lat_max) &
                         (data['long'] >= long_min) & (data['long'] <= long_max)]
    
    mean_price = filtered_data['price'].mean()
    return mean_price

# Configuração da página
st.set_page_config(page_title='Previsão de Preços de Casas em King County', layout='wide')

# Função para fazer a previsão
def predict_price(model, features):
    prediction = model.predict(features)
    return prediction

# Carregar o modelo uma única vez
model = load_model()

# Carregar os dados uma única vez
data = load_data()

# Título da aplicação
st.title('Previsão de Preços de Casas em King County, EUA')

# Seção de entrada de dados
st.header('Insira os detalhes da casa:')

# Coleta de entradas do usuário
bedrooms = st.number_input('Número de Quartos', min_value=0)
bathrooms = st.number_input('Número de Banheiros', min_value=0.0)
sqft_living = st.number_input('Área Habitável (pés quadrados)', min_value=1)
sqft_lot = st.number_input('Área do Lote (pés quadrados)', min_value=1)
floors = st.number_input('Número de Andares', min_value=1.0)
waterfront = st.selectbox('Vista para o Mar', [0, 1])
view = st.number_input('Índice de Visão (0-4)', min_value=0)
condition = st.number_input('Condição da Casa (1-5)', min_value=1)
grade = st.number_input('Grau da Casa (1-13)', min_value=1)
sqft_above = st.number_input('Área Acima do Solo (pés quadrados)', min_value=1)
sqft_basement = st.number_input('Área do Porão (pés quadrados)', min_value=1)
yr_built = st.number_input('Ano de Construção', min_value=1900)
yr_renovated = st.number_input('Ano da Renovação', min_value=0)
zipcode = st.number_input('Código Postal', min_value=98001)
lat = st.number_input('Latitude', min_value=47.1559, max_value=47.7776)
long = st.number_input('Longitude', min_value=-122.519, max_value=-121.315)
sqft_living15 = st.number_input('Área Habitável dos Vizinhos (pés quadrados)', min_value=399, max_value=6210)
sqft_lot15 = st.number_input('Área do Lote dos Vizinhos (pés quadrados)', min_value=651, max_value=871200)

# Coleta das entradas em um array
features = np.array([[bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, view, condition, grade,
                      sqft_above, sqft_basement, yr_built, yr_renovated, zipcode, lat, long, sqft_living15, sqft_lot15]])

# Exibir média de preço da área
mean_price = calculate_mean_price(data, lat, long)

# Fazer a previsão quando o botão for clicado
if st.button('Prever Preço'):
    prediction = predict_price(model, features)
    st.write(f'Preço Previsto: ${prediction[0]:,.2f}')
    st.write(f'Média de Preço da Área: ${mean_price:,.2f}')

# Exibir mapa do local
st.header('Mapa do Local:')
m = folium.Map(location=[lat, long], zoom_start=15)
folium.Marker([lat, long], popup='Localização Escolhida').add_to(m)
folium_static(m)

# Função principal para executar a aplicação
if __name__ == '__main__':
    st.title("Análise de Vendas de Casas em King County")
