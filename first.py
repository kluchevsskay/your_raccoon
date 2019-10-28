import sys
import time

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QProgressBar, QMainWindow
from PyQt5.QtWidgets import QLCDNumber, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore



class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main1.ui', self)

        # self.pushButton.clicked.connect(self.run)

        self.name_picture = 'сидит.jpg'
        self.picture1 = QPixmap(self.name_picture)
        self.picture.setPixmap(self.picture1)
        
        self.begin.clicked.connect(self.doAction)

        self.timer = QtCore.QBasicTimer()

        self.step_food = 100
        self.step_healthy = 100
        self.step_sleep = 100
        self.step_mood = 100
        self.step_clean = 100

        self.number_food = 0.2
        self.number_mood = 0.1
        self.number_sleep = 0.2
        self.number_clean = 0.3
        self.number_healthy = 0.1

        if self.step_food < 70:
            self.number_mood += 0.2


    def timerEvent(self, e):

        self.step_food = self.step_food - self.number_food
        self.food.setValue(self.step_food)

        self.step_sleep = self.step_sleep - self.number_sleep
        self.sleep.setValue(self.step_sleep)

        self.step_healthy = self.step_healthy - self.number_healthy
        self.healthy.setValue(self.step_healthy)

        self.step_clean = self.step_clean - self.number_clean
        self.clean.setValue(self.step_clean)

        self.step_mood = self.step_mood - self.number_mood
        self.mood.setValue(self.step_mood)

    def doAction(self):
        self.step_food = 100
        self.step_healthy = 100
        self.step_sleep = 100
        self.step_mood = 100
        self.step_clean = 100

        if self.timer.isActive():
            self.timer.stop()
            self.begin.setText('ВСЁ СНАЧАЛА')
        else:
            self.timer.start(100, self)
            self.begin.setText('ЗАВЕРШИТЬ')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
