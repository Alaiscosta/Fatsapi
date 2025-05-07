from fastapi import FastAPI, HTTPException
from models import Desarrollador, Plataforma, Juego
from gestor_archivos import GestorArchivos
from typing import List , Optional

app = FastAPI(
    title="API de Videojuegos",
    description="API para gestionar información sobre videojuegos, plataformas y desarrolladores",
    version="1.0.0"
)

# Inicializar gestores de archivos
gestor_desarrolladores = GestorArchivos(Desarrollador, "desarrolladores.json")
gestor_plataformas = GestorArchivos(Plataforma, "plataformas.json")
gestor_juegos = GestorArchivos(Juego, "juegos.json")

# Endpoints para Desarrolladores
@app.get("/desarrolladores", response_model=List[Desarrollador], tags=["Desarrolladores"])
def listar_desarrolladores():
    return gestor_desarrolladores.get_all()

@app.get("/desarrolladores/{id}", response_model=Desarrollador, tags=["Desarrolladores"])
def obtener_desarrollador(id: int):
    desarrollador = gestor_desarrolladores.get_by_id(id)
    if not desarrollador:
        raise HTTPException(status_code=404, detail="Desarrollador no encontrado")
    return desarrollador

@app.post("/desarrolladores", response_model=Desarrollador, status_code=201, tags=["Desarrolladores"])
def crear_desarrollador(desarrollador: Desarrollador):
    try:
        return gestor_desarrolladores.add(desarrollador)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/desarrolladores/{id}", response_model=Desarrollador, tags=["Desarrolladores"])
def actualizar_desarrollador(id: int, desarrollador: Desarrollador):
    if id != desarrollador.id:
        raise HTTPException(status_code=400, detail="ID en URL no coincide con ID en cuerpo")
    
    actualizado = gestor_desarrolladores.update(id, desarrollador.dict())
    if not actualizado:
        raise HTTPException(status_code=404, detail="Desarrollador no encontrado")
    return actualizado

@app.delete("/desarrolladores/{id}", status_code=204, tags=["Desarrolladores"])
def eliminar_desarrollador(id: int):
    # Verificar si el desarrollador tiene juegos asociados
    juegos = gestor_juegos.get_all()
    if any(juego.desarrollador_id == id for juego in juegos):
        raise HTTPException(
            status_code=400, 
            detail="No se puede eliminar el desarrollador porque tiene juegos asociados"
        )
    
    if not gestor_desarrolladores.delete(id):
        raise HTTPException(status_code=404, detail="Desarrollador no encontrado")

# Endpoints para Plataformas
@app.get("/plataformas", response_model=List[Plataforma], tags=["Plataformas"])
def listar_plataformas():
    return gestor_plataformas.get_all()

@app.get("/plataformas/{id}", response_model=Plataforma, tags=["Plataformas"])
def obtener_plataforma(id: int):
    plataforma = gestor_plataformas.get_by_id(id)
    if not plataforma:
        raise HTTPException(status_code=404, detail="Plataforma no encontrada")
    return plataforma

@app.post("/plataformas", response_model=Plataforma, status_code=201, tags=["Plataformas"])
def crear_plataforma(plataforma: Plataforma):
    try:
        return gestor_plataformas.add(plataforma)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/plataformas/{id}", response_model=Plataforma, tags=["Plataformas"])
def actualizar_plataforma(id: int, plataforma: Plataforma):
    if id != plataforma.id:
        raise HTTPException(status_code=400, detail="ID en URL no coincide con ID en cuerpo")
    
    actualizado = gestor_plataformas.update(id, plataforma.dict())
    if not actualizado:
        raise HTTPException(status_code=404, detail="Plataforma no encontrada")
    return actualizado

@app.delete("/plataformas/{id}", status_code=204, tags=["Plataformas"])
def eliminar_plataforma(id: int):
    # Verificar si la plataforma está asociada a algún juego
    juegos = gestor_juegos.get_all()
    if any(id in juego.plataformas for juego in juegos):
        raise HTTPException(
            status_code=400, 
            detail="No se puede eliminar la plataforma porque está asociada a juegos"
        )
    
    if not gestor_plataformas.delete(id):
        raise HTTPException(status_code=404, detail="Plataforma no encontrada")

# Endpoints para Juegos
@app.get("/juegos", response_model=List[Juego], tags=["Juegos"])
def listar_juegos():
    return gestor_juegos.get_all()

@app.get("/juegos/{id}", response_model=Juego, tags=["Juegos"])
def obtener_juego(id: int):
    juego = gestor_juegos.get_by_id(id)
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return juego

@app.post("/juegos", response_model=Juego, status_code=201, tags=["Juegos"])
def crear_juego(juego: Juego):
    try:
        # Verificar que el desarrollador existe
        if not gestor_desarrolladores.get_by_id(juego.desarrollador_id):
            raise HTTPException(status_code=400, detail="Desarrollador no existe")
        
        # Verificar que las plataformas existen
        for plataforma_id in juego.plataformas:
            if not gestor_plataformas.get_by_id(plataforma_id):
                raise HTTPException(status_code=400, detail=f"Plataforma con ID {plataforma_id} no existe")
        
        return gestor_juegos.add(juego)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/juegos/{id}", response_model=Juego, tags=["Juegos"])
def actualizar_juego(id: int, juego: Juego):
    if id != juego.id:
        raise HTTPException(status_code=400, detail="ID en URL no coincide con ID en cuerpo")
    
    # Verificar que el desarrollador existe
    if not gestor_desarrolladores.get_by_id(juego.desarrollador_id):
        raise HTTPException(status_code=400, detail="Desarrollador no existe")
    
    # Verificar que las plataformas existen
    for plataforma_id in juego.plataformas:
        if not gestor_plataformas.get_by_id(plataforma_id):
            raise HTTPException(status_code=400, detail=f"Plataforma con ID {plataforma_id} no existe")
    
    actualizado = gestor_juegos.update(id, juego.dict())
    if not actualizado:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return actualizado

@app.delete("/juegos/{id}", status_code=204, tags=["Juegos"])
def eliminar_juego(id: int):
    if not gestor_juegos.delete(id):
        raise HTTPException(status_code=404, detail="Juego no encontrado")

# Endpoint adicional para búsqueda
@app.get("/juegos/buscar", response_model=List[Juego], tags=["Juegos"])
def buscar_juegos(
    genero: Optional[str] = None,
    año_min: Optional[int] = None,
    año_max: Optional[int] = None
):
    juegos = gestor_juegos.get_all()
    
    if genero:
        juegos = [j for j in juegos if j.genero.lower() == genero.lower()]
    
    if año_min:
        juegos = [j for j in juegos if j.año_lanzamiento >= año_min]
    
    if año_max:
        juegos = [j for j in juegos if j.año_lanzamiento <= año_max]
    
    return juegos