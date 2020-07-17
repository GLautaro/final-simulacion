# Importacion de paginas
import Paginas.Principal as principal
import Paginas.Simulacion as simulacion

# Importacion de modulos de terceros
import streamlit as st


def CreateLayout():
    st.sidebar.title("Menú")
    app_mode = st.sidebar.selectbox("Seleccione una página:",
                                    ["Introducción", "Simular"])

    if app_mode == 'Introducción':
        principal.LoadPage()
    else:
        simulacion.LoadPage()


if __name__ == "__main__":
    CreateLayout()