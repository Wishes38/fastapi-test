from fastapi import FastAPI
from app.core.database import engine, Base
from app import models
from app.routers import users, products, orders, categories, reviews

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Ticaret API",
    version="1.0.0",
    description="4010930246@erciyes.edu.tr Serkan Özdemir, Saygılarımla"
)

app.include_router(users.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(orders.router)
app.include_router(reviews.router)

@app.get("/")
def read_root():
    return {"mesaj": "API çalışıyor. /docs adresinde swagger'ı kullanabilirsiniz."}

