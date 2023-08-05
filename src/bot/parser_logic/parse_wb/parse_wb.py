import csv

import requests
from aiogram import Bot

from aiogram.types import Message

from src.configuration import conf
from src.bot.parser_logic.parse_headers import headers
from src.bot.parser_logic.parse_wb.wb_parse_models import Items


class ParseWB:
    def __init__(self, url: str, message: Message):
        self.brand_id = self.__get_brand_id(url)
        self.message = message

    @staticmethod
    def __get_brand_id(url) -> str:
        find_id = url[::-1].find('/')
        brand_name = url[-find_id:]
        r = requests.get(
            f'https://static.wbstatic.net/data/brands/{brand_name}.json',
            headers=headers.create_headers()
        )
        brand_id = r.json()
        return str(brand_id['id'])

    async def parse(self):
        bot: Bot = Bot(token=conf.bot.token)
        page = 1
        self.__create_csv()
        await bot.send_message(self.message.from_user.id, 'Парсер запущен')
        while True:
            response = requests.get(
                f'https://catalog.wb.ru/brands/%D0%BA/catalog?appType=1&brand={self.brand_id}&curr=rub&dest=-1257786'
                f'&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,'
                f'114&sort=popular&spp=0&uclusters=0&limit=300&page={page}',
                headers=headers.create_headers(),
            )
            page += 1
            items_info = Items.model_validate(response.json()['data'])
            if not items_info.products:
                break
            self.__save_csv(items_info)

    @staticmethod
    def __create_csv():
        with open('../bot/wb_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'название', 'цена', 'бренд', 'скидка', 'рейтинг', 'в наличии', 'кол-во отзывов'])

    @staticmethod
    def __save_csv(items):
        with open('../bot/wb_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for product in items.products:
                writer.writerow(
                    [
                        product.id,
                        product.name,
                        product.salePriceU / 100,
                        product.brand,
                        product.sale,
                        product.reviewRating,
                        product.volume,
                        product.feedbacks,
                    ]
                )
