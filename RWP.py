import requests
from bs4 import BeautifulSoup
import sqlite3
# PyQt5.QtWebEngine
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtWebEngineWidgets import *


class RandomWikiPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(800, 900)
        self.setWindowTitle('Случайная статья из Википедии')

        self.random_btn = QPushButton("Случайная статья", self)
        self.random_btn.resize(150, 30)
        self.random_btn.move(225, 10)
        self.random_btn.setFont(QFont('Arial', 10))



        self.list_of_pages = QPushButton("Просмотренные статьи", self)
        self.list_of_pages.resize(150, 30)
        self.list_of_pages.move(405, 10)
        self.list_of_pages.setFont(QFont('Arial', 10))

        self.web = QWebEngineView(self)
        self.web.resize(700, 800)
        self.web.move(50, 50)

        # random_wiki_url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%A1%D0%BB%D1%83%D1%87%D0%B0%D0%B9%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'
        # page = requests.get(random_wiki_url)  # получение html кода
        # page_url = page.url
        # self.web.load(QUrl(page_url))

        self.random_btn.clicked.connect(self.show_page)


    def show_page(self):
        random_wiki_url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%A1%D0%BB%D1%83%D1%87%D0%B0%D0%B9%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'
        page = requests.get(random_wiki_url)  # получение html кода
        page_url = page.url  # ссылка на страницу
        soup = BeautifulSoup(page.text, "html.parser")  # html код сайта
        page_title = soup.find("title").text
        page_title = page_title.split(" — ")[0]
        print(page_title)
        print(page_url)

        self.web.load(QUrl(page_url))
        self.take_data_to_db(page_title, page_url)

    def take_data_to_db(page_title, page_url):
        conn = sqlite3.connect("db.sqlite")
        with conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO VisitedPages(title, url) VALUES(?, ?)  """, (page_title, page_url))
            conn.commit()
        conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    rwp = RandomWikiPage()
    rwp.show()
    sys.exit(app.exec())