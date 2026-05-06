from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, 
                             QVBoxLayout, QHBoxLayout, QRadioButton, 
                             QGroupBox, QButtonGroup)
from PyQt5.QtGui import QFont
from random import shuffle, randint  

app = QApplication([])
main_win = QWidget()
main_win.setGeometry(300, 300, 600, 500)
main_win.setWindowTitle("Memory Card - Культурный центр 'Человек мира'")
font = QFont('Arial', 14)
main_win.setFont(font)

class Question:
    def __init__(self, text, right_answer, wrong1, wrong2, wrong3):
        self.text = text             
        self.right_answer = right_answer 
        self.wrong_answers = [wrong1, wrong2, wrong3] 

questions_list = [
    Question("Какой национальности не существует?", 
             "Смурфы", "Энцы", "Чулымцы", "Алеуты"),
    Question("Какой язык является официальным в Бразилии?", 
             "Португальский", "Испанский", "Французский", "Итальянский"),
    Question("Какое из этих племён существует в реальности?", 
             "Чулымцы", "Хоббиты", "Эльфы", "Смурфы"),
    Question("Где находится культурный центр «Человек мира»?", 
             "В Москве", "В Санкт-Петербурге", "В Новосибирске", "Во Владивостоке"),
    Question("Какой народ проживает на Аляске?", 
             "Алеуты", "Энцы", "Чулымцы", "Смурфы")
]

main_win.total = 0    
main_win.count = 0  

lb_Question = QLabel("") 

RadioGroupBox = QGroupBox("Варианты ответов")

rbtn_1 = QRadioButton("")
rbtn_2 = QRadioButton("")
rbtn_3 = QRadioButton("")
rbtn_4 = QRadioButton("")

radio_group = QButtonGroup()
radio_group.addButton(rbtn_1)
radio_group.addButton(rbtn_2)
radio_group.addButton(rbtn_3)
radio_group.addButton(rbtn_4)

AnswerGroupBox = QGroupBox("Результат")
lb_Result = QLabel("")
lb_Correct = QLabel("")

layout_result = QVBoxLayout()
layout_result.addWidget(lb_Result, alignment=Qt.AlignCenter)
layout_result.addWidget(lb_Correct, alignment=Qt.AlignCenter)
AnswerGroupBox.setLayout(layout_result)

layout_ans_1 = QHBoxLayout()
layout_ans_2 = QVBoxLayout()
layout_ans_3 = QVBoxLayout()

layout_ans_2.addWidget(rbtn_1)
layout_ans_2.addWidget(rbtn_2)
layout_ans_3.addWidget(rbtn_3)
layout_ans_3.addWidget(rbtn_4)
layout_ans_1.addLayout(layout_ans_2)
layout_ans_1.addLayout(layout_ans_3)

RadioGroupBox.setLayout(layout_ans_1)

ansButton = QPushButton("Ответить")

layout_line1 = QVBoxLayout()
layout_line1.addWidget(lb_Question, alignment=Qt.AlignCenter)

layout_line3 = QHBoxLayout()
layout_line3.addStretch(1)
layout_line3.addWidget(ansButton, stretch=2)
layout_line3.addStretch(1)

layout_card = QVBoxLayout()
layout_card.addLayout(layout_line1)
layout_card.addWidget(RadioGroupBox)
layout_card.addWidget(AnswerGroupBox)
layout_card.addLayout(layout_line3)

main_win.setLayout(layout_card)

buttons = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]
current_question = None  
correct_answer = ""      

def print_statistics():
    """Выводит текущую статистику ответов в консоль"""
    if main_win.total == 0:
        print("Статистика: пока нет отвеченных вопросов.")
    else:
        rating = (main_win.count / main_win.total) * 100
        print(f"   Статистика: Правильных ответов: {main_win.count} из {main_win.total}")
        print(f"   Рейтинг: {rating:.1f}%")

def show_question():
    """Отображает форму вопроса и сбрасывает выбор переключателей"""
    AnswerGroupBox.hide()
    RadioGroupBox.show()
    ansButton.setText("Ответить")
    
    radio_group.setExclusive(False)
    rbtn_1.setChecked(False)
    rbtn_2.setChecked(False)
    rbtn_3.setChecked(False)
    rbtn_4.setChecked(False)
    radio_group.setExclusive(True)

def show_result():
    """Отображает форму ответа"""
    RadioGroupBox.hide()
    AnswerGroupBox.show()
    ansButton.setText("Следующий вопрос")

def show_correct(res):
    """Отображает результат проверки ответа"""
    lb_Result.setText(res)
    lb_Correct.setText(correct_answer)
    show_result()

def check_answer():
    if rbtn_1.isChecked():
        selected = rbtn_1.text()
    elif rbtn_2.isChecked():
        selected = rbtn_2.text()
    elif rbtn_3.isChecked():
        selected = rbtn_3.text()
    elif rbtn_4.isChecked():
        selected = rbtn_4.text()
    else:
        selected = ""
    if selected == "":
        return
    main_win.total += 1
    if selected == correct_answer:
        main_win.count += 1
        show_correct("ПРАВИЛЬНО!")
    else:
        show_correct("НЕПРАВИЛЬНО!")
    print_statistics()

def ask(question_obj):
    global current_question, correct_answer
    current_question = question_obj
    correct_answer = question_obj.right_answer
    lb_Question.setText(question_obj.text)
    all_answers = [question_obj.right_answer] + question_obj.wrong_answers
    shuffle(all_answers)
    for i, button in enumerate(buttons):
        button.setText(all_answers[i])
    show_question()

def next_random_question():
    if questions_list:
        quest_num = randint(0, len(questions_list) - 1)
        random_q = questions_list[quest_num]
        questions_list.pop(quest_num)
        ask(random_q)
    else:
        lb_Question.setText("Нет вопросов в базе")

def start_test():
    if ansButton.text() == "Ответить":
        if any(btn.isChecked() for btn in buttons):
            check_answer()
    else:
        next_random_question()

AnswerGroupBox.hide()
next_random_question()  

ansButton.clicked.connect(start_test)

main_win.show()
app.exec_()
