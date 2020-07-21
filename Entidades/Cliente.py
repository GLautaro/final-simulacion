import random
from Modulos.TablasProbabilidad import CalcularDecisionCliente
from Modulos.Utils import Truncate
from Modulos.Constantes import EstadoCliente as EC

class Cliente:
    def __init__(self, id, estado, tiempo_llegada):
        self.id = id
        self.estado = estado
        self.tiempo_llegada = tiempo_llegada
        self.mesa = None
        self.empleado = None
        self.rnd_decision = None
        self.decision = None

    def __eq__(self, cliente):
        return self.id == cliente.id

    
    def completarColumnas(self, df, nombre_col_estado, nombre_col_mesa, nombre_col_tiempo_llegada, row):
        if nombre_col_estado in df.columns:
            df.at[row, nombre_col_estado] = self.estado.value
            df.at[row, nombre_col_mesa] = str(self.mesa.id_mesa) if self.mesa is not None else "*---------*"
            df.at[row, nombre_col_tiempo_llegada] = str(self.tiempo_llegada)
        else:
            nones = [None for i in range(row)]
            df[nombre_col_estado] = nones + [self.estado.value]
            df[nombre_col_mesa] = nones + [str(self.mesa.id_mesa) if self.mesa is not None else "*---------*"]
            df[nombre_col_tiempo_llegada] = nones + [str(self.tiempo_llegada)]
        return df

    def agregarDF(self, df, row):
        nombre_col_estado = "Estado_cliente_" + str(self.id)
        nombre_col_mesa = "Mesa_cliente_" + str(self.id)
        nombre_col_tiempo_llegada = "Tiempo_llegada_" + str(self.id)
        return self.completarColumnas(df, nombre_col_estado, nombre_col_mesa, nombre_col_tiempo_llegada, row)
    
    def calcularDecision(self, probabilidades):
        rnd_decision = Truncate(random.uniform(0, 1.00001), 2)
        self.rnd_decision = rnd_decision
        self.decision = CalcularDecisionCliente(probabilidades, rnd_decision)


    def enColaCompraTicket(self):
        self.estado = EC.EN_COLA_TICKET
    
    def esperandoTicket(self):
        self.estado = EC.ESPERANDO_TICKET
    
    def enColaEntregaPedido(self):
        self.estado = EC.EN_COLA_ENTREGA
    
    def esperandoEntregaPedido(self, empleado):
        self.estado = EC.ESPERANDO_ENTREGA
        self.empleado = empleado
        empleado.iniciarOcupamiento(self)
    
    def comenzarUsoMesa(self, mesa):
        self.estado = EC.OCUPANDO_MESA
        self.mesa = mesa
        mesa.comenzarOcupamiento(self)
    
    def finalizar(self):
        self.estado = EC.FINALIZADO
        if self.mesa is not None:
            self.mesa.finalizarOcupamiento()
            self.mesa = None