import sys
import time

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QProgressBar, QMainWindow, QDialog
from PyQt5.QtWidgets import QLCDNumber, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *


class MyWidget(QMainWindow):
    """ главное окно"""

    def __init__(self):
        super().__init__()
        uic.loadUi('main1.ui', self)

        # проигрывание музыки на фоне

        self.playlist = QMediaPlaylist()
        self.url = QUrl.fromLocalFile('основа.mp3')
        self.playlist.addMedia(QMediaContent(self.url))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.play()

        # основное изображение
        self.name_picture = 'сидит.jpg'
        self.picture1 = QPixmap(self.name_picture)
        self.picture.setPixmap(self.picture1)

        # запуск таймера при нажатии кнопки

        self.begin.clicked.connect(self.doAction)

        self.timer = QtCore.QBasicTimer()

        # процентные показатели жизнедеятельности

        self.step_food = 100
        self.step_healthy = 100
        self.step_sleep = 100
        self.step_mood = 100
        self.step_clean = 100

        self.steps = [int(self.step_food), int(self.step_healthy), int(self.step_sleep),
                      int(self.step_mood), int(self.step_clean)]

        # изменение показателей

        self.number_food = 0.25
        self.number_mood = 0.15
        self.number_sleep = 0.2
        self.number_clean = 0.3
        self.number_healthy = 0.1

        # зависимость показателей друг от друга

        if self.step_food < 70:
            self.number_mood += 0.2
        if self.step_mood < 60:
            self.number_healthy += 0.2
        if self.step_clean < 50:
            self.number_healthy += 0.5
        if self.step_healthy < 30:
            self.number_healthy += 0.5
        if self.step_healthy < 60:
            self.number_food -= 0.2
        if self.step_sleep < 50:
            self.number_mood += 0.3
        if self.step_mood < 40:
            self.number_sleep += 0.2

        # работа кнопок "кормить", "лечить" и тд

        self.healthy_btn.clicked.connect(lambda: self.life('healthy', 15))
        self.food_btn.clicked.connect(lambda: self.life('food', 20))
        self.mood_btn.clicked.connect(lambda: self.life('mood', 25))
        self.sleep_btn.clicked.connect(lambda: self.life('sleep', 40))
        self.clean_btn.clicked.connect(lambda: self.life('clean', 50))

        # работа кнопки про музыку

        self.misic.clicked.connect(lambda: self.openDialog('музыка'))

    def openDialog(self, name):

        """ открытие диалогового окна"""

        dialog = Information()
        dialog.setWindowTitle(name)
        dialog.setTextOnLabel(name)
        dialog.exec_()

    def timerEvent(self, e):

        """функция для реагирования на события таймера, переопределение обработчик событий"""

        # случай, когда один из показателей равен нулю

        if self.step_food < 1 or self.step_mood < 1 or self.step_clean < 1 \
                or self.step_healthy < 1 or self.step_sleep < 1:
            self.timer.stop()
            self.begin.setText('ВСЁ СНАЧАЛА')

            self.picturePutOn('обиделся.jpg')
            return

        # тревожная музыка на фон

        if self.step_food < 50 or self.step_mood < 50 or self.step_clean < 50 \
                or self.step_healthy < 50 or self.step_sleep < 50:
            self.url = QUrl.fromLocalFile('тревога.mp3')
            self.playlist.addMedia(QMediaContent(self.url))
            self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        # зависимость главного изображения от показателей

        if self.step_food < 90:
            self.picturePutOn('просит кушать.jpg')
            QApplication.processEvents()
        if self.step_mood < 90:
            self.picturePutOn('скучно.jpg')
            QApplication.processEvents()
        if self.step_sleep < 90:
            self.picturePutOn('хочет спать.jpg')
            QApplication.processEvents()
        if self.step_clean < 90:
            self.picturePutOn('грязный.jpg')
            QApplication.processEvents()
        if self.step_healthy < 90:
            self.picturePutOn('болеет.jpg')
            QApplication.processEvents()

        # изменение показателей прогресс-баров

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

    def picturePutOn(self, name):

        """ функция для замены основной картинки"""

        self.name_picture = name
        self.picture1 = QPixmap(self.name_picture)
        self.picture.setPixmap(self.picture1)

    def life(self, name, number):

        """ увеличение показателей"""
        self.number = number
        self.name = name
        if self.name == 'healthy':
            if self.step_healthy + self.number < 100:
                self.step_healthy += self.number
            else:
                self.step_healthy = 100
        elif self.name == 'food':
            if self.step_food + self.number < 100:
                self.step_food += self.number
            else:
                self.step_food = 100
        elif self.name == 'mood':
            if self.step_mood + self.number < 100:
                self.step_mood += self.number
            else:
                self.step_mood = 100
        elif self.name == 'clean':
            if self.step_clean + self.number < 100:
                self.step_clean += self.number
            else:
                self.step_clean = 100
        elif self.name == 'sleep':
            if self.step_sleep + self.number < 100:
                self.step_sleep += self.number
            else:
                self.step_sleep = 100

    def doAction(self):

        """запуск таймера, его отсановка и рестарт"""

        # сброс процентных показатели жизнедеятельности

        self.step_food = 100
        self.step_healthy = 100
        self.step_sleep = 100
        self.step_mood = 100
        self.step_clean = 100

        if self.timer.isActive():
            self.timer.stop()
            self.begin.setText('ВСЁ СНАЧАЛА')
            QApplication.processEvents()
        else:
            self.timer.start(100, self)
            self.begin.setText('ЗАВЕРШИТЬ')
            QApplication.processEvents()


class Information(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('information.ui', self)

    def setTextOnLabel(self, name):
        self.name = name
        if self.name == 'музыка':
            self.text.setText('Ти́моти Макке́нзи, более известный по сценическому имени Labrinth, — британский '
                              'автор-исполнитель и музыкальный продюсер. В данном приложении используются'
                              'его треки New Girl и Following Tyler')
        self.text.setWordWrap(True)
        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
