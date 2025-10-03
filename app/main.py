from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes import example

app = FastAPI(
    title="Lendy",
    description="Lendy helps you accept income-contingent payments",
    version="1.0.0",
)

# Templates
templates = Jinja2Templates(directory="app/templates")

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(example.router, prefix="/api/v1")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/old", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("indexOld.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
