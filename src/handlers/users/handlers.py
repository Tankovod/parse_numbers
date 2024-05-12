from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.enums.content_type import ContentType
from sqlalchemy.exc import IntegrityError

from src.utils.parser import Parser
from .router import router
from src.models import User, Number
from src.tasks import task_user_send
from src.keyboards.inline.k1 import create_k
from src.keyboards.inline.k1 import MyCallbackData


@router.message(F.text == '/start')
async def start(message: Message):
    user = User(id=message.from_user.id)
    text = ''
    try:
        await user.save()
    except IntegrityError:
        text = 'Давно не виделись!'
    else:
        text = 'Добро пожаловать!'
    finally:
        await message.answer(text=text)
    # objs = await Parser.run()
    # if objs:
    #     text = '\n'.join(number.number for number in objs)
    #     await message.answer(text=text)


@router.message(F.text == '/dump')
async def dump(message: Message):
    task_user_send.delay(message.from_user.id)


# @router.callback_query(MyCallbackData.filter())
# async def callback_handler(callback: CallbackQuery, callback_data: MyCallbackData):
#     await callback.answer(text='456789865678909876556789')


@router.message(F.content_type == ContentType.CONTACT)
async def get_contact(message: Message):
    print(message.contact)


@router.message(F.content_type == ContentType.LOCATION)
async def get_contact(message: Message):
    print(message.location)


@router.callback_query(MyCallbackData.filter(F.action == 'page'))
async def callback_handler2(callback: CallbackQuery, callback_data: MyCallbackData):
    await callback.message.edit_reply_markup(
        reply_markup=await create_k(page=callback_data.page)
    )


@router.callback_query(MyCallbackData.filter(F.action == 'get'))
async def select_number(callback: CallbackQuery, callback_data: MyCallbackData):
    async with Number.session() as session:
        number = await session.get(Number, callback_data.number_id)
    await callback.message.edit_text(
        text=f'{number.number}'
    )
