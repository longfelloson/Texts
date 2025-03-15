from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from auth.utils import get_current_user
from database import db
from auth.views import views as auth_views
from auth.router import router as auth_router
from users.router import router as users_router
from texts.views import views as texts_views
from texts.router import router as texts_router


templates = Jinja2Templates("../templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Creates tables and schedules the deletion of expried texts"""
    await db.create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="../static"), name="static")

app.include_router(texts_router)
app.include_router(texts_views)
app.include_router(auth_router)
app.include_router(auth_views)
app.include_router(users_router)
# app.include_router(users_views)


@app.get(
    "/",
    response_class=HTMLResponse,
    dependencies=[Depends(get_current_user)],
)
async def get_main_page(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def unauthorized_error_handler(_: Request, __: HTTPException):
    response = RedirectResponse(
        url="/login", 
        status_code=status.HTTP_303_SEE_OTHER
    )
    return response
