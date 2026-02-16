from fastapi import FastAPI
from Boards_service.routes import workspace, boards, columns, tasks

app = FastAPI(
    title='Boards Service',
    version="1.0.0"
)


app.include_router(workspace.router)
app.include_router(boards.router)
app.include_router(columns.router)
app.include_router(tasks.router)


