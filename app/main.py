from fastapi_offline import FastAPIOffline

from app.actor.router import router as actor_router
from app.country.router import router as country_router
from app.language.router import router as language_router

app = FastAPIOffline()


@app.get("/")
def root():
    return {"message": "welcome to FastAPI DVD_RENTAL_API app"}


# routes
app.include_router(actor_router)
app.include_router(language_router)
app.include_router(country_router)
