from fastapi import FastAPI
from src.Boards_service.routes import workspace, boards, columns, tasks

app = FastAPI(
    title='Boards Service',
    version="1.0.0"
)


app.include_router(workspace.router)
app.include_router(boards.router)
app.include_router(columns.router)
app.include_router(tasks.router)




# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
