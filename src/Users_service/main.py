import sys
from pathlib import Path
from fastapi.responses import JSONResponse

sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, Request
from routes import users, authentication, admin
from core.exceptions import UserNotFound, PermissionError, ConflictError




app = FastAPI(
    title='Users Service',
    version="1.0.0"
)
@app.exception_handler(UserNotFound)
async def user_not_found_handler(request: Request, exc: UserNotFound):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(PermissionError)
async def permission_error_handler(request: Request, exc: PermissionError):
    return JSONResponse(status_code=403, content={"detail": str(exc)})

@app.exception_handler(ConflictError)
async def conflict_error_handler(request: Request, exc: ConflictError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(admin.router)