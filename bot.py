import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiohttp import web

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Берем токен из переменных окружения (для безопасности)
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    logger.error("❌ Токен не найден! Добавьте TOKEN в переменные окружения")
    raise ValueError("TOKEN environment variable is required")

# ID канала из @getidsbot
CHANNEL_ID = -1003832030735  # ID канала lcd_stock_34

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Кэш для клавиатур (для скорости)
_keyboard_cache = {}

def get_back_button(callback_data):
    """Быстрое создание кнопки назад с кэшированием"""
    cache_key = f"back_{callback_data}"
    if cache_key not in _keyboard_cache:
        _keyboard_cache[cache_key] = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅ Назад", callback_data=callback_data)]
        ])
    return _keyboard_cache[cache_key]

# ================== ГЛАВНОЕ МЕНЮ ==================
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📱 Дисплей", callback_data="menu_display")],
    [InlineKeyboardButton(text="🔋 Аккумулятор", callback_data="menu_battery")],
    [InlineKeyboardButton(text="📦 Задняя крышка", callback_data="menu_back_cover")],
    [InlineKeyboardButton(text="🏠 Корпус", callback_data="menu_case")],
    [InlineKeyboardButton(text="🔄 Стекла переклей", callback_data="menu_glass")],
    [InlineKeyboardButton(text="💧 Влагозащитная проклейка", callback_data="menu_waterproof")],
    [InlineKeyboardButton(text="👆 Тачскрин", callback_data="menu_touchscreen")],
    [InlineKeyboardButton(text="🔌 Шлейфы", callback_data="menu_cables")],
    [InlineKeyboardButton(text="📸 Камера на iPhone", callback_data="menu_camera")],
    [InlineKeyboardButton(text="🖼️ Рамка дисплея", callback_data="menu_display_frame")],
    [InlineKeyboardButton(text="🔊 Динамики", callback_data="menu_speakers")],
    [InlineKeyboardButton(text="🧲 Магниты MagSafe", callback_data="menu_magsafe")],
    [InlineKeyboardButton(text="⌚ Apple Watch", callback_data="menu_apple_watch")]
])

# ================== МЕНЮ ДИСПЛЕЙ ==================
display_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📱 Оригинал", callback_data="display_original")],
    [InlineKeyboardButton(text="🔄 Снятый оригинал", callback_data="display_used_original")],
    [InlineKeyboardButton(text="🔥 Fog (дымка)", callback_data="display_fog")],
    [InlineKeyboardButton(text="💪 Hard OLED", callback_data="display_hard_oled")],
    [InlineKeyboardButton(text="🌟 Soft OLED", callback_data="display_soft_oled")],
    [InlineKeyboardButton(text="📺 Копия TFT", callback_data="display_tft")],
    [InlineKeyboardButton(text="📲 Копия in-cell", callback_data="display_incell")],
    [InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main")]
])

# ================== МЕНЮ АККУМУЛЯТОР ==================
battery_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔋 Аккумулятор", callback_data="battery_full")],
    [InlineKeyboardButton(text="🥫 Банка", callback_data="battery_cell")],
    [InlineKeyboardButton(text="🔌 Под привязку", callback_data="battery_program")],
    [InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main")]
])

# ================== МЕНЮ ЗАДНЯЯ КРЫШКА ==================
back_cover_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✨ Original", callback_data="back_original")],
    [InlineKeyboardButton(text="🔄 Снятый оригинал", callback_data="back_used_original")],
    [InlineKeyboardButton(text="📦 Копия", callback_data="back_copy")],
    [InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main")]
])

# ================== МЕНЮ КОРПУС ==================
case_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✨ Original", callback_data="case_original")],
    [InlineKeyboardButton(text="🔄 Снятые Original", callback_data="case_used_original")],
    [InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main")]
])

# ================== МЕНЮ ПРОКЛЕЙКА ==================
waterproof_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 Задняя", callback_data="waterproof_back")],
    [InlineKeyboardButton(text="🔜 Передняя", callback_data="waterproof_front")],
    [InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main")]
])

# ================== МЕНЮ ДИНАМИКИ ==================
speakers_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬆️ Верхние", callback_data="speakers_top")],
    [InlineKeyboardButton(text="⬇️ Нижние", callback_data="speakers_bottom")],
    [InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main")]
])

# ================== МЕНЮ КАМЕРА ==================
camera_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📸 Фронтальная", callback_data="camera_front")],
    [InlineKeyboardButton(text="📷 Основная", callback_data="camera_rear")],
    [InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main")]
])

# ================== МЕНЮ ШЛЕЙФЫ ==================
cables_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📶 WI-FI", callback_data="cable_wifi")],
    [InlineKeyboardButton(text="🌍 GPS", callback_data="cable_gps")],
    [InlineKeyboardButton(text="📱 GSM", callback_data="cable_gsm")],
    [InlineKeyboardButton(text="☀️ Датчик света+микрофон", callback_data="cable_light_mic")],
    [InlineKeyboardButton(text="💡 Датчик света", callback_data="cable_light")],
    [InlineKeyboardButton(text="⚡ Беспроводная зарядка + вспышка", callback_data="cable_wireless_flash")],
    [InlineKeyboardButton(text="🔘 Кнопка вкл + кнопки громкости + беспроводная зарядка", callback_data="cable_power_vol_wireless")],
    [InlineKeyboardButton(text="🔋 Беспроводная зарядка + кнопки громкости", callback_data="cable_wireless_vol")],
    [InlineKeyboardButton(text="🎤 Микрофон", callback_data="cable_mic")],
    [InlineKeyboardButton(text="⚡ Вспышка", callback_data="cable_flash")],
    [InlineKeyboardButton(text="🔛 Кнопка включения", callback_data="cable_power")],
    [InlineKeyboardButton(text="🔊 Кнопки громкости", callback_data="cable_vol")],
    [InlineKeyboardButton(text="🧲 MagSafe", callback_data="cable_magsafe")],
    [InlineKeyboardButton(text="📡 Bluetooth", callback_data="cable_bluetooth")],
    [InlineKeyboardButton(text="💳 разъем SIM", callback_data="cable_sim")],
    [InlineKeyboardButton(text="📳 Вибромотор", callback_data="cable_vibrator")],
    [InlineKeyboardButton(text="🔈 Шлейф Фронт с динамиком", callback_data="cable_front_speaker")],
    [InlineKeyboardButton(text="📐 Cканер Lidar", callback_data="cable_lidar")],
    [InlineKeyboardButton(text="🏠 Кнопка HOME", callback_data="cable_home")],
    [InlineKeyboardButton(text="🔌 Шлейф зарядки/нижний шлейф", callback_data="cable_charging")],
    [InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main")]
])

# ================== МЕНЮ APPLE WATCH ==================
apple_watch_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔋 Аккумулятор", callback_data="watch_battery")],
    [InlineKeyboardButton(text="📱 Дисплей", callback_data="watch_display")],
    [InlineKeyboardButton(text="📦 Задняя крышка", callback_data="watch_back")],
    [InlineKeyboardButton(text="🏠 Корпус", callback_data="watch_case")],
    [InlineKeyboardButton(text="🔄 Стекло", callback_data="watch_glass")],
    [InlineKeyboardButton(text="👆 Тачскрин", callback_data="watch_touch")],
    [InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main")]
])

# ================== СЛОВАРЬ С ID СООБЩЕНИЙ ==================
MESSAGES = {
    # Дисплеи
    "display_original": 9,              # https://t.me/lcd_stock_34/9
    "display_used_original": 45,         # https://t.me/lcd_stock_34/45
    "display_fog": 17,                   # https://t.me/lcd_stock_34/17
    "display_hard_oled": 16,              # https://t.me/lcd_stock_34/16
    "display_soft_oled": 15,              # https://t.me/lcd_stock_34/15
    "display_tft": 11,                    # https://t.me/lcd_stock_34/11
    "display_incell": 46,                 # https://t.me/lcd_stock_34/46
    
    # Аккумуляторы
    "battery_full": 14,                   # https://t.me/lcd_stock_34/14
    "battery_cell": 13,                   # https://t.me/lcd_stock_34/13
    "battery_program": 12,                # https://t.me/lcd_stock_34/12
    
    # Задняя крышка
    "back_original": 47,                  # https://t.me/lcd_stock_34/47
    "back_used_original": 48,             # https://t.me/lcd_stock_34/48
    "back_copy": 49,                      # https://t.me/lcd_stock_34/49
    
    # Корпус
    "case_original": 50,                  # https://t.me/lcd_stock_34/50
    "case_used_original": 51,             # https://t.me/lcd_stock_34/51
    
    # Проклейка
    "waterproof_back": 22,                # https://t.me/lcd_stock_34/22
    "waterproof_front": 53,               # https://t.me/lcd_stock_34/53
    
    # Динамики
    "speakers_top": 29,                   # https://t.me/lcd_stock_34/29
    "speakers_bottom": 54,                # https://t.me/lcd_stock_34/54
    
    # Камера
    "camera_front": 56,                   # https://t.me/lcd_stock_34/56
    "camera_rear": 26,                    # https://t.me/lcd_stock_34/26
    
    # Другие категории
    "menu_glass": 23,                     # https://t.me/lcd_stock_34/23
    "menu_touchscreen": 24,               # https://t.me/lcd_stock_34/24
    "menu_display_frame": 27,             # https://t.me/lcd_stock_34/27
    "menu_magsafe": 28,                   # https://t.me/lcd_stock_34/28
    
    # Шлейфы
    "cable_wifi": 57,                     # https://t.me/lcd_stock_34/57
    "cable_gps": 58,                      # https://t.me/lcd_stock_34/58
    "cable_gsm": 59,                      # https://t.me/lcd_stock_34/59
    "cable_light_mic": 60,                # https://t.me/lcd_stock_34/60
    "cable_light": 61,                    # https://t.me/lcd_stock_34/61
    "cable_wireless_flash": 62,           # https://t.me/lcd_stock_34/62
    "cable_power_vol_wireless": 63,       # https://t.me/lcd_stock_34/63
    "cable_wireless_vol": 64,             # https://t.me/lcd_stock_34/64
    "cable_mic": 65,                      # https://t.me/lcd_stock_34/65
    "cable_flash": 66,                    # https://t.me/lcd_stock_34/66
    "cable_power": 67,                    # https://t.me/lcd_stock_34/67
    "cable_vol": 68,                      # https://t.me/lcd_stock_34/68
    "cable_magsafe": 69,                  # https://t.me/lcd_stock_34/69
    "cable_bluetooth": 70,                # https://t.me/lcd_stock_34/70
    "cable_sim": 71,                      # https://t.me/lcd_stock_34/71
    "cable_vibrator": 72,                 # https://t.me/lcd_stock_34/72
    "cable_front_speaker": 73,            # https://t.me/lcd_stock_34/73
    "cable_lidar": 74,                    # https://t.me/lcd_stock_34/74
    "cable_home": 75,                     # https://t.me/lcd_stock_34/75
    "cable_charging": 76,                 # https://t.me/lcd_stock_34/76
    
    # Apple Watch
    "watch_battery": 31,                  # https://t.me/lcd_stock_34/31
    "watch_display": 0,                   # пока нет
    "watch_back": 32,                     # https://t.me/lcd_stock_34/32
    "watch_case": 0,                      # пока нет
    "watch_glass": 30,                    # https://t.me/lcd_stock_34/30
    "watch_touch": 33,                    # https://t.me/lcd_stock_34/33
}

# ================== ОБРАБОТЧИКИ МЕНЮ ==================
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в магазин запчастей!\n\nВыберите категорию:",
        reply_markup=main_menu
    )

# Универсальный обработчик для всех товаров
@dp.callback_query(lambda c: c.data in MESSAGES)
async def forward_from_channel(callback: types.CallbackQuery):
    message_id = MESSAGES[callback.data]
    
    # Определяем, в какое меню возвращаться
    if callback.data.startswith("display_"):
        back_to = "menu_display"
    elif callback.data.startswith("battery_"):
        back_to = "menu_battery"
    elif callback.data.startswith("back_"):
        back_to = "menu_back_cover"
    elif callback.data.startswith("case_"):
        back_to = "menu_case"
    elif callback.data.startswith("waterproof_"):
        back_to = "menu_waterproof"
    elif callback.data.startswith("speakers_"):
        back_to = "menu_speakers"
    elif callback.data.startswith("camera_"):
        back_to = "menu_camera"
    elif callback.data.startswith("cable_"):
        back_to = "menu_cables"
    elif callback.data.startswith("watch_"):
        back_to = "menu_apple_watch"
    else:
        back_to = "back_to_main"
    
    # Если message_id еще не задан (равен 0), показываем заглушку
    if message_id == 0:
        await callback.message.edit_text(
            "🛠 **Информация появится позже**\n\nСообщение еще не добавлено в канал.",
            reply_markup=get_back_button(back_to)
        )
        await callback.answer()
        return
    
    # Пересылаем сообщение из канала
    try:
        await bot.copy_message(
            chat_id=callback.message.chat.id,
            from_chat_id=CHANNEL_ID,
            message_id=message_id,
            reply_markup=get_back_button(back_to)
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка при пересылке {callback.data} (ID: {message_id}): {e}")
        await callback.message.edit_text(
            "❌ **Ошибка загрузки**\n\nНе удалось получить информацию. Попробуйте позже.",
            reply_markup=get_back_button(back_to)
        )
        await callback.answer()

# Обработчики для показа подменю
@dp.callback_query(lambda c: c.data == "menu_display")
async def show_display_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📱 **Выберите тип дисплея:**",
        reply_markup=display_menu
    )

@dp.callback_query(lambda c: c.data == "menu_battery")
async def show_battery_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🔋 **Выберите тип аккумулятора:**",
        reply_markup=battery_menu
    )

@dp.callback_query(lambda c: c.data == "menu_back_cover")
async def show_back_cover_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📦 **Выберите качество задней крышки:**",
        reply_markup=back_cover_menu
    )

@dp.callback_query(lambda c: c.data == "menu_case")
async def show_case_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🏠 **Выберите качество корпуса:**",
        reply_markup=case_menu
    )

@dp.callback_query(lambda c: c.data == "menu_waterproof")
async def show_waterproof_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "💧 **Выберите тип проклейки:**",
        reply_markup=waterproof_menu
    )

@dp.callback_query(lambda c: c.data == "menu_speakers")
async def show_speakers_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🔊 **Выберите тип динамиков:**",
        reply_markup=speakers_menu
    )

@dp.callback_query(lambda c: c.data == "menu_camera")
async def show_camera_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📸 **Выберите тип камеры:**",
        reply_markup=camera_menu
    )

@dp.callback_query(lambda c: c.data == "menu_cables")
async def show_cables_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🔌 **Выберите тип шлейфа:**",
        reply_markup=cables_menu
    )

@dp.callback_query(lambda c: c.data == "menu_apple_watch")
async def show_apple_watch_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "⌚ **Выберите запчасть для Apple Watch:**",
        reply_markup=apple_watch_menu
    )

# Обработчики для категорий без подменю (теперь пересылают сообщения)
@dp.callback_query(lambda c: c.data == "menu_glass")
async def show_glass(callback: types.CallbackQuery):
    await forward_from_channel(callback)

@dp.callback_query(lambda c: c.data == "menu_touchscreen")
async def show_touchscreen(callback: types.CallbackQuery):
    await forward_from_channel(callback)

@dp.callback_query(lambda c: c.data == "menu_display_frame")
async def show_display_frame(callback: types.CallbackQuery):
    await forward_from_channel(callback)

@dp.callback_query(lambda c: c.data == "menu_magsafe")
async def show_magsafe(callback: types.CallbackQuery):
    await forward_from_channel(callback)

# Возврат в главное меню
@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "👋 Выберите категорию:",
        reply_markup=main_menu
    )

# ================== ВЕБ-СЕРВЕР ДЛЯ RENDER ==================
async def health_check(request):
    """Эндпоинт для проверки здоровья бота"""
    return web.Response(text="Bot is running!")

async def webhook_handler(request):
    """Обработчик вебхуков (на будущее)"""
    return web.Response(text="Webhook received")

async def start_web_server():
    """Запуск веб-сервера для Render"""
    app = web.Application()
    app.router.add_get('/health', health_check)
    app.router.add_get('/', health_check)
    app.router.add_post('/webhook', webhook_handler)
    
    # Render передает порт через переменную окружения PORT
    port = int(os.environ.get('PORT', 8000))
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    logger.info(f"🌐 Веб-сервер запущен на порту {port}")
    return runner

async def main():
    # Запускаем веб-сервер в фоне
    web_runner = await start_web_server()
    
    # Запускаем бота
    logger.info("✅ Бот запущен!")
    logger.info(f"📊 ID канала: {CHANNEL_ID}")
    logger.info(f"📝 Загружено {len([v for v in MESSAGES.values() if v > 0])} сообщений")
    
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        # Очистка при остановке
        await web_runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())