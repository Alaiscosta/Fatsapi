from typing import List
import json
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException, status
from models import Gender, Role, User, UserResponse


app = FastAPI(
    title="API de Gestión de Usuarios",
    description="API para gestionar información de usuarios",
    version="1.0.0"
)

# Cargar datos de usuarios desde el archivo JSON
def load_users():
    with open("users.json", "r") as file:
        users_data = json.load(file)
        users = []
        for user_data in users_data:
            # Convertir UUID de string a objeto UUID
            user_data["id"] = UUID(user_data["id"])
            # Convertir strings de género y roles a enumeraciones
            user_data["gender"] = Gender(user_data["gender"])
            user_data["roles"] = [Role(role) for role in user_data["roles"]]
            users.append(User(**user_data))
    return users

# Guardar datos de usuarios en el archivo JSON
def save_users(users: List[User]):
    users_data = []
    for user in users:
        user_dict = user.dict()
        # Convertir UUID a string para JSON
        user_dict["id"] = str(user_dict["id"])
        # Convertir enumeraciones a strings para JSON
        user_dict["gender"] = user_dict["gender"].value
        user_dict["roles"] = [role.value for role in user_dict["roles"]]
        users_data.append(user_dict)
    
    with open("users.json", "w") as file:
        json.dump(users_data, file, indent=4)

# Cargar la base de datos al inicio
db: List[User] = load_users()

@app.get("/")
async def root():
    # Convertir los usuarios a diccionarios para retornarlos como JSON
    users_list = []
    for user in db:
        user_dict = {
            "id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "gender": user.gender.value,
            "roles": [role.value for role in user.roles]
        }
        users_list.append(user_dict)
    
    return {"users":users_list}

@app.get("/api/v1/users/{user_id}", response_model=User)
async def get_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Usuario con ID {user_id} no encontrado"
    )

@app.post("/api/v1/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    db.append(user)
    save_users(db)  # Guardar cambios en el archivo
    return {"id": user.id}

@app.put("/api/v1/users/{user_id}", response_model=User)
async def update_user(user_id: UUID, user_update: User):
    for i, user in enumerate(db):
        if user.id == user_id:
            # Mantener el ID original
            user_update.id = user_id
            db[i] = user_update
            save_users(db)  # Guardar cambios en el archivo
            return user_update
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Usuario con ID {user_id} no encontrado"
    )

@app.delete("/api/v1/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID):
    for i, user in enumerate(db):
        if user.id == user_id:
            db.pop(i)
            save_users(db)  # Guardar cambios en el archivo
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Usuario con ID {user_id} no encontrado"
        )