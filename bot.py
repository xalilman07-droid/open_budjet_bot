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
            "👇👇 **QUYIDAGI KATTA TUGMANI BOSING** 👇👇"
        )
        
        havola_tugmasi = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔗 OVOZ BERISH UCHUN BU YERGA BOSING 🔗", 
                        url="https://openbudget.uz"
                    )
                ]
            ]
        )
        
        await bot.send_message(
            chat_id=GURUH_CHAT_ID, 
            text=matn, 
            parse_mode="Markdown", 
            reply_markup=havola_tugmasi,
            disable_web_page_preview=True
        )
        logging.info("Xabar guruhga muvaffaqiyatli yuborildi.")
        
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")

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
    asyncio.run(main())
