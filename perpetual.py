import streamlit as st

# Definir datos estáticos sobre los exchanges
exchanges = {
    "Woo": {"taker_fee": 0.0004, "maker_fee": 0.0002, "funding_rate": 0.0006},
    "Hyperliquid": {"taker_fee": 0.0004, "maker_fee": 0.0002, "funding_rate": -0.0001},
    "Satori": {"taker_fee": 0.0004, "maker_fee": 0.0002, "funding_rate": 0.0003}
}

# Definir la función para calcular la tabla
def calcular_tabla(valor_trade, apalancamiento, num_dias):
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

    beneficio_total = num_dias * beneficio_en_dolares - comisiones_totales

    # Calcular el APR
    APR = round(((beneficio_total / num_dias) / (valor_trade * 2)) * 365 * 100,2)

    return {
        "Exchange": [exchange_menor_funding, exchange_mayor_funding],
        "Funding (%)": [f'{funding_menor:.2f}%', f'{funding_mayor:.2f}%'],
        "Fee ($)": [f'${fee_exchange_menor:.2f}', f'${fee_exchange_mayor:.2f}'],
        "Comisiones Totales ($)": f'${comisiones_totales:.2f}',
        "Volumen Generado ($)": f'${volumen_generado:.2f}',
        "Beneficio por Día (%)": f'{beneficio_por_dia_pct:.2f}%',
        "Beneficio en Dólares ($)": f'${beneficio_en_dolares:.2f}',
        "Break Even (Días)": f'{break_even_dias:.2f}',
        "Break Even (Horas)": f'{break_even_horas:.2f}',
        "Beneficio Total ($)": f'${beneficio_total:.2f}',
        "APR (%)": f'{APR:.2f}%'
    }

st.title("Calculadora de Arbitraje de Perpetuos")
valor_trade = st.number_input("Valor del Trade", min_value=0.01, step=0.01)
apalancamiento = st.number_input("Apalancamiento", min_value=1, step=1)
num_dias = st.number_input("Número de Días", min_value=1, step=1)

if st.button("Calcular"):
    resultado = calcular_tabla(valor_trade, apalancamiento, num_dias)
    st.write(resultado)

