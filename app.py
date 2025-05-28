import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Calculadora de Geração de Viagens", layout="wide")

# Logomarca esquerda
st.image("logomarca.png", width=300)

# Ajuste textos
st.markdown("""
    <style>
        h1, h2, h3 {
            font-size: 130% !important;
        }
        .stMetric {
            font-size: 1.2em !important;
        }
        .stDataFrame, .stMarkdown p {
            font-size: 1.2em !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Calculadora de Geração de Viagens Condominios Residenciais")

# Estilo customizado
st.markdown("""
    <style>
    html, body, [class*="css"] {
        background-color: #f3f5f7;
        color: #1a1a1a;
    }
    .stNumberInput>div>div>input {
        width: 80px;
        font-size: 1.2em;
    }
    .stRadio>div {
        display: flex;
        gap: 10px;
        flex-direction: row;
    }
    .stButton>button {
        background-color: #003865;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        height: 3em;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Modelos
modelos = {
    "OLIVEIRA (2015)": {
        "manha": {"coef": 0.7562, "const": -35.147, "atracao": 0.18, "producao": 0.82,
                  "modais": {"Auto": 0.321, "Moto": 0.049, "Ônibus": 0.204, "A pé": 0.426}},
        "tarde": {"coef": 0.7932, "const": -22.36, "atracao": 0.61, "producao": 0.39,
                  "modais": {"Auto": 0.356, "Moto": 0.053, "Ônibus": 0.151, "A pé": 0.44}}
    },
    "BHTRANS (2015)": {
        "manha": {"coef": 0.74, "const": 0, "atracao": 0.1, "producao": 0.9,
                  "modais": {"Auto": 0.321, "Moto": 0.049, "Ônibus": 0.204, "A pé": 0.426}},
        "tarde": {"coef": 0.4601, "const": 0, "atracao": 0.7, "producao": 0.3,
                  "modais": {"Auto": 0.356, "Moto": 0.053, "Ônibus": 0.151, "A pé": 0.44}}
    },
    "FERREIRA (2013)": {
        "manha": {"coef": 0.3627, "const": 165.2988, "atracao": 0.18, "producao": 0.82,
                  "modais": {"Auto": 0.4, "Moto": 0.12, "Ônibus": 0.04, "A pé": 0.44}},
        "tarde": {"coef": 0.3627, "const": 165.2988, "atracao": 0.61, "producao": 0.39,
                  "modais": {"Auto": 0.4, "Moto": 0.12, "Ônibus": 0.04, "A pé": 0.44}}
    }
}

# Entradas do usuário
col1, col2 = st.columns(2)
with col1:
    ur = st.number_input("URs:", min_value=0, step=1, format="%d")
with col2:
    pico = st.radio("Hora-Pico:", ["Manhã", "Tarde"], horizontal=True)

pico_key = "manha" if pico == "Manhã" else "tarde"

# Mostrar resultados
if ur > 0:
    col_result, col_img = st.columns([2, 1])
    with col_result:
        st.markdown("---")
        st.header(f"Resultados para {ur} UR na Hora-Pico da {pico}")
        resultados_gerais = []

        for nome_modelo, modelo in modelos.items():
            st.subheader(f"Modelo: {nome_modelo}")
            if pico_key in modelo:
                params = modelo[pico_key]
                total_viagens = max(0, round(params["coef"] * ur + params["const"]))
                atracao_viagens = round(total_viagens * params["atracao"])
                producao_viagens = round(total_viagens * params["producao"])

                col_res1, col_res2, col_res3 = st.columns(3)
                with col_res1:
                    st.metric(label="Total de Viagens Geradas", value=f"{total_viagens}")
                with col_res2:
                    st.metric(label="Viagens Atraídas", value=f"{atracao_viagens} ({params['atracao']:.1%})")
                with col_res3:
                    st.metric(label="Viagens Produzidas", value=f"{producao_viagens} ({params['producao']:.1%})")

                st.write("**Divisão Modal Estimada:**")
                modais_data = []
                for modal, percentual in params["modais"].items():
                    viagens_modal = round(total_viagens * percentual)
                    modais_data.append({"Modo": modal, "Viagens": viagens_modal, "Percentual": f"{percentual:.1%}"})
                df_modais = pd.DataFrame(modais_data)
                st.dataframe(df_modais.set_index('Modo'), use_container_width=True)

                resultados_gerais.append({
                    "Modelo": nome_modelo,
                    "Total Viagens": total_viagens,
                    "Atração": atracao_viagens,
                    "Produção": producao_viagens,
                    "Auto": round(total_viagens * params["modais"]["Auto"]),
                    "Moto": round(total_viagens * params["modais"]["Moto"]),
                    "Ônibus": round(total_viagens * params["modais"]["Ônibus"]),
                    "A pé": round(total_viagens * params["modais"]["A pé"])
                })

        if resultados_gerais:
            st.markdown("---")
            st.header("Resumo Comparativo dos Modelos")
            df_resumo = pd.DataFrame(resultados_gerais)
            st.dataframe(df_resumo.set_index('Modelo'), use_container_width=True)
    with col_img:
        st.image("condominio.png", use_container_width=True)
else:
    st.info("Por favor, insira um número de Unidades Residenciais (UR) maior que zero para calcular.")

st.markdown("""
---

📚 **Referência Bibliográfica Principal**  
Oliveira, P., Rodrigues, F. (2015, junho). *Calibração de modelo de geração de viagens para condomínios de edifícios residenciais*. In Anais 20º Congresso Brasileiro de Transporte e Trânsito, Santos, SP.

👨‍💻 **Desenvolvido por [Wagner Jales](http://www.wagnerjales.com.br)**
""")
