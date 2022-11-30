import PyQt5
from PyQt5 import QtCore
from Visualizer3D.model.model import Model
from Visualizer3D.controllers.main_controller import MainController
from Visualizer3D.gui.PCLVisualizer import PCLVisualizerWindow



class App(QtCore.QObject):
    def __init__(self):
        super(App, self).__init__()
        self.model = Model()
        self.main_controller = MainController(self.model)
        self.main_view = PCLVisualizerWindow(self.model, self.main_controller)

# if __name__ == '__main__':
#     app = App(sys.argv)
#     # apply_stylesheet(app, theme='dark_cyan.xml')
#     sys.exit(app.exec_())



