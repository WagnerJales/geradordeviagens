import streamlit as st
from PIL import Image

st.set_page_config(page_title="Calculadora de Geração de Viagens", layout="wide")

# Logomarca no topo
logomarca = Image.open("logomarca.png")
st.image(logomarca, width=200)

st.title("🚦 Calculadora de Geração de Viagens para Edifícios residenciais de classe média")

# Modelos disponíveis
modelos = {
    "Modelo OLIVEIRA (2015)": {
        "manha": {"coef": 0.7562, "const": -35.147, "atracao": 0.18, "producao": 0.82,
                  "modais": {"Auto": 0.321, "Moto": 0.049, "Ônibus": 0.204, "A pé": 0.426}},
        "tarde": {"coef": 0.7932, "const": -22.36, "atracao": 0.61, "producao": 0.39,
                  "modais": {"Auto": 0.356, "Moto": 0.053, "Ônibus": 0.151, "A pé": 0.44}}
    },
    "Modelo BHTRANS (2017)": {
        "manha": {"coef": 0.74, "const": 0, "atracao": 0.10, "producao": 0.90,
                  "modais": {"Auto": 0.321, "Moto": 0.049, "Ônibus": 0.204, "A pé": 0.426}},
        "tarde": {"coef": 0.4601, "const": 0, "atracao": 0.70, "producao": 0.30,
                  "modais": {"Auto": 0.356, "Moto": 0.053, "Ônibus": 0.151, "A pé": 0.44}}
    },
    "Modelo FERREIRA (2013)": {
        "manha": {"coef": 0.3627, "const": 165.2988, "atracao": 0.18, "producao": 0.82,
                  "modais": {"Auto": 0.40, "Moto": 0.12, "Ônibus": 0.040, "A pé": 0.44}},
        "tarde": {"coef": 0.3627, "const": 165.2988, "atracao": 0.61, "producao": 0.39,
                  "modais": {"Auto": 0.40, "Moto": 0.12, "Ônibus": 0.040, "A pé": 0.44}}
    }
}

# Estilo personalizado
st.markdown("""
    <style>
        h1, h2, h3 {
            font-size: 1.3em !important;
        }
        .css-1cpxqw2, .css-ffhzg2 {
            font-size: 130% !important;
        }
        td, th {
            font-size: 1.1rem !important;
        }
        input[type="number"], .stNumberInput input {
            height: 3em !important;
            font-size: 1.3em !important;
        }
        div[data-baseweb="select"] {
            height: 3em !important;
            font-size: 1.2em !important;
        }
    </style>
""", unsafe_allow_html=True)

# Entradas do usuário
col1, col2 = st.columns(2)
with col1:
    ur = st.number_input("Digite o número de Unidades Residenciais (UR):", min_value=0, step=1, format="%d")
with col2:
    pico = st.selectbox("Selecione a Hora-Pico:", ["Manhã", "Tarde"])

# Mostrar resultados para todos os modelos
if ur > 0:
    col1, col2 = st.columns([2, 1])
    with col1:
        for nome_modelo, modelo in modelos.items():
            st.markdown(f"### 📘 {nome_modelo}")

            key = "manha" if pico == "Manhã" else "tarde"
            param = modelo[key]
            coef, const = param["coef"], param["const"]
            atracao_pct, producao_pct = param["atracao"], param["producao"]
            modais = param["modais"]

            viagens = int(round(coef * ur + const))
            atracao = int(round(viagens * atracao_pct))
            producao = int(round(viagens * producao_pct))

            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Total de viagens no pico da {pico.lower()}**: {viagens:,d}")
                st.write(f"**Atração**: {atracao:,d} viagens ({atracao_pct*100:.0f}%)")
                st.write(f"**Produção**: {producao:,d} viagens ({producao_pct*100:.0f}%)")
            with c2:
                st.write("**🚲 Divisão Modal**")
                for modo, pct in modais.items():
                    qtd = int(round(viagens * pct))
                    st.write(f"- {modo}: {qtd:,d} viagens ({pct*100:.1f}%)")
    with col2:
        imagem = Image.open("condominio.png")
        st.image(imagem, use_column_width=True)

# Rodapé
st.markdown("""
---

📚 **Referência Bibliográfica**  
Oliveira, P., Rodrigues, F. (2015, junho). *Calibração de modelo de geração de viagens para condomínios de edifícios residenciais*.  
In Anais 20º Congresso Brasileiro de Transporte e Trânsito, Santos, SP.

👨‍💻 **Adaptado por [Wagner Jales](http://www.wagnerjales.com.br)**
""")
