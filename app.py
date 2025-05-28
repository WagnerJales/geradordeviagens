import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Geração de Viagens", layout="wide")

st.title("🚦 Calculadora de Geração de Viagens Condominios Residenciais")

# Modelos disponíveis
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
    ur = st.number_input("Digite o número de Unidades Residenciais (UR):", min_value=0, step=1, format="%d")
with col2:
    pico = st.selectbox("Selecione a Hora-Pico:", ["Manhã", "Tarde"])

# Mapear seleção do pico para chave do dicionário
pico_key = "manha" if pico == "Manhã" else "tarde"

# Mostrar resultados para todos os modelos
if ur > 0:
    st.markdown("---")
    st.header(f"Resultados para {ur} UR na Hora-Pico da {pico}")

    resultados_gerais = []

    for nome_modelo, modelo in modelos.items():
        st.subheader(f"Modelo: {nome_modelo}")

        # Verificar se o pico selecionado existe no modelo
        if pico_key in modelo:
            params = modelo[pico_key]
            
            # Calcular viagens totais
            total_viagens = params["coef"] * ur + params["const"]
            total_viagens = max(0, round(total_viagens)) # Garantir que não seja negativo e arredondar

            # Calcular atração e produção
            atracao_viagens = round(total_viagens * params["atracao"])
            producao_viagens = round(total_viagens * params["producao"])

            # Exibir resultados principais
            col_res1, col_res2, col_res3 = st.columns(3)
            with col_res1:
                st.metric(label="Total de Viagens Geradas", value=f"{total_viagens}")
            with col_res2:
                st.metric(label="Viagens Atraídas", value=f"{atracao_viagens} ({params['atracao']:.1%})")
            with col_res3:
                st.metric(label="Viagens Produzidas", value=f"{producao_viagens} ({params['producao']:.1%})")

            # Calcular e exibir divisão modal
            st.write("**Divisão Modal Estimada:**")
            modais_data = []
            for modal, percentual in params["modais"].items():
                viagens_modal = round(total_viagens * percentual)
                modais_data.append({"Modo": modal, "Viagens": viagens_modal, "Percentual": f"{percentual:.1%}"})
            
            df_modais = pd.DataFrame(modais_data)
            st.dataframe(df_modais.set_index('Modo'), use_container_width=True)

            # Adicionar aos resultados gerais para o resumo
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

        else:
            st.warning(f"Dados para a hora-pico '{pico}' não disponíveis para o modelo {nome_modelo}.")
        st.markdown("&nbsp;") # Adiciona um espaço

    # Tabela Resumo Comparativa
    if resultados_gerais:
        st.markdown("---")
        st.header("Resumo Comparativo dos Modelos")
        df_resumo = pd.DataFrame(resultados_gerais)
        st.dataframe(df_resumo.set_index('Modelo'), use_container_width=True)

else:
    st.info("Por favor, insira um número de Unidades Residenciais (UR) maior que zero para calcular.")

st.markdown("""
---

📚 **Referência Bibliográfica Principal**  
Oliveira, P., Rodrigues, F. (2015, junho). *Calibração de modelo de geração de viagens para condomínios de edifícios residenciais*. In Anais 20º Congresso Brasileiro de Transporte e   Trânsito, Santos, SP.

👨‍💻 **Desenvolvido por [Wagner Jales](http://www.wagnerjales.com.br)**
""")
