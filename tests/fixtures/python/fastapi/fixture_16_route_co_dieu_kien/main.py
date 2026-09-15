from fastapi import FastAPI

import settings
from private import router as private_router
from public import router as public_router

app = FastAPI()
app.include_router(public_router)

# Route ben trong chi ton tai o mot so moi truong. Tai lieu phai noi ro dieu do.
if settings.ENV == "development":
    app.include_router(private_router)
