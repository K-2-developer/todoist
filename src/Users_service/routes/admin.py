# routes/admin.py
from fastapi import APIRouter, Depends
from typing import List, Annotated
from uuid import UUID
from Users_service.dependencies import get_admin_service, get_current_admin_user
from Users_service.service.admin_service import AdminService
from Users_service.schemas.user_schemas import UserResponse, UserRoleUpdate
from Users_service.Domain.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get('/users', response_model=List[UserResponse])
async def get_all_users(
    admin_service: AdminService = Depends(get_admin_service),
    _admin: Annotated[User, Depends(get_current_admin_user)] = None
):
    return await admin_service.get_all_users_full()

@router.patch('/users/{user_id}/role', status_code=204)
async def update_user_role(
    user_id: UUID,
    data: UserRoleUpdate,
    admin_service: AdminService = Depends(get_admin_service),
    _admin: Annotated[User, Depends(get_current_admin_user)] = None
):
    await admin_service.update_user_role(user_id, data.role)