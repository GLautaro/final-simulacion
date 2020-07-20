from Modulos.Constantes import EstadoCliente as EC

class Cliente:
    def __init__(self, id, estado, tiempo_llegada):
        self.id = id
        self.estado = estado
        self.tiempo_llegada = tiempo_llegada
        self.mesa = None
        self.empleado = None

    def __eq__(self, cliente):
        return self.id == cliente.id
    
    ##Probablemente hay que agregar el tiempo llegada
    def completarColumnas(self, df, nombre_col_estado, nombre_col_mesa, row):
        if nombre_col_estado in df.columns:
            df.at[row, nombre_col_estado] = self.estado.value
            df.at[row, nombre_col_mesa] = str(self.mesa.id_mesa) if self.mesa is not None else "*---------*"
        else:
            nones = [None for i in range(row)]
            df[nombre_col_estado] = nones + [self.estado.value]
            df[nombre_col_mesa] = nones + [str(self.mesa.id_mesa) if self.mesa is not None else "*---------*"]
        return df

    def agregarDF(self, df, row):
        nombre_col_estado = "Estado_cliente_" + str(self.id)
        nombre_col_mesa = "Mesa_cliente_" + str(self.id)
        return super().completarColumnas(df, nombre_col_estado, nombre_col_mesa, row)
    
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