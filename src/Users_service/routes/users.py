from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from Domain.user import User
from dependencies import get_user_service
from service.user_service import UserService
from schemas.user_schemas import *
from typing import Annotated
from dependencies import get_current_user, get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post('/', response_model=UUID, status_code=201)
async def create_user(
    data : UserCreate,
    service : UserService = Depends(get_user_service)
):
    return await service.create_user(data)


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return UserResponse.model_validate(current_user)

@router.get('/{user_id}', response_model=UserResponse, status_code=200)
async def get_user(
        user_id: UUID,
        service: UserService = Depends(get_user_service),
        current_user: Annotated[User, Depends(get_current_user)] = None
):
    return await service.get_user(user_id, current_user)



@router.put('/{user_id}', status_code=204)
async def update_user(
        user_id: UUID,
        data: UserUpdate,
        service: UserService = Depends(get_user_service),
        current_user: Annotated[User, Depends(get_current_user)] = None
):
    await service.update_user(user_id, data, current_user)


@router.delete('/{user_id}', status_code=200)
async def delete_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
    current_user: Annotated[User, Depends(get_current_user)] = None
):
    await service.delete_user(user_id, current_user)
    return {"status": "archived"}


@router.delete('/{user_id}/hard', status_code=200)
async def hard_delete_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
    current_user: Annotated[User, Depends(get_current_user)] = None
):
    await service.hard_delete_user(user_id, current_user)
    return {"status": "deleted"}

@router.get("/", response_model=List[UserResponseShort], status_code=200)
async def list_users(
        service : UserService = Depends(get_user_service)
):
    return await service.list_all_users()

@router.get('/by_email/{email}', response_model=UserEmailResponse, status_code=200)
async def get_user_by_email(
        email : str,
        service : UserService = Depends(get_user_service)
):
    return await service.get_user_by_email(email)