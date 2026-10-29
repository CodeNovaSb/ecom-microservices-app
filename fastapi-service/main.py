from fastapi import FastAPI
from app.orders.routes import router as orders_router
from app.payments.routes import router as payments_router

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(orders_router)

app.include_router(payments_router)


