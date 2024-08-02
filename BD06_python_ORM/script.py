import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import Publisher, Book, Shop, Stock, Sale


def get_shops(search): #Функция принимает обязательный параметр

    DSN = 'postgresql://postgres:2024p09114@localhost:5432/BD06'
    engine = sqlalchemy.create_engine(DSN)

    Session = sessionmaker(bind=engine)
    db_session = Session()

    rez = db_session.query( #Создаем общее тело запроса на выборку данных и сохраняем в переменную
        Book.title, Shop.name, Sale.prise, Sale.date_sale, #Название книги, имя магазина, стоимость продажи и дату продажи
    ).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)
    if search.isdigit(): #Проверяем переданные данные в функцию на то, что строка состоит только из чисел
        found_publisher = db_session.query(Publisher.id, Publisher.name).filter(Publisher.id == search).all() #Обращаемся к запросу, который составили ранее, и применяем фильтрацию, где айди публициста равно переданным данным в функцию, и сохраняем в переменную
    else:
        found_publisher = db_session.query(Publisher.id, Publisher.name).filter(Publisher.name == search).all() #Обращаемся к запросу, который составили ранее, и применяем фильтрацию, где имя публициста равно переданным данным в функцию, и сохраняем в переменную
    for name, shop, sale, date in rez.filter(Publisher.id == found_publisher[0][0] or Publisher.name == found_publisher[0][1]).all(): #Проходим в цикле по переменой, в которой сохраняем результат фильтрации, и при каждой итерации получаем кортеж и распаковываем значения в 4 переменные
        print(f"{name: <40} | {shop: <15} | {sale: <8} | {date}") #Передаем в форматированную строку переменные, которые содержат имя книги, название магазина, стоимость продажи и дату продажи

    db_session.close()





def leveling(words, word):   # Выравнваем длинну слова до максимально длиного (добовляем пробелы)
    if max(words) >= len(word):
        number_of_spaces = max(words) - len(word)
    new_word = word
    for _ in range(0, number_of_spaces):
        new_word += ' '
    return new_word


if __name__ == '__main__':
    search = input('Для вывода списка купленных книг издатля. Введите автора или его id: ') #Просим клиента ввести имя или айди публициста и данные сохраняем в переменную
    get_shops(search=search) #Вызываем функцию получения данных из базы, передавая в функцию данные, которые ввел пользователь строкой выше