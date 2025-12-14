from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.connection.mongo import productos_collection

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/product/{modelo}")
def detalle_producto(request: Request, modelo: str):
    productos = list(
        productos_collection.find({"modelo": modelo})
    )

    if not productos:
        return templates.TemplateResponse(
            "404.html", {"request": request}
        )

    return templates.TemplateResponse(
        "product.html",
        {
            "request": request,
            "producto": productos[0],  # info general
            "tiendas": productos       # precios
        }
    )