import json
import os
import re
import configparser

import docx
import jinja2
from dataclasses import dataclass
import requests
import fitz
from typing import List, Optional
import logging


@dataclass
class Document:  # Создается класс для удобного хранения данных о документе в виде объекта
    num: str  # Номер по счету
    index: str  # $topic
    link: str  # Ссылка
    name: str  # Названи документа
    is_active_then: bool  # Действителен ли на данную дату
    is_active_now: bool  # Действителен ли на сегодня
    context: str  # Контекст
    date: str  # Дата для "is_active_then"


class checkDocsRelevance:  # Основной класс с методами для формирования списка и HTML - таблицы
    def __init__(self, name, date):
        self.date = date
        self.reader = None
        self.file = None
        self.text = ""
        self.name = name
        self.type = self.name.split(".")[-1]
        config = configparser.ConfigParser()
        config.read('settings.ini')
        self.token = config["api"]["token"]
        self.url_make_links = config["api"]["url_make_links"]
        self.accept = config["api"]["accept"]
        self.content_type = config["api"]["content-type"]
        self.links_base_url = config["api"]["links_base_url"]
        self.url_get_modifications = config["api"]["url_get_modifications"]
        self.url_get_doc_info = config["api"]["url_get_doc_info"]

    def open_doc(self):  # Функция для открытия документа и его считывания
        try:
            if self.type == "pdf":  # Если формат - PDF
                with fitz.open(f'input/{self.name}') as doc:
                    text = ""
                    for page in doc:
                        text += page.get_text()
                self.text = text

                self.text = self.text.replace("\n", " ")
                self.text = self.text.replace("\t", " ")
                self.text = self.text.strip()
                while "  " in self.text:
                    self.text = self.text.replace("  ", " ")
            elif self.type == "docx":  # Если формат - DOCX
                self.file = docx.Document(f'input/{self.name}')
                for para in range(len(self.file.paragraphs)):
                    self.text += " " + self.file.paragraphs[para].text

                self.text = self.text.replace("\n", " ")
                self.text = self.text.replace("\t", " ")
                self.text = self.text.strip()
                while "  " in self.text:
                    self.text = self.text.replace("  ", " ")
            elif self.type == "txt":  # Если формат - TXT
                self.file = open(f'input/{self.name}', "r")
                self.text = self.file.read()

                self.text = self.text.replace("\n", " ")
                self.text = self.text.replace("\t", " ")
                self.text = self.text.strip()
                while "  " in self.text:
                    self.text = self.text.replace("  ", " ")
        except Exception as e:
            logging.error(e)

    def get_text(self) -> str:  # Возвращает полученный из документа текст
        return self.text

    def make_doc_list(self) -> Optional[List[Document]]:  # Метод для создания списка из экземпляров класса "Document"
        self.open_doc()  # Получение текста на вход
        requestslist = []
        url = self.url_make_links  # Ссылка для запроса
        print(url)
        headers = {  # Заголовки для запроса
            'Accept': self.accept,
            'Content-type': self.content_type,
            'Authorization': f'Bearer {self.token}'
        }

        print(self.text)
        text = ""
        ind = 0
        while ind < len(self.text):  # Разделение текста на куски по 2000 символов
            ind += 2000
            cur = self.text[ind - 2000:ind]
            payload = json.dumps({
                "text": cur,
                "baseUrl": self.links_base_url
            })
            try:
                response = requests.request("POST", url, headers=headers,
                                        data=payload, timeout=30)  # Запрос для проставления ссылок в отрывке текста
            except Exception as e:
                logging.error(str(e) + ": Не удалось отправить запрос для проставления ссылок")
                return []

            html = response.json()["text"]
            if ind != 2000:
                center = text[-30:] + html[:30]
                if "<a" not in center and "a>" not in center and "</a" not in center:
                    payload = json.dumps({
                        "text": center,
                        "baseUrl": self.links_base_url
                    })
                    try:
                        response = requests.request("POST", url, headers=headers,
                                                data=payload,
                                                timeout=30)  # Запрос для проставления ссылок в отрывке текста
                    except Exception as e:
                        logging.error(str(e) + ": Не удалось отправить запрос для проставления ссылок")
                        return []
                    text = text[:-30] + response.json()["text"] + html[30:]
                else:
                    text += html
            else:
                text += html

        if len(self.text) % 2000 != 0:
            cur = self.text[ind:]
            payload = json.dumps({
                "text": cur,
                "baseUrl": self.links_base_url
            })
            try:
                response = requests.request("POST", url, headers=headers, data=payload, timeout=30)
                html = response.json()["text"]
                center = text[-30:] + html[:30]
                if "<a" not in center and "a>" not in center and "</a" not in center:
                    payload = json.dumps({
                        "text": center,
                        "baseUrl": self.links_base_url
                    })
                    try:
                        response = requests.request("POST", url, headers=headers,
                                                    data=payload,
                                                    timeout=30)  # Запрос для проставления ссылок в отрывке текста
                    except Exception as e:
                        logging.error(str(e) + ": Не удалось отправить запрос для проставления ссылок")
                        return []
                    text = text[:-30] + response.json()["text"] + html[30:]
                else:
                    text += html
            except Exception as e:
                logging.error(str(e) + ": Не удалось отправить запрос для проставления ссылок")

                return []
            # print(response.text)

        html = text
        htmls = re.split("<a href=\"|</a>", html)
        # print(html)

        for i in range(1, len(htmls),
                       2):  # Поиск всех документов, извлечение ссылок, их номеров в системе Гарант и контекста
            htmlc = htmls[i]
            htmlc = re.split('"', htmlc)
            link = htmlc[0]  # Ссылка
            try:
                cur_context = htmls[i - 1][-50:]
            except:
                cur_context = htmls[i - 1]

            cur_context += "<a href=\"" + htmls[i] + "</a>"

            try:
                if len(htmls) > i + 1:
                    cur_context += htmls[i + 1][:50]
            except:
                if len(htmls) > i + 1:
                    cur_context += htmls[i + 1]

            cur_context = cur_context.replace("<p>", "")
            cur_context = cur_context.replace("</p>", "")  # Контекст

            htmlc = str(htmlc[0])
            htmlc = htmlc.split('document/')
            htmlc = htmlc[1]
            htmlc = htmlc.split('/')
            number = htmlc[0]  # Номер в системе Гарант

            url = self.url_get_modifications

            payload = json.dumps({"topics": [number], "modDate": self.date})
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-type': self.content_type,
                'Accept': self.accept
            }
            try:
                response = requests.post(url, headers=headers, data=payload, timeout=30).json()[
                    "topics"]  # Запрос для получения сведений об акутальности документа на данную дату
            except Exception as e:
                logging.error(str(e) + ": Не удалось отправить запрос для получения изменений в документе с данной даты")
                return []

            if len(response) == 0:
                is_active_then = True
            else:
                is_active_then = False
            print(number)
            url1 = f'{self.url_get_doc_info}{number}'
            headers1 = {
                'Accept': self.accept,
                'Content-type': self.content_type,
                'Authorization': f'Bearer {self.token}',
            }

            try:
                response1 = requests.get(url1,
                                     headers=headers1, timeout=30).json()  # Запрос для получения названия документа и сведений об актуальности на сегодня
            except Exception as e:
                logging.error(str(e) + ": Не удалось отправить запрос для проучения информации о документе")
                return []
            # print(response1)
            namme = response1['name']
            is_active_now = response1['status']
            if is_active_now == "Действующие":
                is_active_now = True
            else:
                is_active_now = False

            a = Document(str(i // 2 + 1), number, link, namme, is_active_then, is_active_now, cur_context,
                         self.date)  # Создание объекта документа
            requestslist.append(a)

        return requestslist

    def create_table(self, new_name):  # Метод для формирования HTML - Файла с таблицой документов
        data = self.make_doc_list()
        changed = inactive = active = 0
        for doc in data:
            if doc.is_active_now:
                active += 1
            else:
                inactive += 1
            if not doc.is_active_then:
                changed += 1
        result = {self.name: {"output_file_name": f"{new_name}.html", "all": len(data), "changed": changed, "inactive": inactive, "active": active}}
        with open(f"output/{new_name}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(result))
        f.close()
        # print(data)

        template = jinja2.Template('''<!DOCTYPE html>
        <html>
            <head>
                <title>Docs list</title>
                <link rel="stylesheet" href="style.css">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css"  rel="stylesheet">
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js"></script>
            </head>
            <body>
                <header></header>
                <div style="margin-top:3%" align="center">
                    <table class="table table-striped" style="width:90%; word-break: normal;">
                        <thead>
                            <tr>
                                <th scope="col">#</th>
                                <th scope="col">Документ</th>
                                <th scope="col">Статус на сегодня</th>
                                <th scope="col">Изменялся ли с {{given_date}}</th>
                                <th scope="col">Контекст</th>
                            </tr>
                        </thead>
                        <tbody>{% for doc in docs %}
                            <tr>
                                <th scope="row">{{doc.num}}</th>
                                <td>{{doc.name}}</td>{% if doc.is_active_now %}
                                <td>Действующий</td>{% else %}
                                <td>Недействующий</td>{% endif %}{% if doc.is_active_then %}
                                <td>Нет</td>{% else %}
                                <td>Да</td>{% endif %}
                                <td>...{{doc.context}}...</td>
                            </tr>{% endfor %}
                        </tbody>
                    </table>
                </div>
            </body>
        </html>''')
        try:
            html = template.render(docs=data, given_date=self.date)  # Формирование HTML
        except Exception as e:
            logging.error(str(e) + ": Не удалось сформировать HTML")
            return

        # print(html)
        with open(f"output/{new_name}.html", "w", encoding='utf-8') as f:  # Запись в файл "output/template.html"
            f.write(html)
        f.close()


def start(date="2021-10-25"):  # Функция обработки множества файлов в папке input
    input_files = os.listdir("input")  # Список входных файлов
    for old_file in os.listdir("output"):
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)) + "/output", old_file))  # Удаление всех старых файлов в папке output

    for i, new_file in enumerate(input_files):  # Перебор входных файлов
        obj = checkDocsRelevance(new_file, date)  # Создание экземпляра основного класса
        obj.create_table(f"out_{str(i + 1)}")  # Вызов метода для формирования таблицы

# obj = checkDocsRelevance("test.pdf", "2021-10-25")
# obj.create_table("out")

# start()
