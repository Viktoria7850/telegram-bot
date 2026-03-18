import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Берем токен из переменных окружения (обязательно для Bothost.ru!)
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("❌ Токен не найден! Добавьте TOKEN в переменные окружения")

# ID канала lcd_stock_34
CHANNEL_ID = -1003832030735

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

# ================== ПОСТОЯННАЯ КНОПКА ВОЗВРАТА ==================
def get_main_menu_button():
    """Создает Reply-кнопку для возврата в главное меню"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🏠 Главное меню")]],
        resize_keyboard=True,
        is_persistent=True  # Кнопка остается всегда
    )
    return keyboard

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
    [InlineKeyboardButton(text="🔥 Fog", callback_data="display_fog")],
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
    "display_original": 9,
    "display_used_original": 45,
    "display_fog": 17,
    "display_hard_oled": 16,
    "display_soft_oled": 15,
    "display_tft": 11,
    "display_incell": 46,
    
    # Аккумуляторы
    "battery_full": 14,
    "battery_cell": 13,
    "battery_program": 12,
    
    # Задняя крышка
    "back_original": 47,
    "back_used_original": 48,
    "back_copy": 49,
    
    # Корпус
    "case_original": 50,
    "case_used_original": 51,
    
    # Проклейка
    "waterproof_back": 22,
    "waterproof_front": 53,
    
    # Динамики
    "speakers_top": 29,
    "speakers_bottom": 54,
    
    # Камера
    "camera_front": 56,
    "camera_rear": 26,
    
    # Другие категории
    "menu_glass": 23,
    "menu_touchscreen": 24,
    "menu_display_frame": 27,
    "menu_magsafe": 28,
    
    # Шлейфы
    "cable_wifi": 57, "cable_gps": 58, "cable_gsm": 59,
    "cable_light_mic": 60, "cable_light": 61,
    "cable_wireless_flash": 62, "cable_power_vol_wireless": 63,
    "cable_wireless_vol": 64, "cable_mic": 65, "cable_flash": 66,
    "cable_power": 67, "cable_vol": 68, "cable_magsafe": 69,
    "cable_bluetooth": 70, "cable_sim": 71, "cable_vibrator": 72,
    "cable_front_speaker": 73, "cable_lidar": 74, "cable_home": 75,
    "cable_charging": 76,
    
    # Apple Watch
    "watch_battery": 31,
    "watch_display": 0,
    "watch_back": 32,
    "watch_case": 0,
    "watch_glass": 30,
    "watch_touch": 33,
}

# Текст с информацией о магазине (только для подменю)
SHOP_INFO = "\n\n📞 Обращайтесь 🤝\n+7 (927) 537-43-40\n@Lcdstock34\n\nг. Волгоград, пр-т им.В.И. Ленина, 15\nВход TESLA"

# Текст приветствия после нажатия /start
WELCOME_TEXT = """Добро пожаловать в магазин запчастей LCD34 👋
Нажмите кнопку '🏠 Главное меню' внизу экрана, чтобы начать работу.

Обращайтесь 🤝
+7 (927) 537-43-40
@Lcdstock34

г. Волгоград, пр-т им.В.И. Ленина, 15 
Вход TESLA"""

# ================== ОБРАБОТЧИКИ ==================
@dp.message(Command("start"))
async def start(message: types.Message):
    # Отправляем приветствие с постоянной кнопкой "Главное меню"
    sent_message = await message.answer(
        WELCOME_TEXT,
        reply_markup=get_main_menu_button()
    )
    
    # Пытаемся закрепить сообщение (если бот имеет права администратора)
    try:
        await bot.pin_chat_message(
            chat_id=message.chat.id,
            message_id=sent_message.message_id
        )
    except Exception as e:
        logger.info(f"Не удалось закрепить сообщение: {e}")
    
    # Отправляем главное меню
    await message.answer(
        "Выберите категорию:",
        reply_markup=main_menu
    )

# Обработчик для кнопки "Главное меню"
@dp.message(lambda message: message.text == "🏠 Главное меню")
async def return_to_main_menu(message: types.Message):
    await message.answer(
        "Выберите категорию:",
        reply_markup=main_menu
    )

# ВАЖНО: Убираем обработчик всех сообщений, чтобы не мешать работе бота
# Теперь бот будет отвечать ТОЛЬКО на команду /start и нажатие кнопки "Главное меню"
# Все остальные сообщения будут игнорироваться (Telegram сам покажет кнопку START)

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
    
    if message_id == 0:
        await callback.message.edit_text(
            "🛠 **Информация появится позже**",
            reply_markup=get_back_button(back_to)
        )
        await callback.answer()
        return
    
    try:
        # Копируем сообщение из канала
        await bot.copy_message(
            chat_id=callback.message.chat.id,
            from_chat_id=CHANNEL_ID,
            message_id=message_id,
            reply_markup=get_back_button(back_to)
        )
        # Отправляем информацию о магазине ТОЛЬКО после товара
        await callback.message.answer(SHOP_INFO)
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await callback.answer("❌ Ошибка загрузки")

# Обработчики меню
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

@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Выберите категорию:",
        reply_markup=main_menu
    )

async def main():
    logger.info("✅ Бот запущен!")
    logger.info(f"📊 ID канала: {CHANNEL_ID}")
    logger.info(f"📝 Загружено {len([v for v in MESSAGES.values() if v > 0])} сообщений")
    
    # Устанавливаем команды бота (чтобы кнопка START появилась)
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Запустить бота / Главное меню")
    ])
    
    # Удаляем вебхук перед запуском поллинга
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())