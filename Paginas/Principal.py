import streamlit as st

# The homepage is loaded using a combination of .write and .markdown.

def LoadPage():
    st.title('Presentacion Final - Ejercicio Cafeteria UTN')
    st.markdown('Simulación - Final 22 de Julio.')
    st.markdown('Lautaro Gonzalez - Legajo 75174')
    st.write('Se desarrollo esta aplicación que permite generar una simulación basada en un sistema multi-colas.')
    for i in range(2):
        st.write('')

    st.header('💬Sobre la Aplicación')
    st.write(
        'En el menú lateral usted podrá navegar las distintas funcionalidades de esta aplicación.')
    st.write(
        'Si selecciona "Simular" usted podra realizar la simulación y modificar los parametros de la misma')

    st.header('📝Ejercicio 43: Cafeteria UTN.')
    st.write("A la cafetería de la UTN entran personas con una distribución N(10’,6’) entre las 18:00 y las 20:00. El " + 
            "60% entra para comprar algo, el 30 % viene a utilizar las mesas y el resto solamente esta de paso. " + 
            'Para poder comprar deben comprar un ticket en la única caja de la cafetería, la que está atendida ' +
            'por el dueño. Una vez que retiran el ticket, se dirigen hacia el costado izquierdo de la caja donde 2 ' + 
            'empleados hacen la entrega de lo que figura en el ticket. Las personas que compran y quieren ' + 
            'quedarse, lo hacen si hay mesa libre, sino se van y se retiran una vez que terminan de consumir lo que compraron.')
    st.write('⏺ Tiempo de compra de ticket: 20 segundos.')
    st.write('⏺ Tiempo de entrega de pedido: exp(-)(50”)')
    st.write('⏺ Tiempo de consumición de pedido: 5 +- 1 minutos ')
    st.write('⭕ Plantear una fórmula (cuyos datos se extraerían de vector de estado) para establecer el promedio de permanencia de las personas en la cafetería.')
    st.header('Analisis y planteo')
    st.write('El flujo de eventos se corresponde con el siguiente diagrama')
    st.image('diagrama.png', caption='Diagrama de flujo Cafeteria' ,use_column_width=True)
    st.subheader('Objetos')
    st.write('⏺ Cliente (Objeto Temporal) Estados:  En Cola Ticket, Esperando Ticket, En cola Entrega, Esperando Entrega, Ocupando mesa, Finalizado')
    st.write('⏺ Dueño (Objeto Permanente) Estados:  Libre, Ocupado')
    st.write('⏺ Empleado (i) (Objeto Permanente) Estados:  Libre, Ocupado')
    st.write('⏺ Mesa (i) (Objeto Permanente) Estados:  Libre, Ocupado')
    st.subheader('Eventos')
    st.write('⭕Llegada cliente: Distribución Normal')
    st.write('⭕Fin Compra Ticket: Tiempo constante')
    st.write('⭕Fin Entrega Pedido (i): Distribución Exponencial Negativa')
    st.write('⭕Fin Uso Mesa (i): Distribución Uniforme (A-B)')
    st.success('Para resolver la consigna, se acumulara el tiempo de permanencia de los clientes y se contaran los clientes que finalizan. Encontraremos el promedio de permanencia dividiento dichas variables')


