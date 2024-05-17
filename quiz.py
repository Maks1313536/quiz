from flask import Flask, render_template, redirect, url_for, session, request

from db_screpts1 import get_question_after, s, check_answer
from random import shuffle
import os
import sqlite3
question_id, quiz_id = 0, 0
def question_form(question):
    answers_list = [question[2], question[3], question[4], question[5]]
    shuffle(answers_list)
    print(type(int(session['quiz'])))
    return render_template('test.html', 
    question = question[1], quest_id = question[0],
    answers_list = answers_list, c = int(session['quiz']))
 
def save_answers():
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    session['last_question'] = quest_id
    session['total'] += 1
    if check_answer(quest_id, answer):
        session['answers'] += 1
f1 = 0
def start_quiz(quiz_id):
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0


def index():
    global f1
    
    
    session['last_question'] = 0
    if request.method == 'GET':
        start_quiz(-1)
        return render_template('start.html', quizes = s())
    else:
        quiz_id =  request.form.get('quiz')
        start_quiz(quiz_id)
         
        return redirect(url_for('test'))

def test():
    
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_answers()
        
        next_question = get_question_after(session['last_question'], session['quiz'])

        if next_question is None or len(next_question) == 0:
            return redirect(url_for('result'))
        else:
            return question_form(next_question)

def result():
    html = render_template('result.html', a = session['answers'])
  
    return html
   
folder = os.getcwd()
app = Flask(__name__, template_folder=folder, static_folder=folder)
app.config['SECRET_KEY'] = 'VeryStrongKey'
app.add_url_rule('/', 'index', index, methods=['POST', 'GET'])
app.add_url_rule('/test', 'test', test, methods=['POST', 'GET'])
app.add_url_rule('/result', 'result', result, methods=['POST', 'GET'])
if __name__ == '__main__':
    
    app.run()