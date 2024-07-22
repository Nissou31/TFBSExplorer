from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .endpoints import health, welcome, tfbs

app = FastAPI()

app.include_router(health.router)
app.include_router(welcome.router)
app.include_router(tfbs.router)


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")
