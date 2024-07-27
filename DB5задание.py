import psycopg2

def structureDB():
    conn = psycopg2.connect(database='DB5exercise', user='postgres', password='2024p09114')
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
        conn.commit()
    conn.close()

def new_client(surname, name, email):
    conn = psycopg2.connect(database='DB5exercise', user='postgres', password='2024p09114')
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO users(surname, name, email) values(%s, %s, %s) RETURNING *;
        """, (surname, name, email))
        print('создана запись в таблице USERS: ', cur.fetchone())
    conn.commit()
    conn.close()

def add_phone(user_id, number):
    conn = psycopg2.connect(database='DB5exercise', user='postgres', password='2024p09114')
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phoneNumber(user_id, number) values(%s, %s) RETURNING *;
            """, (user_id, number))
        print('телефон добавлен phoneNUMBER: ', cur.fetchone())
    conn.commit()
    conn.close()

def update_user(user_id, surname, name, email):
    conn = psycopg2.connect(database='DB5exercise', user='postgres', password='2024p09114')
    with conn.cursor() as cur:
        cur.execute("""
               UPDATE users SET surname=%s, name=%s, email=%s WHERE id=%s;
               """, (surname, name, email, user_id,))
        cur.execute("""
               SELECT * FROM users;
               """)
        print(cur.fetchall())
    conn.commit()
    conn.close()

def phone_delete(surname):
    user_id=looking_client(client_data=surname) ## находим id клиента по фамилии номер телефона которого нужно удалить
    if user_id != []:
        delete_number = del_number(user_id=user_id)  # если у клиента больше одного номера выесняем какой именно нужно удалить
        if delete_number != 'no':
            conn = psycopg2.connect(database='DB5exercise', user='postgres', password='2024p09114')
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM phoneNumber
                    WHERE number=%s;
                    """, (delete_number,))
                cur.execute("""
                       SELECT * FROM phoneNumber;
                       """)
                print('результат после удаления', cur.fetchall())
            conn.commit()
            conn.close()
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
    conn = psycopg2.connect(database='DB5exercise', user='postgres', password='2024p09114')
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, surname, name, email, number FROM users u
            left join phoneNumber pn on pn.user_id = u.id
            WHERE surname = %s OR name = %s OR email = %s OR number = %s;
            """, (client_data, client_data, client_data, client_data,))
        user_id = cur.fetchall()
    conn.close()
    return user_id

def quantity_number(user_id): #проверяем сколько у клиента номеров
    conn = psycopg2.connect(database='DB5exercise', user='postgres', password='2024p09114')
    with conn.cursor() as cur:
        cur.execute("""
            SELECT number FROM phoneNumber
            WHERE user_id = %s;
            """, (user_id[0][0],))
        user_phone = cur.fetchall()
    conn.close()
    return user_phone


def delete_user(surname):
    user_id=looking_client(client_data=surname) ## находим id клиента по фамилии номер телефона которого нужно удалить
    print("информация о удаляемом клиенте", user_id)
    if user_id != []:
        print('Наши клиента удалим его')
        conn = psycopg2.connect(database='DB5exercise', user='postgres', password='2024p09114')
        with conn.cursor() as cur:
            cur.execute("""
                            DELETE FROM phoneNumber
                            WHERE user_id=%s;
                            """, (user_id[0][0],))
            cur.execute("""
                               SELECT * FROM phoneNumber;
                               """)
            print('результат после удаления', cur.fetchall())
        conn.commit()
        with conn.cursor() as cur:
            cur.execute("""
                            DELETE FROM users
                            WHERE id=%s;
                            """, (user_id[0][0],))
            cur.execute("""
                               SELECT * FROM users;
                               """)
            print('результат после удаления', cur.fetchall())
        conn.commit()
        conn.close()
    else:
        print('Клиента с фамилией', surname, 'нет в базе данных')


structureDB()

new_client(name='Владимр', surname='Путин', email='putin@kreml.ru')
new_client(surname='Медведев', name='Дмитрй', email='медведь')
new_client(surname='Набиулина', name='Эльвира', email='nabiylina@cbrf.ru')
new_client(surname='Орешкин', name='Максим', email='oreshkin@cbrf.ru')

add_phone(user_id=1, number='+7-001')
add_phone(user_id=2, number='+7-101')
add_phone(user_id=1, number='+7-100')
add_phone(user_id=4, number='+7-200')
add_phone(user_id=3, number='+7-555')


update_user(user_id=2, surname='Мишустин', name='Михаил', email='mishustin@kreml.ru')

phone_delete(surname='Путин')
phone_delete(surname='Набиулина')

delete_user(surname='Орешкин')

search = input('Поиск клиента по его данным. Введите фамилию, почту или телефон: ')
print('Результат поиска: ', looking_client(client_data=search)[0])