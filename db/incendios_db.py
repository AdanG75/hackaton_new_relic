from typing import List

from bson import ObjectId

from db.mongo_connection import act_db
from db.lugares_db import get_lugares
from schemas.enum_objects import Riesgo, EstadoFuego
from schemas.schemas import IncendioResponse, Incendio, Lugares, Incendios
from utils.utils import haversine

incendios_collection = act_db["incendios"]


def alert_incendio(incendio: Incendio, logged: bool = False) -> IncendioResponse:
    lugares = get_lugares()
    riesgo_incendio = get_risk(incendio, lugares)

    incendio_dict = dict(incendio)
    incendio_dict['riesgo'] = riesgo_incendio
    incendio_dict['estatus'] = str(EstadoFuego.activo.value)
    incendio_dict['revisado'] = logged

    inserted_id: str = str(incendios_collection.insert_one(incendio_dict).inserted_id)

    return IncendioResponse(
        id=inserted_id,
        latitud=incendio_dict['latitud'],
        longitud=incendio_dict['longitud'],
        direccion=incendio_dict['direccion'],
        riesgo=incendio_dict['riesgo'],
        estatus=incendio_dict['estatus'],
        revisado=incendio_dict['revisado']
    )


def get_risk(incendio: Incendio, lugares: Lugares) -> str:
    riesgo = str(Riesgo.bajo.value)
    riesgo_medio_flag = False

    for lugar in lugares.lugares:
        # Evalua que la distancia sea menor a 500m
        if haversine(incendio.latitud, incendio.longitud, lugar.latitud, lugar.longitud) <= 500:
            if lugar.riesgo == Riesgo.alto:
                return str(Riesgo.alto.value)

            if not riesgo_medio_flag and lugar.riesgo == Riesgo.medio.value:
                riesgo = str(Riesgo.medio.value)
                riesgo_medio_flag = True

    return riesgo


def get_incendios_activos() -> Incendios:
    incendios_list: List[IncendioResponse] = []

    for incendio in incendios_collection.find({"estatus": {"$regex": "^(Activo||Apagando)$"}}):
        new_incendio = IncendioResponse(
            id=str(incendio['_id']),
            latitud=float(incendio['latitud']),
            longitud=float(incendio['longitud']),
            direccion=str(incendio['direccion']),
            riesgo=str(incendio['riesgo']),
            estatus=str(incendio['estatus']),
            revisado=bool(incendio['revisado'])
        )
        incendios_list.append(new_incendio)

    return Incendios(incendios=incendios_list)


def get_all_incendios() -> Incendios:
    incendios_list: List[IncendioResponse] = []

    for incendio in incendios_collection.find():
        new_incendio = IncendioResponse(
            id=str(incendio['_id']),
            latitud=float(incendio['latitud']),
            longitud=float(incendio['longitud']),
            direccion=str(incendio['direccion']),
            riesgo=str(incendio['riesgo']),
            estatus=str(incendio['estatus']),
            revisado=bool(incendio['revisado'])
        )
        incendios_list.append(new_incendio)

    return Incendios(incendios=incendios_list)


def verificar_incendio(id_incendio: str, verificado: bool) -> str:
    count_changes = incendios_collection.update_one(
        {'_id': ObjectId(id_incendio)},
        {'$set': {'revisado': verificado}}
    ).modified_count

    return f"\nTotal de elementos modificados {count_changes}"


def change_status_incendio(id_incendio: str, status: EstadoFuego) -> str:
    count_changes = incendios_collection.update_one(
        {'_id': ObjectId(id_incendio)},
        {'$set': {'estatus': str(status.value)}}
    ).modified_count

    if count_changes > 0:
        return "\nEstado cambiado a: {}".format(status.value)
    else:
        return "\nNo se ha realizado ningun cambio"
