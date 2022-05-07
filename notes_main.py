from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QHBoxLayout, QVBoxLayout, QFormLayout, QInputDialog

import json

notes = {'Добро пожаловать':
        {'текст': 'В этом приложении можно создавать заметки с тегами',
        'теги':['умные заметки', 'инструкция']}}
with open('notes_data.json', 'w') as file:
    json.dump(notes, file)
app = QApplication([])

'''Интерфейс приложения'''
#параметры окна приложения
notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки')
notes_win.resize(900, 600)

#виджеты окна приложения
list_notes = QListWidget()
list_notes_label = QLabel('Список заметок')

button_note_create = QPushButton('Создать заметку') #появляется окно с полем "Введите имя заметки"
button_note_del = QPushButton('Удалить заметку')
button_note_save = QPushButton('Сохранить заметку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введите тег...')
field_text = QTextEdit()
button_tag_add = QPushButton('Добавить к заметке')
button_tag_del = QPushButton('Открепить от заметки')
button_tag_search = QPushButton('Искать заметки по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегов')
l1 = QVBoxLayout()
l1.addWidget(field_text)
l2 = QVBoxLayout()
l2.addWidget(list_notes_label)
l2.addWidget(list_notes)
l3 = QHBoxLayout()

l3.addWidget(button_note_create)
l3.addWidget(button_note_del)
l2.addLayout(l3)
l2.addWidget(button_note_save)
l2.addWidget(list_tags_label)
l2.addWidget(list_tags)
l2.addWidget(field_tag)
l4 = QHBoxLayout()
l4.addWidget(button_tag_add)
l4.addWidget(button_tag_del)
l2.addLayout(l4)
l2.addWidget(button_tag_search)

def show_notes():
    name = list_notes.selectedItems()[0].text()
    field_text.setText(notes[name]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[name]['теги'])

list_notes.itemClicked.connect(show_notes)

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Добавть заметку', 'Название заметки')
    if ok and note_name != '':
        notes[note_name] = {'текст' :'', 'теги' : []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]['теги'])
        print(notes)
button_note_create.clicked.connect(add_note)

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)
        print(notes)
    else:
        print('Заметка для удаления не выбрана')
button_note_del.clicked.connect(del_note)

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текст'] = field_text.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)
        print(notes)
    else:
        print('Заметка для сохранения не выбрана!')
button_note_save.clicked.connect(save_note)


def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)
    else:
        print('Заметка для добавления тега не выбрана!')
def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['теги'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)
    else:
        print('Тег для удаления не выбран')
def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == 'Искать заметки по тегу' and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note]=notes[note]
        button_tag_search.setText('Сбросить поиск')
        list_notes.clear()
        list_tags.clear() 
        list_notes.addItems(notes.fi)
    elif button_tag_search.text() == 'Сбросить поиск':
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText('Искать заметки по тегу')
    else:
        pass
        #error.setText('Заметок с таким тегом нет')
        #error.exec_()

mainl = QHBoxLayout()
mainl.addLayout(l1)
mainl.addLayout(l2)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)
notes_win.setLayout(mainl)
notes_win.show()
list_notes.addItems(notes)
app.exec()