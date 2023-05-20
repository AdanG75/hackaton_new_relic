from typing import Optional

from fastapi import APIRouter, Query, Body, Depends
from starlette import status

from auth.oauth2 import get_current_user
from db import lugares_db
from schemas.enum_objects import Riesgo
from schemas.schemas import Lugares, Lugar, LugarResponse, UsuarioResponse

router = APIRouter(tags=['Lugares'])


@router.get(
    path="/lugares",
    response_model=Lugares,
    status_code=status.HTTP_200_OK,
    summary="Obtener lugares"
)
async def get_lugares(
        riesgo: Optional[Riesgo] = Query(None)
):
    """
    GET Obtiene los lugares que coincidan con el lugar de riesgo enviado como query parameter. En caso qe no se envíe
    ningún parametro, regresará todos los lugares registrados

    **Parametros**
    - riesgo (Riesgo): Debe se pasado como un **query parameter** y solamente puede contener los siguientes valores:
    \"Alto\", \"Medio\" o \"Bajo\"

    **Respuesta**
    - Regresa un objeto de tipo \'Lugares\' que contiene el parametro \'lugares\' que, a su vez, es una
    lista de objetos \'LugarResponse\' que contiene los valores: id, email, latitud, longitud, direccion, riesgo
    """
    if riesgo is None:
        lugares = lugares_db.get_lugares()
    else:
        lugares = lugares_db.get_lugares_based_risk(str(riesgo.value))

    return lugares


@router.post(
    path="/lugar",
    response_model=LugarResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Agregar lugar"
)
async def create_lugar(
        lugar: Lugar = Body(...),
        current_user: UsuarioResponse = Depends(get_current_user)
):
    """
    POST Guardará un objeto lugar dentro del sistema. Para ello se debe estar registrado dentro del sistema

    **Parametros**
    - lugar (Lugar): Debe se pasado como un **body parameter** y debe contener los valores: email, latitud, longitud,
    direccion, riesgo(\"Alto\", \"Medio\" o \"Bajo\")
    - Authorization (Header): Este parametro debe ser pasado dentro de la **cabecera de la petición** y debe contener
    el tipo de token y el token. Un ejemplo sería el siguiente: Bearer eyJhbGciOiJIUzI1NiIjA...

    **Respuesta**
    - Regresa un objeto de tipo \'LugarResponse\' que contiene los valores: id, email, latitud,
    longitud, direccion, riesgo
    """
    lugar_response = lugares_db.save_lugar(lugar)

    return lugar_response
