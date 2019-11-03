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

        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.playlist().setCurrentIndex(0)
        self.player.play()

        # включение и выключение музыки
        self.on.clicked.connect(lambda: self.misicOnOff('on'))
        self.off.clicked.connect(lambda: self.misicOnOff('off'))

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

        # работа кнопки про музыку и информацию ("?")
        self.misic.clicked.connect(lambda: self.openDialog('музыка'))
        self.qst_clean.clicked.connect(lambda: self.openDialog('чистота'))
        self.qst_sleep.clicked.connect(lambda: self.openDialog('сон'))
        self.qst_food.clicked.connect(lambda: self.openDialog('еда'))
        self.qst_mood.clicked.connect(lambda: self.openDialog('настроение'))
        self.qst_healthy.clicked.connect(lambda: self.openDialog('здоровье'))
        self.alina.clicked.connect(lambda: self.openDialog('автор'))

    def misicOnOff(self, name):
        if name == 'on':
            self.player.play()
        elif name == 'off':
            self.player.stop()

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
            self.player.playlist().setCurrentIndex(0)
            self.player.play()
            return

        # случай, когда все показатели в норме
        elif self.step_food > 80 or self.step_mood > 80 or self.step_clean > 80 \
                or self.step_healthy > 80 or self.step_sleep > 80:
            self.picturePutOn('сидит.jpg')
            self.player.playlist().setCurrentIndex(0)
            self.player.play()

        # тревожная музыка на фон
        if self.step_food < 50 or self.step_mood < 50 or self.step_clean < 50 \
                or self.step_healthy < 50 or self.step_sleep < 50:
            self.url = QUrl.fromLocalFile('тревога.mp3')
            self.playlist.addMedia(QMediaContent(self.url))

            self.player.playlist().setCurrentIndex(1)
            self.player.play()
        else:
            self.player.playlist().setCurrentIndex(0)
            self.player.play()

        # зависимость главного изображения от показателей
        if self.step_food < 80:
            self.picturePutOn('просит кушать.jpg')
            QApplication.processEvents()
        elif self.step_mood < 80:
            self.picturePutOn('скучно.jpg')
            QApplication.processEvents()
        elif self.step_healthy < 80:
            self.picturePutOn('болеет.jpg')
            QApplication.processEvents()
        elif self.step_sleep < 80:
            self.picturePutOn('хочет спать.jpg')
            QApplication.processEvents()
        elif self.step_clean < 80:
            self.picturePutOn('грязный.jpg')
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
    """класс диалогового окна"""

    def __init__(self):
        super().__init__()
        uic.loadUi('information.ui', self)

    def setTextOnLabel(self, name):
        """вывод текста в диалоговом окне"""

        self.name = name
        if self.name == 'музыка':
            self.text.setText('Ти́моти Макке́нзи, более известный по сценическому имени Labrinth, — британский '
                              'автор-исполнитель и музыкальный продюсер. В данном приложении используются'
                              'его треки New Girl и Following Tyler')
        elif self.name == 'чистота':
            self.text.setText('Енот относится к числу чистоплотных животных и вполне самостоятельно может'
                              ' справиться с чистотой своей шкурки, ввиду этого процедуру купания следует '
                              'проводить не чаще 3-4 раз в год, применяя при этом обыкновенные шампуни для'
                              ' животных. Большие усилия хозяин енота должен направлять на еженедельную чистку'
                              ' вольера.')
        elif self.name == 'еда':
            self.text.setText('Эти милые звери всеядны и неприхотливы в выборе своей пищи. Для здорового'
                              ' существования зверька в условиях квартиры его рацион должен быть приближен к'
                              ' тому что и в естественных условиях (нежное мясо и отваренная рыба). Для здорового '
                              'пищеварения в рацион зверушки должны входить следующие фрукты на выбор: слива, яблоко,'
                              ' виноград, банан, а также различные ягоды. Экспериментировать с цитрусовыми не стоит,'
                              ' так как это чревато для зверя аллергией. ')
        elif self.name == 'здоровье':
            self.text.setText('Конечно, прежде, чем привести зверя в дом, следует показать его врачу-ветеринару,'
                              ' для того чтобы сделать прививки, проверить наличие паразитов в организме животного.'
                              ' Еноты очень чувствительны к воздействию на них прямых солнечных лучей, и могут'
                              ' получить тепловой удар, стоит обезопасить питомца от этого. ')
        elif self.name == 'сон':
            self.text.setText('Владельцы енотов отмечают, что эти проныры с полосатым хвостом обожают сон.'
                              ' Может доходить до того, что енот засыпает непосредственно в процессе игры '
                              'со своим владельцем. Почуяв зевоту и легкую сонливость, енот без стеснения '
                              'заваливается в спячку на том же месте, где стоит.')
        elif self.name == 'настроение':
            self.text.setText('Вся жизнь енота – это одна сплошная авантюра. Если в голову енота заберется'
                              ' какая-то идея, то он осуществит свои планы несмотря ни на что. Характер енота '
                              'полоскуна можно сравнить с непобедимым завоевателем, который приходит в жизнь '
                              'человека, чтобы завоевать его сердце, захватить симпатию и пленить все свободное'
                              ' время.')
        elif self.name == 'автор':
            self.text.setText('Автором данного приложения является Васильева Алина, более известная под'
                              ' псевдонимом Ключевская. Этот тамагочи енота был сделан в рамках проекта'
                              ' Яндекс.Лицея. Странички Алины в соц.сетях: vk.com/damn_sock '
                              '  stihi.ru/avtor/damnsock   инсту надо добавить')
        self.text.setWordWrap(True)
        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
