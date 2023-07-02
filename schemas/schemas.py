from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr

from schemas.enum_objects import EstadoFuego, Riesgo


class BasicResponse(BaseModel):
    response: str = Field("Error", min_length=1, max_length=200)


class Incendio(BaseModel):
    latitud: float = Field(..., ge=-90, le=90)
    longitud: float = Field(..., ge=-180, le=180)
    direccion: Optional[str] = Field(None, min_length=1, max_length=190)
    riesgo: Optional[Riesgo] = Field(None)
    estatus: Optional[EstadoFuego] = Field(None)
    revisado: Optional[bool] = Field(False)

    class Config:
        schema_extra = {
            "example": {
                "latitud": 4.6817269457138835,
                "longitud": -74.08216613225932,
                "direccion": "CIUDADELA COMERCIAL METROPOLIS, Ak 68 No. 75 A – 50, Bogotá, Colombia"
            }
        }


class IncendioResponse(Incendio):
    id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": "dsfds656d6f1grf16gd1f-fdd",
                "latitud": 4.6817269457138835,
                "longitud": -74.08216613225932,
                "direccion": "CIUDADELA COMERCIAL METROPOLIS, Ak 68 No. 75 A – 50, Bogotá, Colombia",
                "riesgo": "Medio",
                "estatus": "Activo",
                "revisado": True
            }
        }


class Incendios(BaseModel):
    incendios: List[IncendioResponse] = Field(...)


class Lugar(BaseModel):
    email: EmailStr = Field(...)
    latitud: float = Field(..., ge=-90, le=90)
    longitud: float = Field(..., ge=-180, le=180)
    direccion: Optional[str] = Field(None, min_length=1, max_length=190)
    riesgo: Optional[Riesgo] = Field(None)

    class Config:
        schema_extra = {
            "example": {
                "email": "lugar0@lugarmail.com",
                "latitud": 4.6817269457138835,
                "longitud": -74.08216613225932,
                "direccion": "CIUDADELA COMERCIAL METROPOLIS, Ak 68 No. 75 A – 50, Bogotá, Colombia",
                "riesgo": "Bajo"
            }
        }


class LugarResponse(Lugar):
    id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": "dfsdd84gf1g6sgfgffdh6-95fd",
                "email": "lugar0@lugarmail.com",
                "latitud": 4.6817269457138835,
                "longitud": -74.08216613225932,
                "direccion": "CIUDADELA COMERCIAL METROPOLIS, Ak 68 No. 75 A – 50, Bogotá, Colombia",
                "riesgo": "Bajo"
            }
        }


class Lugares(BaseModel):
    lugares: List[LugarResponse] = Field(...)


class UsuarioBase(BaseModel):
    email: EmailStr = Field(...)
    nombre: str = Field(..., min_length=2, max_length=200)


class RegistroUsuario(UsuarioBase):
    password: str = Field(..., min_length=8, max_length=61)

    class Config:
        schema_extra = {
            "example": {
                "email": "bombero1@bomberosmail.com",
                "nombre": "Pedro Galindo",
                "password": "123456789"
            }
        }


class UsuarioResponse(UsuarioBase):
    id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "bombero1@bomberosmail.com",
                "nombre": "Pedro Galindo",
                "id": "123m5-7dso74hg8-erh9-91h"
            }
        }


class UsuarioVerify(UsuarioBase):
    id: str = Field(...)
    password: str = Field(..., min_length=8, max_length=61)


class Token(BaseModel):
    access_token: str = Field(...)
    token_type: str = Field("bearer")
    user_id:str = Field(...)
    username: str = Field(...)
