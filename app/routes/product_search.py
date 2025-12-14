from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.scraper.productos_repo import buscar_modelos_unicos

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/product_search", response_class=HTMLResponse)
def product_search(request: Request, q: str = None):
    modelos = []
    mensaje = None

    if q:
        modelos = buscar_modelos_unicos(q)

        if not modelos:
            mensaje = f"No se encontraron resultados para '{q}'"

    return templates.TemplateResponse(
        "product-search.html",
        {
            "request": request,
            "modelos": modelos,
            "query": q,
            "mensaje": mensaje
        }
    )
