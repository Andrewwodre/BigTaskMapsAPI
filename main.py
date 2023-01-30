import os
import sys
from PyQt5.QtCore import Qt
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PIL import Image
SCREEN_SIZE = [600, 600]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.pixmap = QPixmap()
        self.image = QLabel(self)
        self.image.setPixmap(self.pixmap)
        self.image.move(0, 0)
        self.image.resize(*SCREEN_SIZE)
        #self.image.setPixmap(self.pixmap)
        self.ll = f"{input()},{input()}"
        self.spn = "0.002,0.002"
        self.map = "map"
        self.zoom = int(input())
        self.map_params = {
            "ll": self.ll,
            "l": self.map,
            "z": self.zoom
        }
        self.initUI()
        self.getImage()
        self.reload()

    def getImage(self):
        map_request = "http://static-maps.yandex.ru/1.x/"
        #ll=&spn=&l=map
        self.response = requests.get(map_request, self.map_params)

        if not self.response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", self.response.status_code, "(", self.response.reason, ")")
            sys.exit(1)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

    def reload(self):
        self.pixmap.loadFromData(self.response.content)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            self.zoom = int(self.zoom) - 1 if int(self.zoom) > 0 else self.zoom
            self.map_params["z"] = self.zoom
        if event.key() == Qt.Key_PageUp:
            self.zoom = int(self.zoom) + 1 if int(self.zoom) < 17 else self.zoom
            self.map_params["z"] = self.zoom
        self.getImage()
        self.reload()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
