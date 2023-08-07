from io import BytesIO

from asyncio import get_event_loop
from itertools import count

from aiogram.types import BufferedInputFile
from sqlalchemy import select

from .settings import celery, bot
from .utils.parser import Parser
from .models import UserNumber, Number


@celery.task
def task_parser():
    async def _task_parser():
        await Parser.run()

    loop = get_event_loop()
    loop.run_until_complete(_task_parser())


@celery.task
def task_user_send(user_id: int):
    async def _task_user_send():
        async with Number.session() as session:
            user_numbers = await session.scalars(select(UserNumber).filter(UserNumber.user_id == user_id))
            numbers = await session.scalars(
                select(Number)
                .filter(Number.id.not_in([user_number.number_id for user_number in user_numbers]))
            )
            numbers = numbers.all()
            user_numbers = [UserNumber(user_id=user_id, number_id=number.id) for number in numbers]
            text = ''
            number_count = len(numbers)

            for number in numbers:
                text += f'{number.number}\n'
            for number in user_numbers:
                try:
                    await number.save()
                except:
                    pass

            if text:
                file = BytesIO()
                file.write(text.encode())
                file.seek(0)
                try:
                    await bot.send_message(
                        chat_id=user_id,
                        text=f'Новых номеров: {number_count}'
                    )
                    await bot.send_document(
                        chat_id=user_id,
                        document=BufferedInputFile(file=file.getvalue(), filename='numbers.txt')
                    )
                except:
                    pass
            else:
                try:
                    await bot.send_message(
                        chat_id=user_id,
                        text='Новых номеров нет!'
                    )
                except:
                    pass

    loop = get_event_loop()
    loop.run_until_complete(_task_user_send())
