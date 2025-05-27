import streamlit as st

st.set_page_config(page_title="Calculadora de Geração de Viagens", layout="centered")

st.title("🚦 Calculadora de Geração de Viagens")

# Entrada do usuário
ur = st.number_input("Digite o número de Unidades Residenciais (UR):", min_value=0.0, step=1.0)
pico = st.selectbox("Selecione a Hora-Pico:", ["Manhã", "Tarde"])

# Definir parâmetros com base no pico
if pico == "Manhã":
    coef, const = 0.7562, -35.147
    atracao_pct, producao_pct = 0.18, 0.82
    modais = {
        "Auto": 0.321,
        "Moto": 0.049,
        "Ônibus": 0.204,
        "A pé": 0.426
    }
else:
    coef, const = 0.7932, -22.36
    atracao_pct, producao_pct = 0.61, 0.39
    modais = {
        "Auto": 0.356,
        "Moto": 0.053,
        "Ônibus": 0.151,
        "A pé": 0.44
    }

# Cálculo de viagens
viagens = coef * ur + const

if ur > 0:
    st.subheader("📈 Resultados")
    st.write(f"**Total de viagens no pico da {pico.lower()}**: {viagens:.2f}")

    atracao = viagens * atracao_pct
    producao = viagens * producao_pct

    st.write(f"**Atração**: {atracao:.2f} viagens ({atracao_pct*100:.0f}%)")
    st.write(f"**Produção**: {producao:.2f} viagens ({producao_pct*100:.0f}%)")

    st.markdown("### 🚲 Divisão Modal")
    for modo, pct in modais.items():
        qtd = viagens * pct
        st.write(f"- {modo}: {qtd:.2f} viagens ({pct*100:.1f}%)")
else:
    st.info("Insira um valor de UR maior que 0.")
