import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI
from routes import users, authentication




app = FastAPI(
    title='Users Service',
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(authentication.router)
