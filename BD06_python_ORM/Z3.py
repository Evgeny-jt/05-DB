import requests
import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Shop, Stock, Sale


def open_file(name):
    print('Открываем файл ', name)
    with open(f'{name}.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    return json_data

def save_bd(model, id, param):
    if model == 'publisher':
        publisher = Publisher(name=param['name'])
        session.add(publisher)
        session.commit()
    elif model == 'book':
        book = Book(title=param['title'], id_publisher=param['id_publisher'])
        session.add(book)
        session.commit()
    elif model == 'shop':
        shop = Shop(name=param['name'])
        session.add(shop)
        session.commit()
    elif model == 'stock':
        stock = Stock(id_book=param['id_book'], id_shop=param['id_shop'], count=param['count'])
        session.add(stock)
        session.commit()
    elif model == 'sale':
        sale = Sale(prise=param['price'], date_sale=param['date_sale'], id_stock=param['id_stock'], count=param['count'])
        session.add(sale)
        session.commit()
    else:
        print('Неизвестная МОДЕЛЬ')



data_file = open_file(name='tests_data')

DSN = 'postgresql://postgres:2024p09114@localhost:5432/BD06'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

print('Вносим изменение а таблици базы данных')
for data in data_file:
    # print(data['model'])
    model = data['model']
    pk = data['pk']
    param = data['fields']
    # print(model, id)
    # print(param)
    save_bd(model=model, id=pk, param=param)

print('Изменение внесены')

view = input('Чтобы посмотреть созданную базу данных напиши ДА ')
if view == 'да' or view == 'ДА':
    print('---BD---')
    print('--Авторы')
    for i in session.query(Publisher).all():
        print(i)
    print('--Книги')
    for i in session.query(Book).all():
        print(i)
    print('--Магазины')
    for i in session.query(Shop).all():
        print(i)
    print('--Стоки')
    for i in session.query(Stock).all():
        print(i)
    print('--Продажи')
    for i in session.query(Sale).all():
        print(i)
else:
    print('ВЫ решини не смотреть базу данны потому что введено: ', view)




session.close()
