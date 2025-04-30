from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import init_db

app = FastAPI(
    title="Central Asia Tours API",
    docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json"
)

# список конкретных фронтовых origin
origins = [
    "http://localhost:5173",  # Vite dev-server
    "https://your.production.app"  # ваш продакшен-домен
]

# обязательно монтировать CORS перед регистрацией роутов и StaticFiles
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # НЕ "*" при allow_credentials=True
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    error_details = []
    for err in exc.errors():
        field_path = " → ".join(map(str, err["loc"]))  # Преобразуем список loc в читаемую строку
        error_message = f"Ошибка в поле '{field_path}': {err['msg']}"
        error_details.append(error_message)

    # Выводим в консоль в более удобочитаемом формате
    print("❌ Ошибка валидации запроса:")
    for error in error_details:
        print(f"  - {error}")

    return JSONResponse(
        status_code=422,
        content={"detail": error_details}
    )


# теперь можно монтировать статику
from fastapi.staticfiles import StaticFiles

app.mount("/images", StaticFiles(directory="images"), name="images")

# и подключать роутеры
from app.routers import auth, users, tours, orders

app.include_router(auth.router, tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tours.router, prefix="/tours", tags=["tours"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])

# Инициализация БД
init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
