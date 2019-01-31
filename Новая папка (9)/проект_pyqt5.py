import sys

from PyQt5.QtWidgets import QApplication, QWidget, QCalendarWidget, QTimeEdit, QListWidget

from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton, QListView, QCheckBox

from PyQt5.QtCore import QDate, QTime

from PyQt5 import QtGui

z = []
try:
    with open('file.txt', 'r', encoding='utf-8') as file:
        file.seek(0)
        if len(file.read()) > 0:
            file.seek(0)
            for x in file.readlines():
                z.append(x)
    file.close()


    class Example(QWidget):

        def __init__(self):
            super().__init__()
            self.clear_lineedit = QLineEdit(self)
            self.info_sort = ''
            self.list = []
            self.dict = {}
            self.flag_print_file_info = True
            self.initUI()

        def initUI(self):

            self.setGeometry(300, 300, 940, 650)

            self.setWindowTitle('Первая программа')

            self.myListView = QListView(self)

            self.myListView.resize(300, 500)

            self.myListView.move(600, 0)

            self.cal = QCalendarWidget(self)

            self.cal.resize(500, 500)

            self.cal.move(0, 0)

            self.time = QTimeEdit(self)

            self.time.resize(50, 50)

            self.time.move(520, 250)

            self.helps = QLabel('Введите событие:', self)

            self.helps.move(0, 530)

            self.input_ivents = QLineEdit(self)

            self.input_ivents.resize(200, 50)

            self.input_ivents.move(130, 520)

            self.setStyleSheet("QLabel { font-size:15px}")

            self.button = QPushButton('Добавить', self)

            self.button.move(80, 580)

            self.print_file_info()

            self.button.clicked.connect(self.push)

            self.show()

        def print_file_info(self):
            if len(z) > 1:
                for x in range(len(z)):
                    x = z[x].split()
                    self.dict[x[1]] = x[0]
                    x = x[1].split('.')
                    x = ''.join(x)
                    self.list.append(x)
            elif len(z) == 2:
                x = z[0].split()
                self.dict[x[1]] = x[0]
                x = x[1].split('.')
                x = ''.join(x)
                self.list.append(x)
            if self.flag_print_file_info:
                for x in range(len(self.list)):
                    self.list[x] = int(self.list[x])
                self.list.sort()
                model = QtGui.QStandardItemModel()
                self.myListView.setModel(model)
                for x in range(len(self.list)):
                    self.list[x] = str(self.list[x])
                for e in self.list:
                    for x in self.dict.keys():
                        if ''.join(x.split('.')) == str(e):
                            p = x.split('.')
                            i = QtGui.QStandardItem(
                                self.dict[x] + '  ' + p[2] + '.' + p[1] + '.' + p[0] + ' ' + p[3] + ':' + p[-1])
                            model.appendRow(i)
                self.show()
                self.flag_print_file_info = False

        def push(self):
            time: QTime = self.time.time()
            self.ivent = self.input_ivents.text()

            self.info_input = ''

            date: QDate = self.cal.selectedDate()

            self.info_input += str(date.year()) + '.'
            self.info_sort += str(date.year())
            if len(str(date.month())) == 1:
                self.info_input += '0' + str(date.month()) + '.'
                self.info_sort += '0' + str(date.month())
            else:
                self.info_input += str(date.month()) + '.'
                self.info_sort += str(date.month())
            if len(str(date.day())) == 1:
                self.info_input += '0' + str(date.day()) + '.'
                self.info_sort += '0' + str(date.day())
            else:
                self.info_input += str(date.day()) + '.'
                self.info_sort += str(date.day())
            if len(str(time.hour())) == 1:
                self.info_input += '0' + str(time.hour()) + '.'
                self.info_sort += '0' + str(time.hour())
            else:
                self.info_input += str(time.hour()) + '.'
                self.info_sort += str(time.hour())
            if len(str(time.minute())) == 1:
                self.info_input += '0' + str(time.minute())
                self.info_sort += '0' + str(time.minute())
            else:
                self.info_input += str(time.minute())
                self.info_sort += str(time.minute())

            self.info_sort = int(self.info_sort)

            self.list.append(self.info_sort)
            self.dict[self.info_input] = self.ivent
            for x in range(len(self.list)):
                self.list[x] = int(self.list[x])
            self.list.sort()
            self.info_sort = ''
            model = QtGui.QStandardItemModel()
            self.myListView.setModel(model)
            for x in range(len(self.list)):
                self.list[x] = str(self.list[x])
            for e in self.list:
                for x in self.dict.keys():
                    if ''.join(x.split('.')) == str(e):
                        p = x.split('.')
                        i = QtGui.QStandardItem(
                            self.dict[x] + '  ' + p[2] + '.' + p[1] + '.' + p[0] + ' ' + p[3] + ':' + p[-1])
                        model.appendRow(i)
            with open('file.txt', 'w', encoding='utf-8') as g:
                g.seek(0)
                for x in self.dict.keys():
                    g.write(self.dict[x] + ' ' + x + '\n')
            g.close()


    if __name__ == '__main__':
        app = QApplication(sys.argv)

        ex = Example()

        ex.show()

        sys.exit(app.exec())

except IOError as e:
    print('не удалось открыть файл ')
