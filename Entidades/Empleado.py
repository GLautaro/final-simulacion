from Modulos.Constantes import EstadoEmpleados as EE

class Empleado():
    def __init__(self, id):
        self.estado = EE.LIBRE
        self.id_empleado = id
        self.cliente = None

    def __eq__(self, otro):
        if otro is None:
            return False
        if isinstance(otro, Empleado):
            return self.id_empleado == otro.id_empleado
        return False
    
    def estaLibre(self):
        return self.estado == EE.LIBRE
    
    def iniciarOcupamiento(self, cliente):
        self.estado = EE.OCUPADO
        self.cliente = cliente
    
    def terminarOcupamiento(self):
        self.estado = EE.LIBRE