#!/usr/bin/env python3
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from player import Player
from categories import Categories
from youtube import YouTubeView


class MainWidget(QWidget):
    current_view = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.youtube = YouTubeView(self)
        self.views = (self.youtube, )

    def _show_view(self, view):
        [v.hide() for v in self.views if v != view]
        if view.rendered:
            view.show()
        else:
            view.render()
        self.window().categories.hide()
        view.setFocus()
        self.current_view = view

    def show_youtube(self):
        self._show_view(self.youtube)

    def keyPressEvent(self, event):
        print(event.key())
        self.current_view.keyPressEvent(event)


class Main(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.container = MainWidget(self)
        self.container.setStyleSheet("""
            QWidget {
                background-color: rgba(30,30,30, 1);
                color: #fff;
            }
        """)
        self.setCentralWidget(self.container)
        self.container.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.container.setAttribute(Qt.WA_NativeWindow)

        self.categories = Categories(self.container)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.categories, Qt.Vertical)

        self.player = Player(str(int(self.container.winId())))

        #player = mpv.MPV(wid=str(int(self.container.winId())),
        #        vo='vdpau', # You may not need this
        #        log_handler=print)
        #player.play(sys.argv[1])


app = QApplication(sys.argv)

# This is necessary since PyQT stomps over the locale settings needed by libmpv.
# This needs to happen after importing PyQT before creating the first mpv.MPV instance.
import locale
locale.setlocale(locale.LC_NUMERIC, 'C')
win = Main()
win.categories.render()
win.setAttribute(Qt.WA_NoSystemBackground, True)
win.setAttribute(Qt.WA_TranslucentBackground, True)
win.show()
sys.exit(app.exec_())