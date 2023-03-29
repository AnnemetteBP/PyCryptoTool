from fastapi import FastAPI, Response, Request, status
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse, status_code=200)
async def read_item(request: Request):
    try:
        template = templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        Response.status_code = status.HTTP_404_NOT_FOUND
        template = None
    return template