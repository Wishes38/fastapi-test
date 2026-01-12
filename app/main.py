from fastapi import FastAPI
from app.core.database import engine, Base
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Ticaret API",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"mesaj": "API deneme"}