from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from src.settings import dp, bot
from src.handlers.users.handlers import router as users_router
from logging import basicConfig, INFO

basicConfig(level=INFO)


async def on_startup():
    await bot.set_my_commands(
        commands=[
            BotCommand(command='/start', description='Start'),
            BotCommand(command='/dump', description='Receive numbers')
        ],
        scope=BotCommandScopeAllPrivateChats(),
        language_code='en'
    )
    await bot.set_my_commands(
        commands=[
            BotCommand(command='/start', description='Старт'),
            BotCommand(command='/dump', description='Получить номера')
        ],
        scope=BotCommandScopeAllPrivateChats(),
        language_code='ru'
    )

if __name__ == '__main__':
    dp.include_router(router=users_router)
    dp.startup.register(on_startup)
    dp.run_polling(bot)
