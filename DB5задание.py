import psycopg2
import pprint as p


def structureDB():
    with psycopg2.connect(database='DB5exercise', user='postgres', password='2024p09114') as conn:
        with conn.cursor() as cur:
            cur.execute("""
            DROP TABLE phoneNumber;
            DROP TABLE users;
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                surname VARCHAR(20) NOT NULL,
                name VARCHAR(20) NOT NULL,
                email VARCHAR(40) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS phoneNumber(
                nomer_id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                number VARCHAR(16) NOT NULL
            );
            """)
    #     conn.commit()
    # conn.close()


def new_client(surname, name, email):
    with psycopg2.connect(database='DB5exercise', user='postgres', password='2024p09114') as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO users(surname, name, email) values(%s, %s, %s) RETURNING *;
            """, (surname, name, email))
            print('создана запись в таблице USERS: ', cur.fetchone())


def add_phone(user_id, number):
    with psycopg2.connect(database='DB5exercise', user='postgres', password='2024p09114') as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO phoneNumber(user_id, number) values(%s, %s) RETURNING *;
                """, (user_id, number))
            print('В таблицу phoneNUMBER добавлен новый номер телефона: ', cur.fetchone())


def update_user(surname, surname_update=None, name=None, email=None, number=None):
    print('ИЗМЕНЕНИЕ ДАННЫХ КЛИЕНТА')
    with psycopg2.connect(database='DB5exercise', user='postgres', password='2024p09114') as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, surname, name, email, number FROM users u
                lEFT JOIN phoneNumber pn ON pn.user_id = u.id
                WHERE surname = %s;
                """, (surname,))
            data_user = cur.fetchall()
            if surname_update != None and surname_update != data_user[0][1]:
                cur.execute("""
                    UPDATE users
                    SET surname=%s
                    WHERE id=%s;
                    """, (surname_update, data_user[0][0],))
                print('Изменили Фамилию на ', surname)
            else:
                print('ФАМИЛИЯ не изменилась')

            if name != None or name != data_user[0][2]:
                cur.execute("""
                    UPDATE users
                    SET name=%s
                    WHERE id=%s;
                    """, (name, data_user[0][0],))
                print('Изменили ИМЯ на ', name)
            else:
                print('ИМЯ не изменилась')

            if email != None or email != data_user[0][3]:
                cur.execute("""
                    UPDATE users
                    SET email=%s
                    WHERE id=%s;
                    """, (email, data_user[0][0],))
                print('Изменили EMAIL на', email)
            else:
                print('EMAIL не изменился')

            if number != None:
                cur.execute("""
                    SELECT count(user_id)
                    FROM phoneNumber
                    WHERE user_id=%s
                    """, (data_user[0][0],))
                quantity_number = cur.fetchall()[0][0]
                if quantity_number > 1:  # изменяем первый номер телефона
                    cur.execute("""
                        SELECT nomer_id, number
                        FROM phoneNumber
                        WHERE user_id=%s
                        LIMIT 1
                        """, (data_user[0][0],))
                    data_ph = cur.fetchall()
                    print(data_ph)
                    cur.execute("""
                        UPDATE phoneNumber
                        SET number=%s
                        WHERE nomer_id=%s
                        """, (number, data_ph[0][0],))
                    print('Изменили ТЕЛЕФОН на', number)
                elif quantity_number == 1:
                    cur.execute("""
                        SELECT nomer_id, number
                        FROM phoneNumber
                        WHERE user_id=%s
                        LIMIT 1
                        """, (data_user[0][0],))
                    data_ph = cur.fetchall()
                    cur.execute("""
                        UPDATE phoneNumber
                        SET number=%s
                        WHERE nomer_id=%s
                        """, (number, data_ph[0][0],))
                    print('Изменили ТЕЛЕФОН на ', number)
                else:
                    print('У клиента в базе еще не было номера телефона, добавим', number)
                    add_phone(data_user[0][0], number)


def phone_delete(surname):
    user_id = looking_client(
        client_data=surname)  ## находим id клиента по фамилии номер телефона которого нужно удалить
    if user_id != []:
        delete_number = del_number(
            user_id=user_id)  # если у клиента больше одного номера выесняем какой именно нужно удалить
        if delete_number != 'no':
            with psycopg2.connect(database='DB5exercise', user='postgres', password='2024p09114') as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        DELETE FROM phoneNumber
                        WHERE number=%s;
                        """, (delete_number,))
                    cur.execute("""
                        SELECT * FROM phoneNumber;
                        """)
                    print('результат после удаления', cur.fetchall())
        else:
            print('У клиента с фамилией', surname, 'нет в телефоного номера в базе данных')
    else:
        print('Клиента с фамилией', surname, 'нет в базе данных')


def del_number(user_id):
    numbers_user = quantity_number(user_id)
    if len(numbers_user) == 0:
        del_number = 'no'
    elif len(numbers_user) == 1:
        del_number = numbers_user[0][0]
        print(del_number, 'его удалим')
    else:
        print('У клиента несколько номеров', numbers_user)
        del_number = input('Введите номер который нужно удалить: ')
    return del_number


def looking_client(client_data):  # ищем клиента по фамилии
    with psycopg2.connect(database='DB5exercise', user='postgres', password='2024p09114') as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, surname, name, email, number FROM users u
                left join phoneNumber pn on pn.user_id = u.id
                WHERE surname = %s OR name = %s OR email = %s OR number = %s;
                """, (client_data, client_data, client_data, client_data,))
            user_id = cur.fetchall()
    return user_id


def quantity_number(user_id):  # проверяем сколько у клиента номеров
    with psycopg2.connect(database='DB5exercise', user='postgres', password='2024p09114') as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT number FROM phoneNumber
                WHERE user_id = %s;
                """, (user_id[0][0],))
            user_phone = cur.fetchall()
    return user_phone


def delete_user(surname):
    user_id = looking_client(
        client_data=surname)  ## находим id клиента по фамилии номер телефона которого нужно удалить
    print("информация о удаляемом клиенте", user_id)
    if user_id != []:
        print('Наши клиента удалим его')
        with psycopg2.connect(database='DB5exercise', user='postgres', password='2024p09114') as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM phoneNumber
                    WHERE user_id=%s;
                    """, (user_id[0][0],))
                cur.execute("""
                    SELECT * FROM phoneNumber;
                    """)
                print('результат после удаления', cur.fetchall())
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM users
                    WHERE id=%s;
                    """, (user_id[0][0],))
                cur.execute("""
                    SELECT * FROM users;
                    """)
                print('результат после удаления', cur.fetchall())
    else:
        print('Клиента с фамилией', surname, 'нет в базе данных')


if __name__ == '__main__':
    structureDB()

    new_client(name='Владимр', surname='Путин', email='putin@kreml.ru')
    new_client(surname='Медведев', name='Дима', email='медведь')
    new_client(surname='Набиулина', name='Эльвира', email='nabiylina@cbrf.ru')
    new_client(surname='Орешкин', name='Максим', email='oreshkin@cbrf.ru')

    add_phone(user_id=1, number='+7-001')
    add_phone(user_id=2, number='+7-101')
    add_phone(user_id=1, number='+7-100')
    add_phone(user_id=4, number='+7-200')
    add_phone(user_id=3, number='+7-555')

    update_user(surname='Медведев', name='Дмитрий', email='medvedev@kreml.ru', number='+7-999')

    phone_delete(surname='Путин')
    phone_delete(surname='Набиулина')

    delete_user(surname='Орешкин')

    search = input('Поиск клиента по его данным. Введите фамилию, почту или телефон: ')
    print('Результат поиска: ', looking_client(client_data=search)[0])

    print('База данных после всех изменений')
    with psycopg2.connect(database='DB5exercise', user='postgres', password='2024p09114') as conn:
        with conn.cursor() as cur:
            cur.execute("""
                     SELECT surname, name, email, number FROM users u
                     LEFT JOIN phoneNumber pn ON pn.user_id = u.id;
                     """)
            p.pprint(cur.fetchall())
