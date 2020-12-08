from baza_sql import *
from baza_ui_handler import *

#===============================#
# Этот файл создан как основной #
# для запуска интерфейса.       #
# Волшебство происходит не тут. #
#===============================#

class ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(ui, self).__init__()
        uic.loadUi('interface.ui', self)    # Загружаем файл.
        self.db = data_base()               # Загружаем базу.
        self.uih = ui_handler(self)         # Загружаем обработчик кнопок\интерфейса
        self.show()                         # Показываем наш GUI.

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ui()
    app.exec_()
