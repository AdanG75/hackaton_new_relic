from typing import Optional

from db.mongo_connection import act_db
from schemas.schemas import RegistroUsuario, UsuarioResponse, UsuarioVerify
from utils.hashing import Hash

usuarios_collection = act_db["usuarios"]


def create_usuario(usuario: RegistroUsuario) -> UsuarioResponse:
    usuario_dict = dict(usuario)
    # Obtenemos el hash de la contraseña
    usuario_dict['password'] = Hash.bcrypt(usuario_dict['password'])

    inserted_id = str(usuarios_collection.insert_one(usuario_dict).inserted_id)

    return UsuarioResponse(
        id=inserted_id,
        email=usuario.email,
        nombre=usuario.nombre
    )


def get_usuario_by_email(email: str) -> Optional[UsuarioResponse]:
    usuario = usuarios_collection.find_one({'email': email})

    if usuario is not None:
        return UsuarioResponse(
            id=str(usuario['_id']),
            email=str(usuario['email']),
            nombre=str(usuario['nombre'])
        )

    return usuario


def get_usuario_to_verify(email: str) -> Optional[UsuarioVerify]:
    usuario = usuarios_collection.find_one({'email': email})

    if usuario is not None:
        return UsuarioVerify(
            id=str(usuario['_id']),
            email=str(usuario['email']),
            nombre=str(usuario['nombre']),
            password=str(usuario['password'])
        )

    return usuario
