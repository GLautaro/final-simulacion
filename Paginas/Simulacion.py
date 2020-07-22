import streamlit as st
import os

from Soporte.ControladorSimuladorColas import Controlador
import Modulos.Utils as utils

def LoadPage():
    st.title('Cafeteria UTN')
    st.markdown('Ingrese los parametros solicitados y luego presione "Iniciar Simulacion".')

    # Parametros de la simulacion y visualizacion
    st.header('🔧Parametros de simulación.')
    tiempo = st.number_input('Tiempo a simular (minutos - max. 120)', min_value=0.0, value=120.0, max_value=120.0)
    cant_iteraciones = st.number_input('Cantidad de iteraciones a mostrar', min_value=0, value=100, format='%d')
    min_iteraciones = st.number_input('Minutos desde la cual se muestran las iteraciones', min_value=0.0, value=0.0, max_value=tiempo)
    cantidad_mesas = st.number_input('Cantidad de mesas en la cafeteria', min_value=0, value=5, format='%d')

    # Parametros de llegada de clientes (distribucion Normal)
    st.header('🏃Parametros de llegada de Clientes.')
    st.markdown('Se solicitan los parametros correspondientes a una distribucion normal')
    media_demora = st.number_input('Media μ', min_value=0.0, value=10.0)
    desviacion_est_demora = st.number_input('Desviación estandar σ', min_value=0.0, value=6.0)

    
    # Parametros de decision del cliente (montecarlo)
    st.header('🔢Probabilidades en la decision del cliente.')
    st.markdown('Se solicitan los probabilidades correspondientes a las decisiones que puede tomar una persona en la cafeteria.')
    prob_compra = st.number_input('Probabilidad de que entre a comprar(%):', min_value=0.0, max_value=100.0,
                                value=60.0, step=1.0)
    prob_mesa = st.number_input('Probabilidad de que solo utilice una mesa(%):', min_value=0.0, max_value=100.0,
                                value=30.0, step=1.0)
    prob_de_paso = st.number_input('Probabilidad de que solo este de paso(%):', min_value=0.0, max_value=100.0,
                                value=10.0, step=1.0)

    # Parametros de tiempo de compra de ticket
    st.header('🎫Parametros de compra de ticket.')
    tiempo_compra = st.number_input('Tiempo de compra de ticket (segundos)', min_value=0, value=20, format='%d')

    # Parametros de tiempo de entrega de pedido
    st.header('☕Parametros de entrega de pedido')
    st.markdown('Se solicitan los parametros correspondientes a una distribucion exponencial negativa')
    exp_neg_media = st.number_input('Media μ:', min_value=0.0, value=5.0)

    # Parametros de consumicion de pedido
    st.header('🍴Parametros de consumicion de pedido (Uso de mesa).')
    st.markdown('Se solicitan los parametros correspondientes a una distribucion uniforme (A-B)')
    a_uniforme = st.number_input('A:', value=4, format='%d')
    b_uniforme = st.number_input('B:', value=6, format='%d')

    # -----------------------
    # Fin seccion parametros
    # -----------------------

    simulacion_ok = st.button('Iniciar simulación')
    if simulacion_ok:
        tiempo_compra = utils.Truncate((tiempo_compra / 60), 2)
        controlador = Controlador(tiempo, 0, min_iteraciones, cant_iteraciones, cantidad_mesas, media_demora, desviacion_est_demora, [prob_compra, prob_mesa, prob_de_paso], tiempo_compra, exp_neg_media, a_uniforme, b_uniforme)
        df, resultados = controlador.simular()

        st.write(df["Simulacion"])

        st.title("⭐Resultados de la simulacion")
        st.write("Cantidad de personas totales: " + str(resultados[0]))
        st.write("Cantidad de personas con atencion finalizada: " + str(resultados[1]))
        st.write("Tiempo Acumulado de permanencia en la cafeteria (Minutos): " + str(utils.Truncate(resultados[2], 2)))
        st.subheader("Promedio de permanencia de las personas en la cafeteria (Minutos): " + str(utils.Truncate(resultados[2] / resultados[1], 2)))
        
        #os.system("taskkill /F /IM excel.exe")
        nombre = "tpfinal.xlsx"
        try:
            utils.GenerarExcel(df, nombre)
            os.startfile(nombre)
        except Exception as err:
            st.error("Ups! Ocurrió un error, intente cerrar el archivo Excel antes de simular. Error: " + str(err))

        

