import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
GURUH_CHAT_ID = int(os.getenv("GURUH_CHAT_ID", "0"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def send_budget_link():
    try:
        # Guruhda chiquvchi asosiy matn
        matn = (
            "🇺🇿 **OPEN BUDGET — OVOZ BERISH BOSHLANDI!**\n\n"
            "Hurmatli fuqaro! Open Budget loyihasiga ovoz berish jarayonlari davom etmoqda. "
            "O'z ovozingizni qishlog'imiz ravnaqi va rivoji uchun ayamaysiz degan umiddamiz.\n\n"
            "Bizni oxirgi manzilga eltuvchi ko'chalarimiz 🚘 **ASFALT BO'LISHI UCHUN** ovoz berishingizni so'raymiz! 🙏\n\n"
            "Murojaat va ovoz berish bo'yicha yordam kerak bo'lsa, ushbu raqamlarga qo'ng'iroq qiling (7/24 faol):\n"
            "☎️ +998950760222\n"
            "☎️ +998972130304\n"
            "☎️ +998950278779\n\n"
            "Kim qachon bo'lsa ham telefon qilaversin, sizning ovozingiz biz uchun juda muhim! ✨\n\n"
            "👇👇 **OVOZ BERISH UCHUN PASTDAGI KATTA TUGMALARNI BOSING** 👇👇"
        )
        
        # Siz taqdim etgan to'g'ri va aniq havola
        OPEN_BUDGET_TARGET_URL = "https://new.openbudget.uz/uz/initiative-budget/active-initiatives/55/b773e0e7-b83f-40c7-998a-9bba8e2401c2"
        
        # Tugmalarni yaqqol ko'rinishi uchun 2 qatorli ulkan dizaynda yaratamiz
        havola_tugmasi = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📢 OVOZ BERISH SAHIFASIGA O'TISH 📢", 
                        url=OPEN_BUDGET_TARGET_URL
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🛑 SIZNING OVOZINGIZ SHU YERDA! BOSING 🛑", 
                        url=OPEN_BUDGET_TARGET_URL
                    )
                ]
            ]
        )
        
        # Guruhga yuborish qismi
        await bot.send_message(
            chat_id=GURUH_CHAT_ID, 
            text=matn, 
            parse_mode="Markdown", 
            reply_markup=havola_tugmasi,
            disable_web_page_preview=True  # Ortiqcha rasm chiqib joyni band qilmasligi uchun
        )
        logging.info("Yangilangan ulkan tugmali xabar muvaffaqiyatli yuborildi.")
        
    except Exception as e:
        logging.error(f"Xabar yuborishda xatolik yuz berdi: {e}")

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply("Bot muvaffaqiyatli yangilandi va faol ishlamoqda!")

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
    asyncio.run(main())

