from asyncio import sleep
from http import HTTPStatus
from typing import List

from src.settings import URLS
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError

from src.models import Number

# URLS = (
#     ('/filter?sort=4', 'https://cars.av.by', ),
#     ('/filter?page=2&sort=4', 'https://cars.av.by'),
#     # ('https://truck.av.by/filter?sort=4', 'https://truck.av.by'),
#     # ('https://moto.av.by/filter?sort=4', 'https://moto.av.by'),
#     # ('https://moto.av.by/filter?page=2&sort=4', 'https://moto.av.by'),
#     # ('https://bus.av.by/filter?sort=4', 'https://bus.av.by'),
# )

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Content-Type": "text/html; charset=utf-8",
    "Accept": "text/html, application/xhtml+xml, */*",
}


class Parser:

    @classmethod
    async def get_ids(cls, url: str, path_params: str = None, **query) -> list[str]:
        async with ClientSession(base_url=url, headers=headers) as session:
            async with session.get(
                url=path_params,
                params=query,
            ) as response:
                if response.status == HTTPStatus.OK:
                    response_text = await response.text()

                    soup = BeautifulSoup(response_text, 'lxml')

                    links = soup.find_all(attrs={'class': 'listing-item__link'})
                    print(links)
                    return [link['href'].split('/')[-1] for link in links]

    @classmethod
    async def get_numbers(cls, ids: list[str]) -> list[str]:
        phone_car = []
        # await message.answer(f'Сбор данных с {site_search_url}...', disable_web_page_preview=True)
        async with ClientSession(base_url='https://api.av.by', headers=headers) as session:
            for i in ids:
                url1 = f'/offers/{i}/phones'
                async with session.get(
                    url=url1
                ) as response:
                    if response.status == HTTPStatus.OK:
                        data = await response.json()
                        phone_car.append(data[0].get('country')['code'] + data[0].get('number'))
                await sleep(0.5)
        return phone_car

    @classmethod
    async def check_urls(cls) -> str:
        id_s = []

        for url in URLS:
            id_s.extend(await cls.get_ids(url=url[1], path_params=url[0]))

        answer = ''
        for number in await cls.get_numbers(id_s):
            answer += '\n' + number

        return answer

    @classmethod
    async def run(cls):
        id_s = []

        for url in URLS:
            r = await cls.get_ids(url=url[1], path_params=url[0])
            if r:
                id_s.extend(r)

        lst = await cls.get_numbers(id_s)
        return await cls.save(lst)

    @classmethod
    async def save(cls, numbers: List[str]) -> List[Number]:
        new_numbers = []
        for number in numbers:
            number = Number(number=number)
            try:
                await number.save()
            except IntegrityError:
                pass
            else:
                new_numbers.append(number)
        return new_numbers
# f = run(Parser.check_urls())
# # f = await Parser.check_urls()
# print(f)
# print(len(f))
