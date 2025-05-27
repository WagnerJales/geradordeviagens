import streamlit as st

st.set_page_config(page_title="Calculadora de Geração de Viagens", layout="wide")

st.title("🚦 Calculadora de Geração de Viagens")

# Modelos disponíveis
modelos = {
    "Padrão (Oliveira & Rodrigues, 2015)": {
        "manha": {"coef": 0.7562, "const": -35.147, "atracao": 0.18, "producao": 0.82,
                  "modais": {"Auto": 0.321, "Moto": 0.049, "Ônibus": 0.204, "A pé": 0.426}},
        "tarde": {"coef": 0.7932, "const": -22.36, "atracao": 0.61, "producao": 0.39,
                  "modais": {"Auto": 0.356, "Moto": 0.053, "Ônibus": 0.151, "A pé": 0.44}}
    },
    "Residencial (Betim-MG) – ImTraff (2015)": {
        "manha": {"coef": 0.74, "const": 0, "atracao": 0.18, "producao": 0.82,
                  "modais": {"Auto": 0.321, "Moto": 0.049, "Ônibus": 0.204, "A pé": 0.426}},
        "tarde": {"coef": 0.4601, "const": 0, "atracao": 0.61, "producao": 0.39,
                  "modais": {"Auto": 0.356, "Moto": 0.053, "Ônibus": 0.151, "A pé": 0.44}}
    },
    "Residencial (Vitória-ES) – ANTP (2015)": {
        "manha": {"coef": 0.3627, "const": 165.2988, "atracao": 0.18, "producao": 0.82,
                  "modais": {"Auto": 0.321, "Moto": 0.049, "Ônibus": 0.204, "A pé": 0.426}},
        "tarde": {"coef": 0.3627, "const": 165.2988, "atracao": 0.61, "producao": 0.39,
                  "modais": {"Auto": 0.356, "Moto": 0.053, "Ônibus": 0.151, "A pé": 0.44}}
    }
}

# Entradas do usuário
col1, col2 = st.columns(2)
with col1:
    ur = st.number_input("Digite o número de Unidades Residenciais (UR):", min_value=0, step=1, format="%d")
with col2:
    pico = st.selectbox("Selecione a Hora-Pico:", ["Manhã", "Tarde"])

# Mostrar resultados para todos os modelos
if ur > 0:
    for nome_modelo, modelo in modelos.items():
        
st.markdown("""
---

📚 **Referência Bibliográfica**  
Oliveira, P., Rodrigues, F. (2015, junho). *Calibração de modelo de geração de viagens para  
condomínios de edifícios residenciais*. In Anais 20º Congresso Brasileiro de Transporte e  
Trânsito, Santos, SP.

👨‍💻 **Desenvolvido por [Wagner Jales](http://www.wagnerjales.com.br)**
""")
