import streamlit as st

# Definir datos estáticos sobre los exchanges
exchanges = {
    "Woo": {"taker_fee": 0.0004, "maker_fee": 0.0002, "funding_rate": 0.0006},
    "Hyperliquid": {"taker_fee": 0.0004, "maker_fee": 0.0002, "funding_rate": -0.0001},
    "Satori": {"taker_fee": 0.0004, "maker_fee": 0.0002, "funding_rate": 0.0003}
}

# Definir la función para calcular la tabla
def calcular_tabla(valor_trade, apalancamiento):
    # Encontrar el exchange con la mayor y menor tasa de financiación
    exchange_menor_funding = min(exchanges, key=lambda x: exchanges[x]["funding_rate"])
    exchange_mayor_funding = max(exchanges, key=lambda x: exchanges[x]["funding_rate"])

    # Calcular las tasas de financiación y la diferencia entre ellas
    funding_menor = exchanges[exchange_menor_funding]["funding_rate"]
    funding_mayor = exchanges[exchange_mayor_funding]["funding_rate"]
    diferencia_funding = funding_mayor - funding_menor

    # Calcular las comisiones de taker por trade para ambos exchanges
    fee_exchange_menor = exchanges[exchange_menor_funding]["taker_fee"] * apalancamiento * valor_trade
    fee_exchange_mayor = exchanges[exchange_mayor_funding]["taker_fee"] * apalancamiento * valor_trade

    # Calcular las comisiones totales y el volumen generado
    comisiones_totales = fee_exchange_menor + fee_exchange_mayor
    volumen_generado = valor_trade * apalancamiento

    # Calcular el beneficio por día en porcentaje y en dólares
    beneficio_por_dia_pct = diferencia_funding * 3
    beneficio_en_dolares = beneficio_por_dia_pct * valor_trade * apalancamiento

    # Calcular el break even en días y en horas
    break_even_dias = comisiones_totales / beneficio_en_dolares
    break_even_horas = break_even_dias * 24

    return {
        "Exchange Menor Funding": exchange_menor_funding,
        "Exchange Mayor Funding": exchange_mayor_funding,
        "Funding Menor": funding_menor,
        "Funding Mayor": funding_mayor,
        "Diferencia Funding": diferencia_funding,
        "Fee Exchange Menor": fee_exchange_menor,
        "Fee Exchange Mayor": fee_exchange_mayor,
        "Comisiones Totales": comisiones_totales,
        "Volumen Generado": volumen_generado,
        "Beneficio por Día (%)": beneficio_por_dia_pct,
        "Beneficio en Dólares": beneficio_en_dolares,
        "Break Even (Días)": break_even_dias,
        "Break Even (Horas)": break_even_horas
    }

# Configurar la interfaz de usuario con Streamlit
st.title("Calculadora de Arbitraje de Perpetuos")
valor_trade = st.number_input("Valor del Trade", min_value=0.01, step=0.01)
apalancamiento = st.number_input("Apalancamiento", min_value=1, step=1)

if st.button("Calcular"):
    resultado = calcular_tabla(valor_trade, apalancamiento)
    st.write(resultado)
