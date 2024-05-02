from fastapi import FastAPI, Path, Query, HTTPException
import models
from database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)