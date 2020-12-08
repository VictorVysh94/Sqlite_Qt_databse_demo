import os,sys,sqlite3
from PyQt5 import QtWidgets, uic,QtGui,QtCore
from PyQt5.QtCore import QThread,Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QFontDialog,QFileDialog,QMessageBox,QTableWidgetItem,QMenu,QShortcut,QApplication

class ui_handler:
    def __init__(self,parent):
        self.parent = parent
        self.setup_tables_header()
        self.fill_tables()
        self.setup_triggers()

    # Привязка кнопок и сигналов к функциям и командам
    def setup_triggers(self):
        # Кнопка "убрать" делает запрос в базу данных на удаление аренды.
        self.parent.del_user_button.clicked.connect(self.delete_client)
        
        # Кнопка "удалить" делает запрос в базу данных на удаление аренды.
        self.parent.del_rent_button.clicked.connect(self.delete_rent)
        
        # Кнопка "добавить" пользователя должна перебрасывать фокус на вкладку пользователей
        self.parent.open_user_btn.clicked.connect(self.users_select_mode)
        
        # Кнопка "добавить" книгу должна перебрасывать фокус на вкладку пользователей
        self.parent.open_book_btn.clicked.connect(self.books_select_mode)
        
        # Кнопка "добавить" в аренду должна делать запрос в базу с параметрами из двух QLineEdit
        self.parent.add_new_rent_button.clicked.connect(self.add_new_rent_book)
        
        # Кнопка "добавить" юзера делает запрос в базу данных  с параметрами из двух QLineEdit
        self.parent.add_new_user_button.clicked.connect(self.add_new_user)
        
        # Привязываем действие "текст изменился" у QLineEdit для книг в вкладке book к функции
        self.parent.book_searchLine.textChanged.connect(self.book_text_changed)
        
        # Привязываем действие "текст изменился" у QLineEdit для ФИО в вкладке users к функции
        self.parent.user_FIO_1.textChanged.connect(self.FIO_text_changed)
        
        # Привязываем действие "текст изменился" у QLineEdit для Карта в вкладке users к функции
        self.parent.user_card_1.textChanged.connect(self.CARD_text_changed)

    def delete_client(self):
        try:
            self.parent.db.sql_del_client(self.parent.users_table.item(self.parent.users_table.currentRow(),0).text())
            self.fill_tables()
        except Exception as ex:
            print(ex)

    def delete_rent(self):
        try:
            self.parent.db.sql_del_rent(self.parent.rent_table.item(self.parent.rent_table.currentRow(),0).text())
            self.fill_tables()
        except Exception as ex:
            print(ex)

    def add_new_user(self):
        if self.parent.user_FIO_1.text() != "" and self.parent.user_card_1.text() != "":
            self.parent.db.sql_new_user(self.parent.user_FIO_1.text(),self.parent.user_card_1.text())
            self.fill_tables()
        else:
            pass

    def CARD_text_changed(self,text):
        if text == "":
            self.clear_table(self.parent.users_table)
            self.fill_clients()
        else:
            self.clear_table(self.parent.users_table)
            self.load_card_by_search(text)
        
    def load_card_by_search(self,text):
        search_text = text.lower()
        for cli in self.parent.db.clients:
            if search_text in str(cli.Key).lower():
                pass
            else:
                continue
            append_data = [str(cli.ID),
                           cli.Name,
                           str(cli.Key)]
            self.fill_data(self.parent.users_table,append_data)

    def FIO_text_changed(self,text):
        if text == "":
            self.clear_table(self.parent.users_table)
            self.fill_clients()
        else:
            self.clear_table(self.parent.users_table)
            self.load_fio_by_search(text)
        
    def load_fio_by_search(self,text):
        search_text = text.lower()
        for cli in self.parent.db.clients:
            if search_text in cli.Name.lower():
                pass
            else:
                continue
            append_data = [str(cli.ID),
                           cli.Name,
                           str(cli.Key)]
            self.fill_data(self.parent.users_table,append_data)

    
    def users_select_mode(self):
        try:
            self.parent.MainTab.setCurrentIndex(1)
            tabs = [self.parent.book_tab,self.parent.rent_tab]
            for tab1 in tabs:
                tab1.setDisabled(1)
            self.parent.users_table.keyPressEvent = self.keyPressEvent_on_users_select
        except Exception as ex:
            print(ex)

    def keyPressEvent_on_users_select(self,event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:            
            tabs = [self.parent.book_tab,self.parent.rent_tab]
            for tab1 in tabs:
                tab1.setEnabled(1)
            self.parent.MainTab.setCurrentIndex(2)
            self.parent.user_Line1.setText(self.parent.users_table.item(self.parent.users_table.currentRow(),0).text())
            self.parent.users_table.keyPressEvent = None

    def add_new_rent_book(self):
        usr  = self.parent.user_Line1.text()
        book = self.parent.book_Line1.text()
        if usr == "" or book == "":
            pass
        else:
            try:
                self.parent.db.sql_new_rent(usr,book)
                self.fill_tables()
            except Exception as ex:
                print(ex)
                
    def books_select_mode(self):
        self.parent.MainTab.setCurrentIndex(0)
        tabs = [self.parent.user_tab,self.parent.rent_tab]
        for tab1 in tabs:
            tab1.setDisabled(1)
        self.parent.books_table.keyPressEvent = self.keyPressEvent_on_book_select

    def keyPressEvent_on_book_select(self,event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:            
            tabs = [self.parent.user_tab,self.parent.rent_tab]
            for tab1 in tabs:
                tab1.setEnabled(1)
            self.parent.MainTab.setCurrentIndex(2)
            self.parent.book_Line1.setText(self.parent.books_table.item(self.parent.books_table.currentRow(),0).text())
            self.parent.books_table.keyPressEvent = None
        
    def book_text_changed(self,text):
        if text == "":
            self.clear_table(self.parent.books_table)
            self.fill_books()
        else:
            self.clear_table(self.parent.books_table)
            self.load_book_by_search(text)

    def load_book_by_search(self,text):
        search_text = text.lower()
        for bok in self.parent.db.books:
            if self.parent.book_comboBox.currentIndex() == 0: # 0 - Name
                if search_text in bok.Name.lower():
                    pass
                else:
                    continue
            elif self.parent.book_comboBox.currentIndex() == 1: # 1 - Date
                if search_text in str(bok.Release).lower():
                    pass
                else:
                    continue
            elif self.parent.book_comboBox.currentIndex() == 2: # 2 - Pub
                if search_text in str(bok.Publisher.Name).lower():
                    pass
                else:
                    continue
            append_data = [str(bok.ID),bok.Name,
                           str(bok.Author.Name),str(bok.Publisher.Name),
                           str(bok.Release),str(bok.Amount)]
            self.fill_data(self.parent.books_table,append_data)

    #============================================ РАБОТА С ТАБЛИЦАМИ ==========================================#

    #=============== ЗАПОЛНЕНИЕ ВСЕХ ТАБЛИЦ ПО ОЧЕРЕДИ =============#
    def fill_tables(self):                                          #
        self.parent.db.load_base()                                  #
        self.clear_table(self.parent.users_table)                   #
        self.fill_clients()                                         #
        self.clear_table(self.parent.books_table)                   #
        self.fill_books()                                           #
        self.clear_table(self.parent.rent_table)                    #
        self.fill_rents()                                           #
    #===============================================================#

    #====== ОЧИСТКА УКАЗАННОЙ ТАБЛИЦЫ ======#
    def clear_table(self,table):            #
        while table.rowCount() > 0:         #
            table.removeRow(0)              #
    #=======================================#

    #============ ЗАПОЛНЕНИЕ ТАБЛИЦЫ ОСНОВЫВАЯСЬ НА ПЕРЕДАННЫХ АРГУМЕНАХ ===============#
    def fill_data(self,table,append_data):                                              #
        cur_row = table.rowCount()                                                      #
        table.insertRow(cur_row)                                                        #
        for counter in range(len(append_data)):                                         #
                table.setItem(cur_row,counter,QTableWidgetItem(append_data[counter]))   #
    #===================================================================================#

    #===================== ЗАПОЛНЕНИЕ КЛИЕНТОВ =================#
    def fill_clients(self):                                     #
        for cli in self.parent.db.clients:                      #
            append_data = [str(cli.ID),                         #
                           cli.Name,                            #
                           str(cli.Key)]                        #
            self.fill_data(self.parent.users_table,append_data) #
    #===========================================================#

    #===================== ЗАПОЛНЕНИЕ КНИГ =================================#
    def fill_books(self):                                                   #
        for bok in self.parent.db.books:                                    #
            append_data = [str(bok.ID),bok.Name,                            #
                           str(bok.Author.Name),str(bok.Publisher.Name),    #
                           str(bok.Release),str(bok.Amount)]                #
            self.fill_data(self.parent.books_table,append_data)             #
    #=======================================================================#

    #===================== ЗАПОЛНЕНИЕ АРЕНДЫ ===================#
    def fill_rents(self):                                       #
        for ren in self.parent.db.rents:                        #
            append_data = [str(ren.ID),ren.Client.Name,         #
                           str(ren.Book.Name),str(ren.Date)]    #
            self.fill_data(self.parent.rent_table,append_data)  #
    #===========================================================#

    #============================================ РАБОТА С ТАБЛИЦАМИ ==========================================#

    #============================== НАСТРОЙКА ЗАГОЛОВКОВ У ТАБЛИЦ ==================================#    
    def setup_tables_header(self):                                                                  #
        header_list = [[self.parent.users_table.horizontalHeader(),2],                              #
                       [self.parent.books_table.horizontalHeader(),5],                              #
                       [self.parent.rent_table.horizontalHeader(),3]]                               #
        for header in header_list:                                                                  #
            for current in range(header[1]):                                                        #
                header[0].setSectionResizeMode(current, QtWidgets.QHeaderView.ResizeToContents)     #
    #============================== НАСТРОЙКА ЗАГОЛОВКОВ У ТАБЛИЦ ==================================#
