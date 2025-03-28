# backend/app/api/v1/router.py
from fastapi import APIRouter
# Импортируем все роутеры эндпоинтов
from app.api.v1.endpoints import products, orders, categories # Добавляем categories

api_router_v1 = APIRouter()

# Подключаем роутеры из эндпоинтов с префиксами
api_router_v1.include_router(products.router, prefix="/products", tags=["Products"])
api_router_v1.include_router(orders.router, prefix="/orders", tags=["Orders"])
# >>>>> ДОБАВЛЯЕМ ПОДКЛЮЧЕНИЕ РОУТЕРА КАТЕГОРИЙ <<<<<
api_router_v1.include_router(categories.router, prefix="/categories", tags=["Categories"])