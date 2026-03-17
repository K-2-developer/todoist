from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from Users_service.core.exceptions import ConflictError
from Users_service.dependencies import get_user_service
from Users_service.service.user_service import UserService
from Users_service.schemas.user_schemas import UserCreate, Token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=201)
async def register(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    try:
        user_id = await service.create_user(user_data)
        return {"id": user_id}
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserService = Depends(get_user_service)
):
    user = await service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = service.create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)