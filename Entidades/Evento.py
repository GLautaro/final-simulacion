from Modulos.Utils import Truncate
from Modulos.TablasProbabilidad import CalcularDecisionCliente
import random

class Evento:
    def __init__(self, duracion, hora, nombre, id):
        self.duracion = duracion
        self.hora = hora
        self.nombre = nombre
        self.id = id

    def __gt__(self, evento):
        return self.hora > evento.hora

    def __lt__(self, evento):
        return self.hora < evento.hora


class Inicializacion(Evento):
    def __init__(self):
        super().__init__(None, 0, "Inicialización", 0)


class FinSimulacion(Evento):
    def __init__(self, horaFin):
        super().__init__(None, horaFin, "Fin Simulacion", 0)


##Puede ir aca el montecarlo???
class LlegadaCliente(Evento):
    def __init__(self, reloj, media, desviacion, probabilidades, id):
        duracion = Truncate(random.gauss(media, desviacion), 2)
        hora = Truncate((reloj + duracion), 2)
        nombre = "Llegada Cliente " + str(id)
        super().__init__(duracion, hora, nombre, id)
        rnd_decision = Truncate(random.uniform(0, 1.00001), 2)
        self.rnd_decision = rnd_decision
        self.decision_cliente = CalcularDecisionCliente(probabilidades, rnd_decision)



class FinCompraTicket(Evento):
    def __init__(self, reloj, duracion, cliente, id):
        hora = Truncate((reloj + duracion), 2)
        nombre = "Fin Compra Ticket " + str(id)
        super().__init__(duracion, hora, nombre, id)
        self.cliente = cliente


class FinEntregaPedido(Evento):
    def __init__(self, reloj, media, empleado, id):
        duracion =  0 if media == 0 else Truncate(random.expovariate(1 / media), 2)
        hora = Truncate((reloj + duracion), 2)
        nombre = "Fin Entrega Pedido " + str(id)
        super().__init__(duracion, hora, nombre, id)
        self.empleado = empleado


class FinUsoMesa(Evento):
    def __init__(self, reloj, mesa, a_unif, b_unif, id):
        duracion = Truncate(random.uniform(a_unif, b_unif), 2)
        hora = Truncate((reloj + duracion), 2)
        nombre = "Fin Uso Mesa " + str(id)
        super().__init__(duracion, hora, nombre, id)
        self.mesa = mesa

        