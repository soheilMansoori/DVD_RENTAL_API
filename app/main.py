from fastapi_offline import FastAPIOffline

from app.actor.router import router as actor_router
from app.address.router import router as address_router
from app.category.router import router as category_router
from app.city.router import router as city_router
from app.country.router import router as country_router
from app.customer.router import router as customer_router
from app.film.router import router as film_router
from app.film_actor.router import router as film_actor_router
from app.film_category.router import router as film_category_router
from app.language.router import router as language_router
from app.staff.router import router as staff_router
from app.store.router import router as store_router

app = FastAPIOffline()


@app.get("/", tags=["Welcome"])
def root():
    return {"message": "welcome to FastAPI DVD_RENTAL_API app"}


# routes
app.include_router(actor_router)
app.include_router(language_router)
app.include_router(country_router)
app.include_router(city_router)
app.include_router(address_router)
app.include_router(category_router)
app.include_router(film_router)
app.include_router(film_actor_router)
app.include_router(film_category_router)
app.include_router(store_router)
app.include_router(staff_router)
app.include_router(customer_router)
