import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import Publisher, Book, Shop, Stock, Sale


def leveling(words, word):   # Выравнваем длинну слова до максимально длиного (добовляем пробелы)
    if max(words) >= len(word):
        number_of_spaces = max(words) - len(word)
    new_word = word
    for _ in range(0, number_of_spaces):
        new_word += ' '
    return new_word


DSN = 'postgresql://postgres:2024p09114@localhost:5432/BD06'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

publisher = input('Для вывода списка купленных книг издатля. Введите автора: ')
print('У автора', publisher, 'купили : ')

len_book = []
len_shop = []
len_prise = []
for p, book, shop, prise in session.query(Publisher, Book.title, Shop.name, Sale.prise).join(Book).join(Stock).join(
        Shop).join(Sale).filter(Publisher.name == publisher):
    len_book.append(len(book))
    len_shop.append(len(shop))
    len_prise.append(len(str(prise)))

for p, b, sh, pr, d in session.query(Publisher, Book.title, Shop.name, Sale.prise, Sale.date_sale).join(Book).join(
        Stock).join(Shop).join(Sale).filter(Publisher.name == publisher):
    new_b = leveling(words=len_book, word=b)
    new_sh = leveling(words=len_shop, word=sh)
    new_pr = leveling(words=len_prise, word=str(pr))
    print(new_b, '|', new_sh, '|', new_pr, '|', d)

session.close()
