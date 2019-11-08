import sys
import InformationWindow
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *


class MyWidget(QMainWindow):
    """ главное окно"""

    def __init__(self):
        super().__init__()
        uic.loadUi('main1.ui', self)

        # отображение имени
        self.continue_btn.clicked.connect(self.nameGiven)

        # счётчик действий
        self.count_healthy = 0
        self.count_food = 0
        self.count_mood = 0
        self.count_clean = 0
        self.count_sleep = 0

        # проигрывание музыки на фоне
        self.playlist = QMediaPlaylist()
        self.url = QUrl.fromLocalFile('music/norm.mp3')
        self.playlist.addMedia(QMediaContent(self.url))

        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.playlist().setCurrentIndex(0)
        self.player.play()

        # включение и выключение музыки
        self.on.clicked.connect(lambda: self.misicOnOff('on'))
        self.off.clicked.connect(lambda: self.misicOnOff('off'))

        # основное изображение
        self.name_picture = 'images_for_main_label/norm.jpg'
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

        # переменный для счётчика дней
        self.days = 300
        self.number_days = 1
        self.count_days = 0

        # изменение показателей
        self.number_food = 0.5
        self.number_mood = 0.3
        self.number_sleep = 0.4
        self.number_clean = 0.6
        self.number_healthy = 0.2

        # работа кнопок "кормить", "лечить" и тд
        self.healthy_btn.clicked.connect(lambda: self.life('healthy', 15))
        self.food_btn.clicked.connect(lambda: self.life('food', 20))
        self.mood_btn.clicked.connect(lambda: self.life('mood', 25))
        self.sleep_btn.clicked.connect(lambda: self.life('sleep', 40))
        self.clean_btn.clicked.connect(lambda: self.life('clean', 50))

        # работа кнопки про музыку и информацию ("?")
        self.misic.clicked.connect(lambda: self.openDialog('музыка'))
        self.qst_clean.clicked.connect(lambda: self.openDialog('чистота'))
        self.qst_sleep.clicked.connect(lambda: self.openDialog('сон'))
        self.qst_food.clicked.connect(lambda: self.openDialog('еда'))
        self.qst_mood.clicked.connect(lambda: self.openDialog('настроение'))
        self.qst_healthy.clicked.connect(lambda: self.openDialog('здоровье'))
        self.alina.clicked.connect(lambda: self.openDialog('автор'))

    def nameGiven(self):
        """ передача введённого имени в специальное поле"""

        self.label_name.setText(self.name_of_raccoon.text())
        QApplication.processEvents()
        self.name_of_raccoon.setText('')

    def misicOnOff(self, name):
        """ включение/выключение музыки"""

        if name == 'on':
            self.player.play()
        elif name == 'off':
            self.player.stop()

    def openDialog(self, name):
        """ открытие диалогового окна"""

        dialog = InformationWindow.Information()
        dialog.setWindowTitle(name)
        dialog.setTextOnLabel(name)
        dialog.exec_()

    def timerEvent(self, e):
        """функция для реагирования на события таймера, переопределение обработчик событий"""

        # сброс показателей
        self.number_food = 0.5
        self.number_mood = 0.3
        self.number_sleep = 0.4
        self.number_clean = 0.6
        self.number_healthy = 0.2

        # зависимость показателей друг от друга
        if self.step_food < 70:
            self.number_mood += 0.4
        elif self.step_mood < 60:
            self.number_healthy += 0.4
        elif self.step_clean < 50:
            self.number_healthy += 0.5
        elif self.step_healthy < 30:
            self.number_healthy += 1
        elif self.step_healthy < 60:
            self.number_food -= 0.4
        elif self.step_sleep < 50:
            self.number_mood += 0.6
        elif self.step_mood < 40:
            self.number_sleep += 0.4

        # случай, когда один из показателей равен нулю
        if self.step_food < 1 or self.step_mood < 1 or self.step_clean < 1 \
                or self.step_healthy < 1 or self.step_sleep < 1:
            self.timer.stop()
            self.begin.setText('ВСЁ СНАЧАЛА')

            self.picturePutOn('images_for_main_label/hurt.jpg')
            self.player.playlist().setCurrentIndex(0)
            self.player.play()
            return

        # случай, когда все показатели в норме
        elif self.step_food > 80 or self.step_mood > 80 or self.step_clean > 80 \
                or self.step_healthy > 80 or self.step_sleep > 80:
            self.picturePutOn('images_for_main_label/norm.jpg')
            self.player.playlist().setCurrentIndex(0)
            self.player.play()

        # тревожная музыка на фон
        if self.step_food < 50 or self.step_mood < 50 or self.step_clean < 50 \
                or self.step_healthy < 50 or self.step_sleep < 50:
            self.url1 = QUrl.fromLocalFile('music/not norm.mp3')
            self.playlist.addMedia(QMediaContent(self.url1))

            self.player.playlist().setCurrentIndex(1)
            self.player.play()
        else:
            self.player.playlist().setCurrentIndex(0)
            self.player.play()

        # зависимость главного изображения от показателей
        if self.step_food < 80:
            self.picturePutOn('images_for_main_label/wanna eat.jpg')
            QApplication.processEvents()
        elif self.step_mood < 80:
            self.picturePutOn('images_for_main_label/boring.jpg')
            QApplication.processEvents()
        elif self.step_healthy < 80:
            self.picturePutOn('images_for_main_label/sick.jpg')
            QApplication.processEvents()
        elif self.step_sleep < 80:
            self.picturePutOn('images_for_main_label/wanna sleep.jpg')
            QApplication.processEvents()
        elif self.step_clean < 80:
            self.picturePutOn('images_for_main_label/dirty.jpg')
            QApplication.processEvents()

        # счётчик дней
        self.days = self.days - self.number_days
        if self.days == 0:
            self.days = 300
            self.count_days += 1

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

        # вывод показателей счётчиков действий
        self.num_healthy.display(self.count_healthy)
        QApplication.processEvents()
        self.num_mood.display(self.count_mood)
        QApplication.processEvents()
        self.num_food.display(self.count_food)
        QApplication.processEvents()
        self.num_clean.display(self.count_clean)
        QApplication.processEvents()
        self.num_sleep.display(self.count_sleep)
        QApplication.processEvents()

        # вывод "прожитых" дней
        self.label_count_days.setText(str(self.count_days))
        QApplication.processEvents()

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
            self.count_healthy += 1

        elif self.name == 'food':
            if self.step_food + self.number < 100:
                self.step_food += self.number
            else:
                self.step_food = 100
            self.count_food += 1

        elif self.name == 'mood':
            if self.step_mood + self.number < 100:
                self.step_mood += self.number
            else:
                self.step_mood = 100
            self.count_mood += 1

        elif self.name == 'clean':
            if self.step_clean + self.number < 100:
                self.step_clean += self.number
            else:
                self.step_clean = 100
            self.count_clean += 1

        elif self.name == 'sleep':
            if self.step_sleep + self.number < 100:
                self.step_sleep += self.number
            else:
                self.step_sleep = 100
            self.count_sleep += 1

    def doAction(self):
        """запуск таймера, его отсановка и рестарт"""

        # сброс счётчика дней
        self.count_days = 0

        # сброс процентных показатели жизнедеятельности
        self.step_food = 100
        self.step_healthy = 100
        self.step_sleep = 100
        self.step_mood = 100
        self.step_clean = 100

        # сброс счётчиков действий
        self.count_healthy = 0
        self.count_food = 0
        self.count_mood = 0
        self.count_clean = 0
        self.count_sleep = 0

        if self.timer.isActive():
            self.timer.stop()
            self.begin.setText('ВСЁ СНАЧАЛА')
            QApplication.processEvents()
        else:
            self.timer.start(100, self)
            self.begin.setText('ЗАВЕРШИТЬ')
            QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
