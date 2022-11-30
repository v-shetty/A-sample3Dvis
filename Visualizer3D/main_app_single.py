import sys
from PyQt5.QtWidgets import QApplication
from Visualizer3D.model.model import Model
from Visualizer3D.controllers.main_controller import MainController
from Visualizer3D.gui.PCLVisualizer import PCLVisualizerWindow
import qdarkstyle


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = Model()
        self.main_controller = MainController(self.model)
        self.main_view = PCLVisualizerWindow(self.model, self.main_controller)

        # apply_stylesheet(self.main_view, theme='dark_cyan.xml')

        palette = qdarkstyle.DarkPalette
        # dark_stylesheet = qdarkstyle._load_stylesheet('PyQt5', palette)
        dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
        self.main_view.setStyleSheet(dark_stylesheet)

        self.main_view.show()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())



