##Lib. Externas
import pandas as pd
##Lib. y modulos internos
from Modulos.Constantes import EstadoDueño as ED
from Modulos.Constantes import EstadoEmpleados as EE
from Modulos.Constantes import DecisionMontecarlo as DM
from Entidades.Mesa import Mesa
from Entidades.Cliente import Cliente
from Entidades.Empleado import Empleado
from Entidades.Evento import Inicializacion, FinSimulacion, LlegadaCliente, FinCompraTicket, FinEntregaPedido, FinUsoMesa
import Modulos.TablasProbabilidad as Prob
import Modulos.Utils as utils

class Controlador:
    def __init__(self, tiempo_simulacion, reloj, mostrar_desde, mostrar_cantidad, cant_mesas, 
                media_llegada, desv_llegada, probabilidades, tiempo_compra, media_entrega, a_mesa, b_mesa):
        
        self.tiempo_simulacion = tiempo_simulacion
        self.reloj = reloj
        self.mostrar_desde = mostrar_desde
        self.mostrar_cantidad = mostrar_cantidad
        self.mesas = []
        self.cant_mesas = cant_mesas
        for i in range(cant_mesas):
            self.mesas.append(Mesa(i))
        
        self.media_llegada = media_llegada
        self.desv_llegada = desv_llegada

        self.probabilidades = Prob.CrearProbabilidadesAcumuladas(probabilidades)

        self.tiempo_compra = tiempo_compra
        
        self.media_entrega = media_entrega

        self.a_mesa = a_mesa
        self.b_mesa = b_mesa
        
        self.cola_compra = []
        self.cola_pedidos = []

        self.contador_clientes = 1
        self.contador_clientes_fin = 0
        self.acum_tiempo_permanencia = 0

        self.dueño = ED.LIBRE
        self.empleado1 = Empleado(1)
        self.empleado2 = Empleado(2)
        self.eventos = []
        self.clientes = []
        self.vectorFinEntrega = [0, 0]
        self.vectorFinMesa = [0 for i in range(cant_mesas)]

        self.llegada_cliente = None
        self.fin_compra_ticket = None
        self.fin_entrega_pedido = None
        self.fin_uso_mesa = None


    def manejarInicializacion(self):
        '''
        Realiza la logica para manejar el evento de inicializacion
        '''
        self.llegada_cliente = LlegadaCliente(self.reloj, self.media_llegada, self.desv_llegada, self.probabilidades ,self.contador_clientes)
        if self.llegada_cliente.decision_cliente == DM.COMPRA:

        self.fin_compra_ticket = FinCompraTicket(0, 0, 0)
        self.fin_entrega_pedido = FinEntregaPedido(0, 0, 0, None)
        self.fin_uso_mesa = FinUsoMesa(0, None, 0, 0, 0)

        self.eventos.append(self.llegada_cliente)
    
    def manejarLlegadaCliente(self, evento_actual):
        self.contador_clientes += 1
        cliente = Cliente(evento_actual.id, "", self.reloj)
        self.clientes.append(cliente)

        prox_llegada_cliente = LlegadaCliente(self.reloj, self.media_llegada, 
                                self.desv_llegada, self.probabilidades, self.contador_clientes)
        self.eventos.append(prox_llegada_cliente)
        self.llegada_cliente = prox_llegada_cliente
        
        #Analizar lo que pasa con la decision del cliente
        if evento_actual.decision_cliente == DM.COMPRA:
            if len(self.cola_compra) == 0:
                fin_compra = FinCompraTicket(self.reloj, self.tiempo_compra, cliente.id)
                self.eventos.append(fin_compra)
                self.fin_compra_ticket = fin_compra
                cliente.esperandoTicket()
            else:
                self.cola_compra.append(cliente)
                cliente.enColaCompraTicket()
        
        elif evento_actual.decision_cliente == DM.MESA:
            mesa_libre = self.buscarMesaLibre()
            if mesa_libre is not None:
                fin_uso_mesa = FinUsoMesa(self.reloj, mesa_libre, self.a_mesa, self.b_mesa, cliente.id)
                self.eventos.append(fin_uso_mesa)
                self.fin_uso_mesa = fin_uso_mesa
                self.vectorFinMesa[cliente.id - 1] = fin_uso_mesa.hora
                cliente.comenzarUsoMesa(mesa_libre)
            else:
                cliente.finalizar()

        else:
            cliente.finalizar()

    def manejarFinCompraTicket(self, evento_actual):
        pass

    def crearVectorEstado(self, evento_actual):
        '''
        La función recibe como parámetro el evento actual de la iteración y 
        retorna el vector de estado correspondiente.
        '''
        eventos = [
            "Evento Actual: " + str(evento_actual.nombre),
            "Reloj: " + str(self.reloj),
            "Tiempo entre llegadas Cliente: " + str(self.llegada_cliente.duracion),
            "Próxima llegada Cliente: " + str(self.llegada_cliente.hora),
            "RND Decision: " + str(self.llegada_cliente.rnd_decision),
            "Decision Cliente: " + str(self.llegada_cliente.decision_cliente),
            "Tiempo Compra Ticket: " + str(self.fin_compra_ticket.duracion),
            "Fin Compra Ticket: " + str(self.fin_compra_ticket.hora),
            "Tiempo entrega pedido: " + str(self.fin_entrega_pedido.duracion),
            "Fin Entrega Pedido Emp. 1: " + str(self.vectorFinEntrega[0]),
            "Fin Entrega Pedido Emp. 2: " + str(self.vectorFinEntrega[1]),
            "Tiempo Uso Mesa: " + str(self.fin_uso_mesa.duracion)
        ]


        for i in range(self.cant_mesas):
            eventos.append("".join(["Fin uso Mesa ", str(i+1), " : ", self.vectorFinMesa[i]]))
        
        compra_ticket = [
            "Cola Compra: " + str(len(self.cola_compra)),
            "Estado Dueño (Compra Ticket): " + str(self.dueño),
        ]

        empleados = [
            "Cola entrega pedidos: " + str(len(self.cola_pedidos)),
            "Estado "
        ]

        mesas_estado = []
        for i in range(self.cant_mesas):
            mesas_estado.append("".join(["Estado mesa ", str(i+1), " : ", self.mesas[i].estado]))
        
        fin_list = [
            "Cantidad Clientes Finalizados: " + str(self.contador_clientes_fin),
            "Acumulador tiempo permanencia: " + str(self.acum_tiempo_permanencia)
        ]

        for cli in self.clientes:
            fin_list.append("Cliente ID: " + str(cli.id))
            fin_list.append("Estado: " + str(cli.estado))
            fin_list.append("Reloj Llegada: " + str(cli.tiempo_llegada))
            mesa = cli.mesa
            if mesa is None:
                fin_list.append("-")
            else:
                fin_list.append("Usando Mesa " + str(mesa.id_mesa)) }
        
        return eventos + compra_ticket + empleados + mesas_estado + fin_list

    def buscarMesaLibre(self):
        libres = list(filter(lambda mesa: mesa.esta_libre(), self.mesas))
        return None if len(libres) == 0 else libres[0]

    def simular(self):
        df_datos_fijos = pd.DataFrame(columns=utils.crearColumnasParcialesDataFrame(self.cant_mesas))

        df_clientes = pd.DataFrame()

        inicializacion = Inicializacion()
        fin_simulacion = FinSimulacion(self.tiempo_simulacion)

        self.eventos.append(inicializacion)
        self.eventos.append(fin_simulacion)

        cantidad_iteraciones_mostradas = 0
        i = 0

        while self.reloj <= self.tiempo_simulacion:
            i += 1
            evento_actual = min(self.eventos, key=lambda x: x.hora)
            self.eventos.remove(evento_actual) #Quita el elemento para procesar el evento

            if isinstance(evento_actual, FinSimulacion):
                break

            if isinstance(evento_actual, Inicializacion):
                self.manejarInicializacion()

            if isinstance(evento_actual, LlegadaCliente):
                self.manejarLlegadaCliente(evento_actual)
            
            elif isinstance(evento_actual, FinCompraTicket):
                self.manejarFinCompraTicket(evento_actual)

            #Vector estado (experimental-only)
            vectorEstado = self.crearVectorEstado(evento_actual)
            print(vectorEstado)

            if (self.reloj >= self.mostrar_desde and 
                cantidad_iteraciones_mostradas < self.mostrar_cantidad and
                cantidad_iteraciones_mostradas <= i):

                #df_datos_fijos, df_clientes = self.agregarDatos()
                cantidad_iteraciones_mostradas += 1
            
            #Incremento de reloj
            self.reloj = min(self.eventos).hora
            self.reloj = utils.Truncate(self.reloj, 2)

        return df_datos_fijos