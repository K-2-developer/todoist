from fastapi import FastAPI
from Users_service.routes import users

app = FastAPI(
    title='Users Service',
    version="1.0.0"
)

app.include_router(users.router)
