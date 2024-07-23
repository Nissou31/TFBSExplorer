from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from .endpoints import health, tfbs, welcome

app = FastAPI(title="TFSBExplorer", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(health.router)
app.include_router(tfbs.router)
app.include_router(welcome.router)


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")
