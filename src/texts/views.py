from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


views = APIRouter(prefix="/texts", tags=["Views"])
templates = Jinja2Templates("../templates")


@views.get("", response_class=HTMLResponse)
async def get_texts_page(request: Request):
    return templates.TemplateResponse(request, "texts.html")


@views.get("/{text_id}", response_class=HTMLResponse)
async def get_text_page(request: Request):
    return templates.TemplateResponse(request, name="text.html")
