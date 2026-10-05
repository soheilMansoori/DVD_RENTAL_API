from fastapi_offline import FastAPIOffline

app = FastAPIOffline()


@app.get("/")
def root():
    return {"message": "welcome to FastAPI DVD_RENTAL_API app"}
