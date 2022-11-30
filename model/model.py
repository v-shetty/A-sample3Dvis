from PyQt5.QtCore import QObject, pyqtSignal


class Model(QObject):
    file_name_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._file_name = ''
        self.RangeImage = 0

    #@property
    def file_name(self):
        return self._file_name

    #
    def file_name(self, value):
        self._file_name = value
        # update in model is reflected in view by sending a signal to view
        self.file_name_changed.emit(value)
        print("executed")
