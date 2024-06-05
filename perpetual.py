import requests
from bs4 import BeautifulSoup
import streamlit as st

def obtener_funding(criptomoneda):
    # URL de la API
    url = "https://api.hyperliquid.xyz/info"

    # Encabezados
    headers = {
        "Content-Type": "application/json"
    }

    # Cuerpo de la solicitud
    data = {
        "type": "metaAndAssetCtxs"
    }

    # Hacer la solicitud POST
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        response_data = response.json()

        # Procesar la respuesta para crear DataFrames
        universe_data = response_data[0]["universe"]
        asset_context_data = response_data[1]

        # Crear DataFrame para "universe"
        universe_df = pd.DataFrame(universe_data)
        
        # Crear DataFrame para "asset contexts"
        asset_context_df = pd.DataFrame(asset_context_data)
        
        # Añadir una columna 'name' al asset_context_df basada en el nombre
        asset_context_df['name'] = universe_df['name']
        
        # Combinar ambos DataFrames basados en la columna 'name'
        combined_df = pd.merge(universe_df, asset_context_df, on='name')
        
        # Filtrar por la criptomoneda seleccionada
        result_df = combined_df[combined_df['name'] == criptomoneda][['name', 'funding']]
        
        return result_df
    else:
        st.error(f"Error en la solicitud: {response.status_code}")
        st.error(response.text)

def obtener_porcentaje_cambio(criptomoneda):
    if criptomoneda == "BTC":
        url = "https://scroll.satori.finance/trade/BTC-USD"
    else:
        url = "https://scroll.satori.finance/trade/"

    proxies = {
        "https": "scraperapi.render=true:ed44b678b839d0e71d4e1279cccf6ee5@proxy-server.scraperapi.com:8001"
    }

    r = requests.get(url, proxies=proxies, verify=False)
    html_text = r.text
    soup = BeautifulSoup(html_text, 'html.parser')
    span_list = soup.findAll('span', {'data-v-5d706ddf': ''})
    
    span_list2 = []
    for span in span_list:
        if '%' in span.text:
            span_list2.append(span.text.strip())
    
    if span_list2:
        valor_porcentaje = span_list2[1].split('%')[0]
        return valor_porcentaje
    else:
        return "No se encontraron datos de porcentaje de cambio"

def obtener_datos_woo(criptomoneda):
    if criptomoneda == "BTC":
        url = "https://dex.woo.org/en/trade/BTC_PERP"
    else:
        url = "https://dex.woo.org/en/trade/ETH_PERP"

    proxies = {
        "https": "scraperapi.render=true:ed44b678b839d0e71d4e1279cccf6ee5@proxy-server.scraperapi.com:8001"
    }

    r = requests.get(url, proxies=proxies, verify=False)
    html_text = r.text
    soup = BeautifulSoup(html_text, "html.parser")
    span_element = soup.find("span", class_="orderly-inline-flex orderly-items-center orderly-gap-1 orderly-tabular-nums orderly-text-warning")

    if span_element:
        return span_element.text.strip()
    else:
        return "No se encontró el elemento span con las clases especificadas."

# Interfaz de usuario con Streamlit
st.title("Información de Criptomonedas")
criptomoneda = st.selectbox("Selecciona una criptomoneda", ["BTC", "ETH"])

if st.button("Obtener Información"):
    funding_df = obtener_funding(criptomoneda)
    porcentaje_cambio = obtener_porcentaje_cambio(criptomoneda)
    datos_woo = obtener_datos_woo(criptomoneda)
    st.write("Funding de", criptomoneda)
    st.write(funding_df)
    st.write("Porcentaje de cambio:", porcentaje_cambio)
    st.write("Datos Woo:", datos_woo)
