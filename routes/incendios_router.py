from typing import Optional

from fastapi import APIRouter, Query, Body, Path, Depends
from starlette import status

from auth.oauth2 import get_current_user
from db import incendios_db
from schemas.enum_objects import EstadoFuego
from schemas.schemas import Incendios, IncendioResponse, Incendio, BasicResponse, UsuarioResponse

router = APIRouter(tags=['Incendios'])


@router.get(
    path="/incendios",
    response_model=Incendios,
    status_code=status.HTTP_200_OK
)
async def get_incendios(
    activos: Optional[bool] = Query(True)
):
    """
    GET Obtiene los incendios registrados en el sistema. En caso que se pase el parametro \'activos\' con el valor
    true solamente se retornarán aquellos incendios que aún no se hayan apagado.
    Si su valor es false o simplemente no se pasa, se retornarán todos los incendios que estén
    almacenados en el sistema.

    **Parametros**
    - activos (bool): Debe ser pasado como un **query parameter** e indica que tipos de incendios se retornarán,
    los activos(true) o todos(false||null)

    **Respuesta**
    - Regresa un objeto de tipo \'Incendios\' que contiene el parametro \'incendios\' que, a su vez, es una
    lista de objetos \'IncendioResponse\' que contiene los valores: id, latitud, longitud, direccion, riesgo,
    estatus, revisado
    """
    if activos:
        incendios_response = incendios_db.get_incendios_activos()
    else:
        incendios_response = incendios_db.get_all_incendios()

    return incendios_response


@router.post(
    path="/incendio",
    response_model=IncendioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Reportar incendio"
)
async def alert_incendio(
        incendio: Incendio = Body(...)
):
    """
    POST Almacena el incendio enviado por la persona

    **Parametros**
    - incendio (Incendio): Debe ser pasado como un **body parameter** e el incendio a reportar,
    los valores que debe contener el objeto \'Incendio\' son: latitud, logitud, direccion

    **Respuesta**
    - Regresa un objeto de tipo \'IncendioResponse\' que contiene los valores: id, latitud, longitud, direccion, riesgo,
    estatus, revisado
    """
    incendio_response = incendios_db.alert_incendio(incendio)

    return incendio_response


@router.patch(
    path="/incendio/{id_incendio}",
    response_model=BasicResponse,
    status_code=status.HTTP_200_OK
)
async def update_incendio(
        id_incendio: str = Path(..., min_length=16, max_length=32),
        verificado: Optional[bool] = Query(None),
        estado: Optional[EstadoFuego] = Query(None),
        current_user: UsuarioResponse = Depends(get_current_user)
):
    """
    PATCH Modifica el objeto incendio dependiendo de los valores que se envíen como query parameters

    **Parametros**
    - id_incendio (str): ID del incendio que se desea modificar, debe ser enviado como **path parameter**
    - verificado (bool): Debe se pasado como un **query parameter** e indica si los bomberos
    ya han validado el incendio o no
    - estado (EstadoFuego): Debe se pasado como un **query parameter** e indica el estado actual del incendio.
    Solamente puede contener tres valores: \'Activo\', \'Apagando\' o \'Apagado\'
    - Authorization (Header): Este parametro debe ser pasado dentro de la **cabecera de la petición** y debe contener
    el tipo de token y el token. Un ejemplo sería el siguiente: Bearer eyJhbGciOiJIUzI1NiIjA...

    **Respuesta**
    - Regresa un objeto de tipo \'BasicResponse\' que contiene el volor \'response\' que es de tipo str
    """
    msg = ''
    if verificado is not None:
        msg += incendios_db.verificar_incendio(id_incendio, verificado)

    if estado is not None:
        msg += incendios_db.change_status_incendio(id_incendio, estado)

    if len(msg) <= 0:
        msg = "Ningun cambio efectuado"

    return BasicResponse(response=msg)
