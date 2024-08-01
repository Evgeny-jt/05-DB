import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Shop, Stock, Sale  # , Publisher, Book, Shop, Stock, Sale

DSN ='postgresql://postgres:2024p09114@localhost:5432/BD06'
engine = sqlalchemy.create_engine(DSN)


create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()


publisher1 = Publisher(name='Пушкин')
publisher2 = Publisher(name='Толстой')
publisher3 = Publisher(name='Булгаков')
session.add_all([publisher1, publisher2, publisher3])
session.commit()


book1 = Book(title='Капитанская дочка', id_publisher=publisher1.id)
book2 = Book(title='Руслан и Людмила', id_publisher=publisher1.id)
book3 = Book(title='Евгений Онегин', id_publisher=publisher1.id)
book4 = Book(title='Война и мир', id_publisher=publisher2.id)
book5 = Book(title='Анна Каренина', id_publisher=publisher2.id)
book6 = Book(title='Кавказский пленик', id_publisher=publisher2.id)
book7 = Book(title='Мастер и Маргарита', id_publisher=publisher3.id)
book8 = Book(title='Собачье сердце', id_publisher=publisher3.id)
book9 = Book(title='Белая гвардия', id_publisher=publisher3.id)
session.add_all([book1, book2, book3, book4, book5, book6, book7, book8, book9])
session.commit()


shop1 = Shop(name='Буквоед')
shop2 = Shop(name='Лабиринт')
shop3 = Shop(name='Книжный дом')
session.add_all([shop1, shop2, shop3])
session.commit()

stock1 = Stock(id_book=book1.id,  id_shop=shop1.id, count=155)
stock2 = Stock(id_book=book2.id,  id_shop=shop1.id, count=115)
stock3 = Stock(id_book=book1.id,  id_shop=shop2.id, count=130)
stock4 = Stock(id_book=book3.id,  id_shop=shop3.id, count=170)
stock5 = Stock(id_book=book1.id,  id_shop=shop3.id, count=140)
stock6 = Stock(id_book=book8.id,  id_shop=shop2.id, count=130)
stock7 = Stock(id_book=book5.id,  id_shop=shop1.id, count=100)
stock8 = Stock(id_book=book9.id,  id_shop=shop2.id, count=140)
session.add_all([stock1, stock2, stock3, stock4, stock5, stock6, stock7, stock8,])
session.commit()

sale1 = Sale(prise=600, date_sale='09-11-2022', id_stock=stock1.id, count=15)
sale2 = Sale(prise=500, date_sale='08-11-2022', id_stock=stock2.id, count=11)
sale3 = Sale(prise=580, date_sale='05-11-2022', id_stock=stock3.id, count=13)
sale4 = Sale(prise=490, date_sale='02-11-2022', id_stock=stock4.id, count=10)
sale5 = Sale(prise=600, date_sale='26-10-2022', id_stock=stock5.id, count=11)
sale6 = Sale(prise=700, date_sale='22-10-2022', id_stock=stock6.id, count=14)
sale7 = Sale(prise=550, date_sale='16-10-2022', id_stock=stock7.id, count=11)
sale8 = Sale(prise=350, date_sale='06-10-2022', id_stock=stock8.id, count=17)
session.add_all([sale1, sale2, sale3, sale4, sale5, sale6, sale7, sale8])
session.commit()

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
