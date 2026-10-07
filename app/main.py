from fastapi_offline import FastAPIOffline

from app.actor.router import router as actor_router

app = FastAPIOffline()


@app.get("/")
def root():
    return {"message": "welcome to FastAPI DVD_RENTAL_API app"}


# routes
app.include_router(actor_router)
