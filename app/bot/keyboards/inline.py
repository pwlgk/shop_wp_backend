# backend/app/bot/keyboards/inline.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.config import settings

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру с кнопкой для запуска Web App магазина.
    """
    # Используем InlineKeyboardBuilder для удобного создания клавиатур
    builder = InlineKeyboardBuilder()

    # Проверяем, что URL для Mini App задан в настройках
    if not settings.MINI_APP_URL:
        # В этом случае не можем создать кнопку WebApp.
        # Можно вернуть пустую клавиатуру или кнопку с сообщением об ошибке.
        # Логируем предупреждение.
        import logging
        logging.getLogger(__name__).warning("MINI_APP_URL is not set in settings. Cannot create WebApp button.")
        # Вернем простую кнопку как плейсхолдер или можно вообще ничего не возвращать
        builder.button(text="❌ Магазин временно недоступен", callback_data="shop_unavailable")
    else:
        # Создаем объект WebAppInfo с URL нашего фронтенда
        web_app_info = WebAppInfo(url=settings.MINI_APP_URL)

        # Добавляем кнопку типа web_app
        builder.button(
            text="🛍️ Открыть магазин", # Текст на кнопке
            web_app=web_app_info
        )

    # Указываем, что кнопки должны располагаться по одной в строке
    builder.adjust(1)

    # Возвращаем готовую клавиатуру
    return builder.as_markup()

# Пример другой клавиатуры, если понадобится
# def get_some_other_keyboard() -> InlineKeyboardMarkup:
#     builder = InlineKeyboardBuilder()
#     builder.button(text="Кнопка 1", callback_data="button_1_pressed")
#     builder.button(text="Кнопка 2", callback_data="button_2_pressed")
#     builder.adjust(2) # Две кнопки в строке
#     return builder.as_markup()