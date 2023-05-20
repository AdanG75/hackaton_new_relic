from typing import Optional

from fastapi import APIRouter, Body, Query, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from starlette import status

from auth.oauth2 import create_access_token
from schemas.schemas import UsuarioResponse, RegistroUsuario, UsuarioVerify, Token

from db import usuario_db
from utils.hashing import Hash

router = APIRouter(tags=["Usuario"])


@router.post(
    path='/usuario',
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear Usuario"
)
async def create_usuario(
        usuario: RegistroUsuario = Body(...)
):
    """
    POST Guarda un usuario en el sistema

    **Parametros**
    - usuario (RegistroUsuario): Debe se pasado como un **body parameter** y debe contener los valores: email, nombre
    y password

    **Respuesta**
    - Regresa un objeto de tipo \'UsuarioResponse\' con los valores: email, nombre y id
    """
    usuario_response = usuario_db.create_usuario(usuario)

    return usuario_response


@router.get(
    path="/usuario/email",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK,
    summary="Retornar usuario utilizando Email"
)
async def get_user_by_email(
        email: EmailStr = Query(None)
):
    """
    GET Obtiene el usuario que coincida con el email proporcionado

    **Parametros**
    - email (str): Debe se pasado como un **query parameter** y debe tener el formato estandar para los email

    **Respuesta**
    - Regresa un objeto de tipo \'UsuarioResponse\' con los valores: email, nombre y id
    """
    not_found_usuario = UsuarioResponse(
            id="0000000000000000000000000",
            email="notfoud@notfound.notfound",
            nombre="Not Found"
        )
    if email is None:
        return not_found_usuario
    else:
        usuario = usuario_db.get_usuario_by_email(email)

        if usuario is None:
            return not_found_usuario

        return usuario


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    summary="Ingreso de usuario (bombero)"
)
async def login(
        request: OAuth2PasswordRequestForm = Depends()
):
    """
    POST Ingreso al sistema

    **Parametros**
    - request (OAuth2PasswordRequestForm): Debe se pasado como un **form (application/x-www-form-urlencoded)** y
    debe contener los valores: username (email) y password

    **Respuesta**
    - Regresa un objeto de tipo \'Token\' con los valores: access_token, token_type, user_id, username
    """
    try:
        user: Optional[UsuarioVerify] = usuario_db.get_usuario_to_verify(request.username)

        if user is None:
            raise Exception

        if not Hash.verify(user.password, request.password):
            raise Exception

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username or password are wrong"
        )

    access_token = create_access_token(
        data={"username": user.email}
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        username=user.email
    )
