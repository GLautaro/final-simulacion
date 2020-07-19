from Modulos.Constantes import EstadoEmpleados as EE

class Empleado():
    def __init__(self, id):
        self.estado = EE.LIBRE
        self.id_empleado = id

    def __eq__(self, otro):
        if otro is None:
            return False
        if isinstance(otro, Empleado):
            return self.id_empleado == otro.id_empleado
        return False
    
    def estaLibre(self):
        return self.estado = EE.LIBRE
    
    def iniciarOcupamiento(self):
        self.estado = EE.OCUPADO
    
    def terminarOcupamiento(self):
        self.estado = EE.LIBRE