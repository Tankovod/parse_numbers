from typing import Literal, Optional
from math import ceil

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from pydantic import PositiveInt

from src.models import Number
from src.database import Base
from sqlalchemy import select
from sqlalchemy.sql.functions import count


class MyCallbackData(CallbackData, prefix='my'):
    number_id: Optional[int]
    page: PositiveInt
    action: Literal['page', 'get']


async def create_k(page: int = 1, paginate_by: int = 5):
    async with Number.session() as session:
        objs_count = await session.scalar(
            select(count(Number.id))
        )
        max_page = ceil(objs_count / paginate_by)
        objs = await session.scalars(
            select(Number)
            .order_by(Number.id)
            .limit(paginate_by)
            .offset(page * paginate_by - paginate_by)
        )
        buttons = [
            [
                InlineKeyboardButton(
                    text=f'{obj.number}',
                    callback_data=MyCallbackData(
                        number_id=obj.id,
                        page=page,
                        action='get'
                    ).pack()
                )
            ]
            for obj in objs
        ]
        if max_page > 1:
            buttons += [
                [
                    InlineKeyboardButton(
                        text='PREV',
                        callback_data=MyCallbackData(
                            action='page',
                            page=(page - 1) if page > 1 else max_page
                        ).pack()
                    ),
                    InlineKeyboardButton(
                        text='NEXT',
                        callback_data=MyCallbackData(
                            action='page',
                            page=(page + 1) if page < max_page else 1
                        ).pack()
                    ),
                ]
            ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
