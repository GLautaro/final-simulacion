from Modulos.Constantes import EstadoMesas as EM

class Mesa:
    def __init__(self, id_mesa):
        self.id_mesa = id_mesa
        self.estado = EM.LIBRE
        self.cliente = None
    
    def __eq__(self, otro):
        if otro is None:
            return False
        if isinstance(otro, Mesa):
            return self.id_mesa == otro.id_mesa
        return False
    
    def comenzarOcupamiento(self, cliente):
        self.cliente = cliente
        self.estado = EM.OCUPADO
    
    def finalizarOcupamiento(self):
        self.cliente = None
        self.estado = EM.LIBRE
    
    def esta_libre(self):
        return self.estado == EM.LIBRE

