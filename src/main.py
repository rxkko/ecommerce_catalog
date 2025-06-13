from fastapi import FastAPI
from src.api.routes import product, user


app = FastAPI()

app.include_router(product.router)
app.include_router(user.router)