from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


views = APIRouter()
templates = Jinja2Templates("../templates")


@views.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse(request, name="login.html")


@views.get("/register", response_class=HTMLResponse)
async def get_registration_page(request: Request):
    return templates.TemplateResponse(request, name="register.html")
