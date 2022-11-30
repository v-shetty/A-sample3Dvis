import sys
import PyQt5
import pyqtgraph
import pyqtgraph.opengl

PyQt5
pyqtgraph
pyqtgraph.opengl
import DLL

from model.model import Model
from view.view import MainView
# from view.viewTest import MainView
# from viewAPI import MainView


from PyQt5.QtWidgets import QApplication
from controller.controller import MainController
import model.GlobalFile as globalfile
from qt_material import apply_stylesheet


class App(QApplication):
    def __init__(self, sys_argv):

        super(App, self).__init__(sys_argv)
        self.model = Model()
        self.main_controller = MainController(self.model)
        globalfile.initialize()
        self.main_view = MainView(self.model, self.main_controller)
        apply_stylesheet(self, theme='dark_cyan.xml')
        self.main_view.show()


if __name__ == '__main__':
    app = App(sys.argv)

    sys.exit(app.exec_())
