from typing import List

from db.mongo_connection import act_db
from schemas.schemas import LugarResponse, Lugares, Lugar

lugares_collection = act_db["lugares"]


def get_lugares() -> Lugares:
    lugares_list: List[LugarResponse] = []
    for lugar in lugares_collection.find():
        new_lugar = LugarResponse(
            id=str(lugar['_id']),
            email=str(lugar['email']),
            latitud=float(lugar['latitud']),
            longitud=float(lugar['longitud']),
            direccion=str(lugar['direccion']),
            riesgo=str(lugar['riesgo'])
        )
        lugares_list.append(new_lugar)

    return Lugares(lugares=lugares_list)


def get_lugares_based_risk(riesgo: str) -> Lugares:
    lugares_list: List[LugarResponse] = []
    for lugar in lugares_collection.find({"riesgo": riesgo}):
        new_lugar = LugarResponse(
            id=str(lugar['_id']),
            email=str(lugar['email']),
            latitud=float(lugar['latitud']),
            longitud=float(lugar['longitud']),
            direccion=str(lugar['direccion']),
            riesgo=str(lugar['riesgo'])
        )
        lugares_list.append(new_lugar)

    return Lugares(lugares=lugares_list)


def save_lugar(lugar: Lugar) -> LugarResponse:
    lugar_dict = dict(lugar)
    lugar_dict['riesgo'] = str(lugar_dict['riesgo'].value)

    inserted_id = str(lugares_collection.insert_one(lugar_dict).inserted_id)

    return LugarResponse(
        id=inserted_id,
        email=lugar.email,
        latitud=lugar.latitud,
        longitud=lugar.longitud,
        direccion=lugar.direccion,
        riesgo=lugar.riesgo
    )
