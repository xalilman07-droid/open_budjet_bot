import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Vergul orqali yozilgan guruh ID raqamlarini to'g'ri ro'yxatga ajratib olamiz
GURUH_CHAT_IDS = [int(i.strip()) for i in os.getenv("GURUH_CHAT_ID", "0").split(",") if i.strip()]

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def send_budget_link():
    if not GURUH_CHAT_IDS:
        logging.warning("Hech qanday guruh ID raqamlari kiritilmagan!")
        return

    try:
        # Bizni oxirgi manzilga eltuvchi... gapi olib tashlangan toza va chiroyli matn (HTML formatida)
        matn = (
            "🇺🇿 <b>OPEN BUDGET — OVOZ BERISH BOSHLANDI!</b>\n\n"
            "Hurmatli fuqaro! Open Budget loyihasiga ovoz berish jarayonlari davom etmoqda. "
            "O'z ovozingizni qishlog'imiz ravnaqi va rivoji uchun ayamaysiz degan umiddamiz.\n\n"
            "Ko'chalarimiz 🚘 <b>ASFALT BO'LISHI UCHUN</b> ovoz berishingizni so'raymiz! 🙏\n\n"
            "Murojaat va ovoz berish bo'yicha yordam kerak bo'lsa, ushbu raqamlarga qo'ng'iroq qiling (7/24 faol):\n"
            "☎️ +998950760222\n"
            "☎️ +998972130304\n"
            "☎️ +998950278779\n\n"
            "Kim qachon bo'lsa ham telefon qilaversin, sizning ovozingiz biz uchun juda muhim! ✨\n\n"
            "👇👇 <b>QUYIDAGI ULKAN TUGMANI BOSING</b> 👇👇"
        )
        
        # SIZ BERGAN ANIQ VA TO'G'RI OVOZ BERISH HAVOLASI (HTMLda chiziqchalar xato bermaydi)
        OPEN_BUDGET_TARGET_URL = "https://openbudget.uz"
        
        # Ulkan tugma ko'rinishi
        havola_tugmasi = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔗 OVOZ BERISH UCHUN BU YERGA BOSING 🔗", 
                        url=OPEN_BUDGET_TARGET_URL
                    )
                ]
            ]
        )
        
        # Har bir guruhga xabarni yuborish
        for chat_id in GURUH_CHAT_IDS:
            try:
                await bot.send_message(
                    chat_id=chat_id, 
                    text=matn, 
                    parse_mode="HTML",  # Markdown xatolaridan qochish uchun HTML tanlandi
                    reply_markup=havola_tugmasi,
                    disable_web_page_preview=True
                )
                logging.info(f"Xabar {chat_id} guruhiga muvaffaqiyatli yuborildi.")
            except Exception as group_error:
                logging.error(f"{chat_id} guruhiga yuborishda xatolik: {group_error}")
        
    except Exception as e:
        logging.error(f"Umumiy xatolik yuz berdi: {e}")

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply("Bot faol ishlamoqda!")

async def handle(request):
    return web.Response(text="Open Budget Bot is online!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", "8080"))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_budget_link, "interval", minutes=5)
    scheduler.start()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run=True
    import asyncio
    asyncio.run(main())

