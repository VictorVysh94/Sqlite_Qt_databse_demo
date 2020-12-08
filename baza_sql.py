import os,sys,sqlite3
from baza_objects import *
import datetime

#===========================================================#
# Данный файл содержит класс для работы с базой данных.     #
# Загрузка данных в переменные по объектам из baza_objects  #
# Так же планируется функционал добавления новых записей,   #
# удаления и редактирования.                                #
#===========================================================#

class data_base:
    def __init__(self):
        self.data_base  = sqlite3.connect("data.db")
        self.clear_variables()

    #===== Переменные для хранения данных из базы ======#
    def clear_variables(self):                          #
        self.books      = list()                        #
        self.authors    = list()                        #
        self.publishers = list()                        #
        self.rents      = list()                        #
        self.clients    = list()                        #
    #===== Переменные для хранения данных из базы ======#


    def sql_del_rent(self,rent_id):
        cursor = self.data_base.cursor()                                                                            #
        cursor.execute("DELETE FROM Rents WHERE ID={}".format(rent_id))
        self.data_base.commit()

    def sql_del_client(self,client_id):
        cursor = self.data_base.cursor()                                                                            #
        cursor.execute("DELETE FROM Clients WHERE ID={}".format(client_id))
        self.data_base.commit()
        
    #================================== Функция добавления новой аренды ============================================#
    def sql_new_rent(self,user_id,book_id):                                                                         #
        cursor = self.data_base.cursor()                                                                            #
        cursor.execute("INSERT INTO Rents (Client,Book,Date) VALUES({},{},'{}')".format(user_id,                    #
                                                                                        book_id,                    #
                                                                                        datetime.datetime.now()))   #
        self.data_base.commit()                                                                                     #
    #===============================================================================================================#

    #======================= Функция добавления нового пользователя ================================#
    def sql_new_user(self,user_fio,user_card):                                                      #
        cursor = self.data_base.cursor()                                                            #
        cursor.execute("INSERT INTO Clients (Name,Key) VALUES('{}',{})".format(user_fio,user_card)) #
        self.data_base.commit()                                                                     #
    #===============================================================================================#

    #=================== Функция загрузки Аренды ===================#
    def load_rent(self):                                            #
        cursor = self.data_base.cursor()                            #
        cursor.execute("SELECT * FROM Rents")                       #
        for ren_line in cursor.fetchall():                          #
            temp_ren                = Client()                      #
            temp_ren.ID             = ren_line[0]                   #
            temp_ren.Client         = self.get_client(ren_line[1])  #
            temp_ren.Book           = self.get_book(ren_line[2])    #
            temp_ren.Date           = ren_line[3]                   #
            self.rents.append(temp_ren)                             #
    #===============================================================#

    #========== Функция загрузки Клиентов ==========#
    def load_cli(self):                             #
        cursor = self.data_base.cursor()            #
        cursor.execute("SELECT * FROM Clients")     #
        for cli_line in cursor.fetchall():          #
            temp_cli                = Client()      #
            temp_cli.ID             = cli_line[0]   #
            temp_cli.Name           = cli_line[1]   #
            temp_cli.Key            = cli_line[2]   #
            self.clients.append(temp_cli)           #
    #===============================================#

    #==================== Функция загрузки Книг ====================#
    def load_books(self):                                           #
        cursor = self.data_base.cursor()                            #
        cursor.execute("SELECT * FROM Books")                       #
        for book_line in cursor.fetchall():                         #
            temp_book               = Book()                        #
            temp_book.ID            = book_line[0]                  #
            temp_book.Name          = book_line[1]                  #
            temp_book.Author        = self.get_author(book_line[2]) #
            temp_book.Publisher     = self.get_pub(book_line[3])    #
            temp_book.Release       = book_line[4]                  #
            temp_book.Amount        = book_line[5]                  #
            self.books.append(temp_book)                            #
    #===============================================================#

    #========== Функция загрузки Авторов ===========#
    def load_aut(self):                             #
        cursor = self.data_base.cursor()            #
        cursor.execute("SELECT * FROM Authors")     #
        for aut_line in cursor.fetchall():          #
            temp_aut                = Author()      #
            temp_aut.ID             = aut_line[0]   #
            temp_aut.Name           = aut_line[1]   #
            self.authors.append(temp_aut)           #
    #===============================================#

    #=========== Функция загрузки Издателей ========#
    def load_pub(self):                             #
        cursor = self.data_base.cursor()            #
        cursor.execute("SELECT * FROM Publishers")  #
        for pub_line in cursor.fetchall():          #
            temp_pub                = Publisher()   #
            temp_pub.ID             = pub_line[0]   #
            temp_pub.Name           = pub_line[1]   #
            temp_pub.Adr            = pub_line[2]   #
            self.publishers.append(temp_pub)        #
    #===============================================#


    #======================= Фукнции получения объекта по ID =======================#
                                                                                    #
    #=========== ИЗДАТЕЛИ ==========#                                               #
    def get_pub(self,pub_id):       #                                               #
        for pub in self.publishers: #                                               #
            if pub_id == pub.ID:    #                                               #
                return pub          #                                               #
    #===============================#                                               #
                                                                                    #
    #============ АВТОРЫ ===========#                                               #
    def get_author(self,aut_id):    #                                               #
        for aut in self.authors:    #                                               #
            if aut_id == aut.ID:    #                                               #
                return aut          #                                               #
    #===============================#                                               #
                                                                                    #
    #============= КНИГИ ===========#                                               #
    def get_book(self,book_id):     #                                               #
        for book in self.books:     #                                               #
            if book_id == book.ID:  #                                               #
                return book         #                                               #
    #===============================#                                               #
                                                                                    #
    #============= КЛИЕНТЫ =============#                                           #
    def get_client(self,client_id):     #                                           #
        for client in self.clients:     #                                           #
            if client_id == client.ID:  #                                           #
                return client           #                                           #
    #===================================#                                           #
                                                                                    #
    #======================= Фукнция получения объекта по ID =======================#

    def load_base(self):
        self.clear_variables()
        self.load_pub()
        self.load_aut()
        self.load_cli()
        self.load_books()
        self.load_rent()
