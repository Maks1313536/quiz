import sqlite3
 
db_name = 'quiz.sqlite'
conn = None
cursor = None
 
def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
 
def close():
    cursor.close()
    conn.close()
 
def do(query):
    cursor.execute(query)
    conn.commit()
    return cursor
def clear_db(): #0
    ''' удаляет все таблицы '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()
 
def create(): #0
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    do('''CREATE TABLE IF NOT EXISTS quiz (id INTEGER PRIMARY KEY, name VARCHAR)''')
    do('''CREATE TABLE IF NOT EXISTS question (id INTEGER PRIMARY KEY, question VARCHAR, answer VARCHAR, wrong1 VARCHAR, wrong2 VARCHAR, wrong3 VARCHAR)''')
    do('''CREATE TABLE IF NOT EXISTS quiz_content (id INTEGER PRIMARY KEY, quiz_id INTEGER, question_id INTEGER, FOREIGN KEY (quiz_id) REFERENCES quiz (id), FOREIGN KEY (question_id) REFERENCES question (id))''')
    close()
 
def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()
 
def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')
 
def check_answer(q_id, ans_text):
    query = '''SELECT question.answer FROM quiz_content, question WHERE quiz_content.id = ? AND quiz_content.question_id = question.id'''
    open()
    print(q_id)
    cursor.execute(query, (str(q_id),))
    result = cursor.fetchone()
    close()
    if result is None:
        return False
    else:
        if result[0] == ans_text:
            return True
        else:
            return False
def get_quiz_count():
    open()
    query = '''SELECT MAX(quiz_id) FROM quiz_content'''
    close()
 
def get_question_after(question_id = 0, quiz_id=1): #0
    open()
    query = '''SELECT quiz_content.id, question, question.answer, question.wrong1, question.wrong2, question.wrong3 
    FROM quiz_content, question WHERE quiz_content.question_id == question.id 
    AND quiz_content.id > ? AND quiz_content.quiz_id == ? ORDER BY quiz_content.id'''
    cursor.execute(query, [question_id, quiz_id])
    result = cursor.fetchone()
    close()
    return result 
def add_questions(): #0
    open()
    query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)"
    answer = input("Добавить связь (y / n)?")
    while answer != 'n':
        quiz_id = int(input("id викторины: "))
        question_id = int(input("id вопроса: "))
        cursor.execute(query, [quiz_id, question_id])
        conn.commit()
        answer = input("Добавить связь (y / n)?")
    close()
 
def add_quiz(): # викторина #0
    quizes = [('Случайность', ), ('Математика', ), ('Игры', )]
    open()
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.commit()
    close()
 
 
def add_links(): # вопросы
    list_q = [
    ("Что такое случайное событие?", "A) Событие, которое происходит без определенной причины", "B) Событие, которое происходит всегда", "C) Событие, вероятность которого можно предсказать", "D) Событие, которое происходит один раз в жизни"),
    ("Какова вероятность выпадения орла при одном броске монеты?", "A) 50%", "B) 0%", "C) 25%", "D) 75%"),
    ("Как называется математическое объект, описывающий случайную величину?", "A) Случайная величина", "B) Статистика", "C) Бином", "D) Граф"),
    ("Можно ли предсказать результат броска игральной кости?", "A) Нет", "B) Да", "C) Только если знаешь физику", "D) Только если удача на твоей стороне"),
    ("Что такое статистическая зависимость?", "A) Непредсказуемая связь между событиями", "B) Отсутствие связи между событиями", "C) Математический закон", "D) Случайность"),
    ("Что такое простое число?", "A) Число, имеющее только два делителя: 1 и само себя", "B) Число, больше всех других", "C) Число, оканчивающееся на 0", "D) Число, которое делится на 3"),
    ("Как называется операция, обратная умножению?", "A) Деление", "B) Сложение", "C) Вычитание", "D) Возведение в степень"),
    ("Что такое квадратный корень числа?", "A) Число, из которого можно извлечь корень", "B) Число, умноженное на себя", "C) Число, которое делится на 2", "D) Сумма двух чисел"),
    ("Что такое геометрическая прогрессия?", "A) Последовательность чисел, в которой каждый следующий член получается умножением предыдущего на одно и то же число", "B) Сумма двух чисел", "C) Треугольник", "D) Отрезок прямой"),
    ("Что такое бесконечность?", "A) Невообразимо большое количество", "B) Конец всего существующего", "C) Точка на числовой прямой", "D) Ноль"),
    ("Какое из этих игровых жанров не относится к видеоиграм?", "A) Монополия", "B) Шутер", "C) Ролевая игра", "D) Хоррор"),
    ("Какова цель игры шахматы?", "A) Достичь шаха и мат", "B) Получить как можно больше очков", "C) Захватить все фигуры противника", "D) Уничтожить короля противника"),
    ("Какой объект нужно собирать в игре 'Tetris'?", "A) Фигуры из блоков", "B) Кристаллы", "C) Фрукты", "D) Цветы"),
    ("Чему посвящена игра 'World of Warcraft'?", "A) Волшебству и фэнтези", "B) Мафии", "C) Пиратам", "D) Автомобилям"),
    ("Как называется самая высокая карта в колоде игральных карт?", "A) Туз", "B) Король", "C) Валет", "D) Дама")
]
    open()
    cursor.executemany('''INSERT INTO question 
                         (question, answer, wrong1, wrong2, wrong3) 
                         VALUES (?,?,?,?,?)''', list_q)
    conn.commit()
    close()
def s():
    query = 'SELECT * FROM quiz ORDER BY id'
    open()
    cursor.execute(query)
    return (cursor.fetchall())
    close()
    

    
    
def main():
    
    create()

    
    
    
    show_tables()

   
    

if __name__ == "__main__":
    main()
