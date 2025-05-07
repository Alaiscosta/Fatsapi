import json
from typing import Type, TypeVar, List, Dict, Any, Optional  
from pathlib import Path
from models import Desarrollador, Plataforma, Juego

T = TypeVar('T', Desarrollador, Plataforma, Juego)


class GestorArchivos:
    def __init__(self, model_class: Type[T], filename: str):
        self.model_class = model_class
        self.filename = filename
        self.filepath = Path(filename)
        # Crear archivo si no existe
        if not self.filepath.exists():
            self.filepath.write_text("[]")
    
    def _read_data(self) -> List[Dict[str, Any]]:
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _write_data(self, data: List[Dict[str, Any]]) -> None:
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    
    def get_all(self) -> List[T]:
        data = self._read_data()
        return [self.model_class(**item) for item in data]
    
    def get_by_id(self, id: int) -> Optional[T]:
        data = self._read_data()
        for item in data:
            if item['id'] == id:
                return self.model_class(**item)
        return None
    
    def add(self, objeto: T) -> T:
        data = self._read_data()
        # Verificar si el ID ya existe
        if any(item['id'] == objeto.id for item in data):
            raise ValueError(f"Ya existe un {self.model_class.__name__} con ID {objeto.id}")
        
        data.append(objeto.dict())
        self._write_data(data)
        return objeto
    
    def update(self, id: int, datos: Dict[str, Any]) -> Optional[T]:
        data = self._read_data()
        updated = None
        for item in data:
            if item['id'] == id:
                item.update(datos)
                updated = self.model_class(**item)
                break
        
        if updated:
            self._write_data(data)
            return updated
        return None
    
    def delete(self, id: int) -> bool:
        data = self._read_data()
        initial_length = len(data)
        data = [item for item in data if item['id'] != id]
        
        if len(data) < initial_length:
            self._write_data(data)
            return True
        return False