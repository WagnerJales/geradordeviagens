if ur > 0:
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

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Total de viagens**: {viagens}")
            st.write(f"**Atração**: {atracao} viagens")
            st.write(f"**Produção**: {producao} viagens")
        with col2:
            st.write("**🚲 Divisão Modal**")
            for modo, pct in modais.items():
                qtd = int(round(viagens * pct))
                st.write(f"- {modo}: {qtd} viagens ({pct*100:.1f}%)")

# Rodapé fora do if
st.markdown(\"""
---

📚 **Referência Bibliográfica**  
Oliveira, P., Rodrigues, F. (2015, junho). *Calibração de modelo de geração de viagens para  
condomínios de edifícios residenciais*. In Anais 20º Congresso Brasileiro de Transporte e  
Trânsito, Santos, SP.

👨‍💻 **Desenvolvido por [Wagner Jales](http://www.wagnerjales.com.br)**
\""")
