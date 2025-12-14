from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.routes import login, register, product_search,product
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

SECRET_KEY = os.getenv("SECRET_KEY")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

templates = Jinja2Templates(directory="app/templates")

app.include_router(login.router)
app.include_router(register.router)
app.include_router(product_search.router)
app.include_router(product.router)

@app.get("/", response_class=HTMLResponse)
def index (request:Request):
    return templates.TemplateResponse("index.html", {"request":request})