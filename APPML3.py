import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

try:
    # Configuração da página
    st.set_page_config(
        page_title="Previsão de Preço de Pizza",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # Carregamento dos dados
    @st.cache_data(show_spinner=False)
    def load_data():
        try:
            return pd.read_csv("pizzas.csv")
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
            return None

    # Carrega os dados e treina o modelo
    df = load_data()
    if df is not None:
        modelo = LinearRegression()
        X = df[["diametro"]]
        y = df[["preço"]]
        modelo.fit(X, y)

        # Interface do usuário
        st.header("🍕 Calculadora de Preço de Pizza")
        st.write("Digite o tamanho do diâmetro da pizza para calcular o preço")

        col1, col2 = st.columns([3, 1])
        with col1:
            diametro = st.slider(
                "Diâmetro da pizza (cm)",
                min_value=0.0,
                max_value=100.0,
                value=30.0,
                step=1.0
            )

        with col2:
            if st.button("Calcular", use_container_width=True):
                if diametro > 0:
                    try:
                        input_data = pd.DataFrame({"diametro": [diametro]})
                        preco_previsto = modelo.predict(input_data)[0][0]
                        st.info(f"💰 Preço estimado: R$ {preco_previsto:.2f}")
                    except Exception as e:
                        st.error(f"Erro ao calcular preço: {e}")
                else:
                    st.warning("Digite um valor válido maior que zero.")

except Exception as e:
    st.error(f"Ocorreu um erro inesperado: {e}")
    
