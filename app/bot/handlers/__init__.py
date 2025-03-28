# backend/app/bot/handlers/__init__.py
from aiogram import Dispatcher, Router
import logging

# Импортируем роутеры из других модулей
from .user import user_router
# from .admin import admin_router # Если будут команды для админов
# from .other import other_router # И т.д.

logger = logging.getLogger(__name__)

def register_handlers(dp: Dispatcher):
    """
    Регистрирует все роутеры с хендлерами в главном диспетчере.
    """
    # Создаем главный роутер (можно и без него, подключая каждый роутер напрямую к dp)
    main_router = Router(name="main_bot_router")

    # Подключаем дочерние роутеры к главному роутеру
    main_router.include_router(user_router)
    # main_router.include_router(admin_router) # << Пример для будущего
    # main_router.include_router(other_router) # << Пример для будущего

    # >>>>> ИЗМЕНЕНИЕ ЗДЕСЬ: Регистрируем ТОЛЬКО главный роутер в диспетчере <<<<<
    dp.include_router(main_router)

    # --- Убираем или комментируем прямое подключение user_router к dp ---
    # dp.include_router(user_router)
    # ------------------------------------------------------------------

    logger.info("Bot message and callback handlers registered successfully via main_router.")