#Archivo utilizado para definir las constantes utilizadas a lo largo de toda la aplicacion
#Se plantea para mejorar la legibilidad de codigo

from enum import Enum

class EstadoCliente(Enum):
    EN_COLA_TICKET = "EN_COLA_TICKET"
    ESPERANDO_TICKET = "ESPERANDO_TICKET"
    EN_COLA_ENTREGA = "EN_COLA_ENTREGA"
    ESPERANDO_ENTREGA = "ESPERANDO_ENTREGA"
    OCUPANDO_MESA = "OCUPANDO_MESA"
    FINALIZADO = "FINALIZADO"

class EstadoDueño(Enum):
    LIBRE = "LIBRE"
    OCUPADO = "OCUPADO"

class EstadoEmpleados(Enum):
    LIBRE = "LIBRE"
    OCUPADO = "OCUPADO"

class EstadoMesas(Enum):
    LIBRE = "LIBRE"
    OCUPADO = "OCUPADO"

class DecisionMontecarlo(Enum):
    COMPRA = "COMPRA"
    DE_PASO = "DE PASO"
    MESA = "MESA"

