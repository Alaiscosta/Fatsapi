from pydantic import BaseModel
from typing import List, Optional  # Asegúrate de importar Optional

class Desarrollador(BaseModel):
    id: int               # Identificador único del desarrollador
    nombre: str           # Nombre de la compañía desarrolladora
    pais: str             # País de origen de la compañía
    fundacion: int        # Año de fundación de la compañía

class Plataforma(BaseModel):
    id: int               # Identificador único de la plataforma
    nombre: str           # Nombre comercial de la plataforma
    fabricante: str       # Compañía que fabrica la plataforma
    lanzamiento: int      # Año de lanzamiento de la plataforma

class Juego(BaseModel):
    id: int                     # Identificador único del juego
    titulo: str                 # Título del juego
    genero: str                 # Género principal del juego
    año_lanzamiento: int        # Año de lanzamiento del juego
    desarrollador_id: int       # ID del desarrollador (relación)
    plataformas: List[int]      # Lista de IDs de plataformas disponibles