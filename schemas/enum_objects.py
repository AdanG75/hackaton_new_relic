from enum import Enum


class Riesgo(Enum):
    alto = "Alto"
    medio = "Medio"
    bajo = "Bajo"


class EstadoFuego(Enum):
    activo = "Activo"
    apagando = "Apagando"
    apagado = "Apagado"
