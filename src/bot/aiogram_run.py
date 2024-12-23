import asyncio
from src.bot.create_bot import bot, dp
from src.bot.routers import form_router, menu_router, setting_router, searching_router, coworker_router


async def main() -> None:
    dp.include_routers(form_router, menu_router, setting_router, searching_router, coworker_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
