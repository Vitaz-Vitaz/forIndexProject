import sqlite3


from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize

from PyQt5.QtGui import QPixmap

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

aMain = None
aID = 0
likedPlants = set()
flagLike = False


class firstWidget(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        global flagLike
        flagLike = False
        self.connection = sqlite3.connect("Plants.sqlite")
        self.res = self.connection.cursor().execute("SELECT * FROM plants").fetchall()
        global aMain
        aMain = self.res.copy()
        for i in self.res:
            print(i)
        self.secondWindow = None
        self.setStyleSheet("background-image: url(background_for_first_widget);")
        uic.loadUi('yandex_first_widget.ui', self)

        self.button_enter_to_guide.setStyleSheet(
            "QPushButton {background: rgb(201, 160, 220); color: rgb(61, 43, 31); border-radius: 10px;}")
        self.my_plants.setStyleSheet(
            "QPushButton {background: rgb(201, 160, 220); color: rgb(61, 43, 31); border-radius: 10px;}")
        self.button_to_admin.setStyleSheet(
            "QPushButton {background: rgb(201, 160, 220); color: rgb(61, 43, 31); border-radius: 10px;}")
        self.button_enter_to_guide.clicked.connect(self.goSecond)
        self.my_plants.clicked.connect(self.showLiked)

    def showLiked(self):
        self.close()
        self.showLiked = showLiked()
        self.showLiked.show()

    def goSecond(self):
        self.close()
        self.secondWindow = secondWindow()
        self.secondWindow.show()


class showLiked(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        global flagLike
        flagLike = False
        uic.loadUi('yandex_TypePlants_widget.ui', self)
        self.setWindowTitle("your plants")

        global likedPlants, aMain

        for i in range(len(likedPlants)):
            print("go")
            item = QtWidgets.QListWidgetItem()
            item.setText(aMain[list(likedPlants)[i]][1])
            print("go2")
            item.setSizeHint(QSize(60, 60))
            self.listWidget.addItem(QtWidgets.QListWidgetItem(item))
        self.listWidget.itemClicked.connect(self.selectionChanged)
        self.button_toMenu.clicked.connect(self.plToMenu)

    def plToMenu(self):
        self.close()
        self.secondWindow = secondWindow()
        self.secondWindow.show()

    def selectionChanged(self, item):
        print("Вы кликнули: {}".format(item.text()))
        n = list()
        nAll = list()
        for i in aMain:
            nAll.append(i[1])

        if item.text() in nAll:
            global aID
            aID = nAll.index(item.text())
            print(aID)
            self.close()
            self.showPlant = showPlant()
            self.showPlant.show()

        self.listWidget.clear()
        for i in range(len(n)):
            item = QtWidgets.QListWidgetItem()
            item.setText(n[i])
            item.setSizeHint(QSize(60, 60))
            self.listWidget.addItem(QtWidgets.QListWidgetItem(item))


class secondWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.fruitAndBerryPlants = None
        self.kailyardPlants = None
        self.gardenPlants = None
        self.roomPlants = None
        self.setWindowTitle("")
        uic.loadUi('Yandex_guide_widget.ui', self)
        self.exit.clicked.connect(self.enterNow)
        pixmap = QPixmap("firstImage.png")
        self.label_1.setPixmap(pixmap)

        self.label_1.installEventFilter(self)
        self.label_2.installEventFilter(self)
        self.label_3.installEventFilter(self)
        self.label_4.installEventFilter(self)
        pixmap = QPixmap("secondImage.png")
        self.label_2.setPixmap(pixmap)

        pixmap = QPixmap("thirdImage.png")
        self.label_3.setPixmap(pixmap)

        pixmap = QPixmap("forthImage.png")
        self.label_4.setPixmap(pixmap)

        pixmap = QPixmap("text1.png")
        self.text1.setPixmap(pixmap)

        pixmap = QPixmap("text2.png")
        self.text2.setPixmap(pixmap)

        pixmap = QPixmap("text3.png")
        self.text3.setPixmap(pixmap)

        pixmap = QPixmap("text4.png")
        self.text4.setPixmap(pixmap)

        pixmap = QPixmap("text5.png")
        self.text5.setPixmap(pixmap)

    def enterNow(self):
        self.close()
        self.first = firstWidget()
        self.first.show()

    def eventFilter(self, obj, e):
        if e.type() == 2:
            btn = e.button()
            print(obj.x(), obj.y())
            if obj.x() == 40:
                self.close()
                self.roomPlants = roomPlants()
                self.roomPlants.show()
            elif obj.x() == 260:
                self.close()

                self.gardenPlants = gardenPlants()
                self.gardenPlants.show()
            elif obj.x() == 20 and obj.y() == 300:
                self.close()
                self.kailyardPlantsPlants = kailyardPlants()
                self.kailyardPlantsPlants.show()
            elif obj.x() == 230 and obj.y() == 300:
                self.close()
                self.fruitAndBerryPlants = fruitAndBerryPlants()
                self.fruitAndBerryPlants.show()
        return super(QMainWindow, self).eventFilter(obj, e)


class showPlant(QtWidgets.QMainWindow):
    def __init__(self):
        global flagLike
        flagLike = False
        super().__init__()

        uic.loadUi('yandex_plant_widget.ui', self)
        self.setWindowTitle(aMain[aID][1])
        self.l_like.installEventFilter(self)
        self.l_Name.setText(aMain[aID][1])

        pixmap1 = QPixmap("Images/notlike.png")
        self.l_like.setPixmap(pixmap1)

        pixmap = QPixmap("Images/" + str(aMain[aID][3]) + ".jpg")
        self.l_Image.setPixmap(pixmap)

        self.button_toMenu.clicked.connect(self.toMenu)

        with open("descriptions/" + str(aMain[aID][3]) + ".txt", 'rt', encoding="utf8") as f:
            l2 = f.readlines()

            for i in l2:
                self.pl_Des.insertPlainText(i)

            self.pl_Des.setReadOnly(True)

        f.close()

    def eventFilter(self, obj, e):
        if e.type() == 2:
            btn = e.button()
            global flagLike, likedPlants, aID
            if not flagLike:
                likedPlants.add(aID)
                pixmap1 = QPixmap("Images/like.png")
                self.l_like.setPixmap(pixmap1)
                flagLike = True
            else:

                pixmap1 = QPixmap("Images/notlike.png")
                self.l_like.setPixmap(pixmap1)
                flagLike = False

        return super(QMainWindow, self).eventFilter(obj, e)

    def toMenu(self):
        self.close()
        self.secondWidget = secondWindow()
        self.secondWidget.show()


class roomPlants(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        global flagLike
        flagLike = False
        uic.loadUi('yandex_TypePlants_widget.ui', self)
        self.setWindowTitle("roomPlants")
        self.button_toMenu.clicked.connect(self.toMenu)
        a = ["Все комнатные  растения", "Аквариумные", "Декоративнолиственные", "Деревья", "Кактусы",
             "Хищные"]
        self.listWidget.itemClicked.connect(self.selectionChanged)
        for i in range(len(a)):
            item = QtWidgets.QListWidgetItem()
            item.setText(a[i])
            item.setSizeHint(QSize(60, 60))
            self.listWidget.addItem(QtWidgets.QListWidgetItem(item))

    def selectionChanged(self, item):
        print("Вы кликнули: {}".format(item.text()))
        n = list()
        nAll = list()
        for i in aMain:
            nAll.append(i[1])
        if item.text() == "Все комнатные  растения":

            for i in aMain:
                if i[2] == "комнатные":
                    print(1)
                    n.append(i[1])
        else:
            for i in aMain:
                if i[-1] == item.text().lower() and i[2] == "комнатные":
                    print(1)
                    n.append(i[1])

        print(str(item.text()))
        if item.text() in nAll:
            global aID
            aID = nAll.index(item.text())
            print(aID)
            self.close()
            self.showPlant = showPlant()
            self.showPlant.show()

        self.listWidget.clear()
        for i in range(len(n)):
            item = QtWidgets.QListWidgetItem()
            item.setText(n[i])
            item.setSizeHint(QSize(60, 60))
            self.listWidget.addItem(QtWidgets.QListWidgetItem(item))

    def toMenu(self):
        self.close()
        self.secondWidget = secondWindow()
        self.secondWidget.show()


class gardenPlants(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        print(3)
        global flagLike
        flagLike = False
        self.setWindowTitle("roomPlants")
        uic.loadUi('yandex_TypePlants_widget.ui', self)
        self.listWidget.itemClicked.connect(self.selectionChanged)
        self.button_toMenu.clicked.connect(self.toMenu)
        a = ["Все садовые растения", "Ампельные", "Декоративнолиственные", "Кустарники"]

        for i in range(len(a)):
            item = QtWidgets.QListWidgetItem()
            item.setText(a[i])
            print(a[i])
            item.setSizeHint(QSize(60, 60))
            self.listWidget.addItem(QtWidgets.QListWidgetItem(item))

    def selectionChanged(self, item):
        print("Вы кликнули: {}".format(item.text()))
        n = list()
        if item.text() == "Все садовые растения":

            for i in aMain:
                if i[2] == "садовые":
                    print(1)
                    n.append(i[1])
        else:
            for i in aMain:
                if i[-1] == item.text().lower() and i[2] == "садовые":
                    print(1)
                    n.append(i[1])

        print(str(item.text()))
        nAll = list()
        for i in aMain:
            nAll.append(i[1])
        if item.text() in nAll:
            global aID
            aID = nAll.index(item.text())
            print(aID)
            self.close()
            self.showPlant = showPlant()
            self.showPlant.show()
        self.listWidget.clear()
        for i in range(len(n)):
            item = QtWidgets.QListWidgetItem()
            item.setText(n[i])
            item.setSizeHint(QSize(60, 60))
            self.listWidget.addItem(QtWidgets.QListWidgetItem(item))

    def toMenu(self):
        self.close()
        self.secondWidget = secondWindow()
        self.secondWidget.show()


class kailyardPlants(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        global flagLike
        flagLike = False
        uic.loadUi('yandex_TypePlants_widget.ui', self)
        self.setWindowTitle("kaliyardPlants")
        self.button_toMenu.clicked.connect(self.toMenu)
        a = ["Все огородные растения", "Десертные", "Луковичные", "Плодовые"]
        self.listWidget.itemClicked.connect(self.selectionChanged)
        for i in range(len(a)):
            item = QtWidgets.QListWidgetItem()
            item.setText(a[i])
            print(a[i])
            item.setSizeHint(QSize(60, 60))
            self.listWidget.addItem(QtWidgets.QListWidgetItem(item))

    def selectionChanged(self, item):
        print("Вы кликнули: {}".format(item.text()))
        n = list()
        if item.text() == "Все огородные растения":

            for i in aMain:
                if i[2] == "огородные":
                    print(1)
                    n.append(i[1])
        else:
            for i in aMain:
                if i[-1] == item.text().lower() and i[2] == "огородные":
                    print(1)
                    n.append(i[1])

        print(str(item.text()))
        nAll = list()
        for i in aMain:
            nAll.append(i[1])
        if item.text() in nAll:
            print(item.text())
            global aID
            aID = nAll.index(item.text())

            print(aID)
            self.close()
            self.showPlant = showPlant()
            self.showPlant.show()
        self.listWidget.clear()
        for i in range(len(n)):
            item = QtWidgets.QListWidgetItem()
            item.setText(n[i])
            item.setSizeHint(QSize(60, 60))
            self.listWidget.addItem(QtWidgets.QListWidgetItem(item))

    def toMenu(self):
        self.close()
        self.secondWidget = secondWindow()
        self.secondWidget.show()


class fruitAndBerryPlants(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        global flagLike
        flagLike = False
        uic.loadUi('yandex_TypePlants_widget.ui', self)
        self.setWindowTitle("fruitAndBerryPlants")
        self.button_toMenu.clicked.connect(self.toMenu)
        a = ["Все плодово-ягодные растения", "Деревья", "Кустарники", "Травянистые"]
        self.listWidget.itemClicked.connect(self.selectionChanged)
        for i in range(len(a)):
            item = QtWidgets.QListWidgetItem()
            item.setText(a[i])
            print(a[i])

            item.setSizeHint(QSize(60, 60))
            self.listWidget.addItem(QtWidgets.QListWidgetItem(item))

    def toMenu(self):
        self.close()
        self.secondWidget = secondWindow()
        self.secondWidget.show()

    def selectionChanged(self, item):
        print("Вы кликнули: {}".format(item.text()))
        n = list()
        if item.text() == "Все плодово-ягодные растения":

            for i in aMain:
                if i[2] == "плодово-ягодные":
                    print(1)
                    n.append(i[1])
        else:
            for i in aMain:
                if i[-1] == item.text().lower() and i[2] == "плодово-ягодные":
                    print(1)
                    n.append(i[1])

        print(str(item.text()))
        nAll = list()
        for i in aMain:
            nAll.append(i[1])
        if item.text() in nAll:
            global aID
            aID = nAll.index(item.text())
            print(aID)
            self.close()
            self.showPlant = showPlant()
            self.showPlant.show()
        self.listWidget.clear()
        for i in range(len(n)):
            item = QtWidgets.QListWidgetItem()
            item.setText(n[i])
            item.setSizeHint(QSize(60, 60))
            self.listWidget.addItem(QtWidgets.QListWidgetItem(item))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = firstWidget()
    ex.show()
    sys.exit(app.exec_())
