from fastapi import FastAPI
from Boards_service.routes import workspace, boards, columns, tasks

app = FastAPI(
    title='Users Service',
    version="1.0.0"
)