from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="FastAPI + Playwright Demo")

templates = Jinja2Templates(directory="app/templates")

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.get("/api/greet")
async def greet(name: str = "world"):
    return {"message": f"Hello, {name}!"}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "FastAPI Demo"},
    )
