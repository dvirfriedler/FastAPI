from fastapi import FastAPI
from .database import engine 
from .models import Base
from .routers import auth, todos, admin, users
from starlette.staticfiles import StaticFiles
import os



app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/healthy")
def healthcheck():
    return {"status": "healthy"}

static_directory = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_directory), name="static")

app.include_router(users.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(todos.router)

