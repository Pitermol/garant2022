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
    isActiveThen: bool  # Действителен ли на данную дату
    isActiveNow: bool  # Действителен ли на сегодня
    context: list  # Контекст
    date: str  # Дата для "isActiveThen"


class checkDocsRelevance:  # Основной класс с методами для формирования списка и HTML - таблицы
    def __init__(self, name, date, new_name):
        self.dateToCheck = date
        self.docxFile = None
        self.new_name = new_name
        self.docRawText = ""
        self.fileName = name
        self.operationStatus = True
        self.docType = self.fileName.split(".")[-1]
        config = configparser.ConfigParser()
        config.read('settings.ini')
        self.APIToken = config["api"]["token"]
        self.apiUrlMakeLinks = config["api"]["url_make_links"]
        self.apiAccept = config["api"]["accept"]
        self.apiContentType = config["api"]["content-type"]
        self.linksBaseUrl = config["api"]["linksBaseUrl"]
        self.apiUrlGetModifications = config["api"]["apiUrlGetModifications"]
        self.apiUrlGetDocInfo = config["api"]["apiUrlGetDocInfo"]

    def open_doc(self):  # Функция для открытия документа и его считывания
        try:
            if self.docType == "pdf":  # Если формат - PDF
                with fitz.open(f'input/{self.fileName}') as doc:
                    text = ""
                    for page in doc:
                        text += page.get_text()
                self.docRawText = text

                self.docRawText = self.docRawText.replace("\n", " ")
                self.docRawText = self.docRawText.replace("\t", " ")
                self.docRawText = self.docRawText.strip()
                while "  " in self.docRawText:
                    self.docRawText = self.docRawText.replace("  ", " ")
            elif self.docType == "docx":  # Если формат - DOCX
                self.docxFile = docx.Document(f'input/{self.fileName}')
                for para in range(len(self.docxFile.paragraphs)):
                    self.docRawText += " " + self.docxFile.paragraphs[para].text

                self.docRawText = self.docRawText.replace("\n", " ")
                self.docRawText = self.docRawText.replace("\t", " ")
                self.docRawText = self.docRawText.strip()
                while "  " in self.docRawText:
                    self.docRawText = self.docRawText.replace("  ", " ")
            elif self.docType == "txt":  # Если формат - TXT
                self.docxFile = open(f'input/{self.fileName}', "r")
                self.docRawText = self.docxFile.read()

                self.docRawText = self.docRawText.replace("\n", " ")
                self.docRawText = self.docRawText.replace("\t", " ")
                self.docRawText = self.docRawText.strip()
                while "  " in self.docRawText:
                    self.docRawText = self.docRawText.replace("  ", " ")
        except Exception as e:
            logging.error(e)

            result = {"successStatus": "False", "errorCode": "1", "sourceFileName": self.fileName}
            with open(f"output/{self.new_name}.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=False))
            f.close()
            self.operationStatus = False

            return

    def get_text(self) -> str:  # Возвращает полученный из документа текст
        return self.docRawText

    def make_doc_list(self) -> Optional[List[Document]]:  # Метод для создания списка из экземпляров класса "Document"
        self.open_doc()  # Получение текста на вход
        requestslist = []
        docsLinksList = []
        url = self.apiUrlMakeLinks  # Ссылка для запроса
        print(url)
        headers = {  # Заголовки для запроса
            'Accept': self.apiAccept,
            'Content-type': self.apiContentType,
            'Authorization': f'Bearer {self.APIToken}'
        }

        print(self.docRawText)
        text = ""
        ind = 0
        while ind < len(self.docRawText):  # Разделение текста на куски по 2000 символов
            ind += 2000
            cur = self.docRawText[ind - 2000:ind]
            payload = json.dumps({
                "text": cur,
                "baseUrl": self.linksBaseUrl
            })
            try:
                response = requests.request("POST", url, headers=headers,
                                        data=payload, timeout=30)  # Запрос для проставления ссылок в отрывке текста
            except Exception as e:
                logging.error(str(e) + ": Не удалось отправить запрос для проставления ссылок")

                result = {"successStatus": "False", "errorCode": "2", "sourceFileName": self.fileName}
                with open(f"output/{self.new_name}.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=False))
                f.close()
                self.operationStatus = False

                return []

            html = response.json()["text"]
            if ind != 2000:
                center = text[-30:] + html[:30]
                if "<a" not in center and "a>" not in center and "</a" not in center:
                    payload = json.dumps({
                        "text": center,
                        "baseUrl": self.linksBaseUrl
                    })
                    try:
                        response = requests.request("POST", url, headers=headers,
                                                data=payload,
                                                timeout=30)  # Запрос для проставления ссылок в отрывке текста
                    except Exception as e:
                        logging.error(str(e) + ": Не удалось отправить запрос для проставления ссылок")

                        result = {"successStatus": "False", "errorCode": "3", "sourceFileName": self.fileName}
                        with open(f"output/{self.new_name}.json", "w", encoding="utf-8") as f:
                            f.write(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=False))
                        f.close()
                        self.operationStatus = False

                        return []
                    text = text[:-30] + response.json()["text"] + html[30:]
                else:
                    text += html
            else:
                text += html

        if len(self.docRawText) % 2000 != 0:
            cur = self.docRawText[ind:]
            payload = json.dumps({
                "text": cur,
                "baseUrl": self.linksBaseUrl
            })
            try:
                response = requests.request("POST", url, headers=headers, data=payload, timeout=30)
                html = response.json()["text"]
                center = text[-30:] + html[:30]
                if "<a" not in center and "a>" not in center and "</a" not in center:
                    payload = json.dumps({
                        "text": center,
                        "baseUrl": self.linksBaseUrl
                    })
                    try:
                        response = requests.request("POST", url, headers=headers,
                                                    data=payload,
                                                    timeout=30)  # Запрос для проставления ссылок в отрывке текста
                    except Exception as e:
                        logging.error(str(e) + ": Не удалось отправить запрос для проставления ссылок")

                        result = {"successStatus": "False", "errorCode": "4", "sourceFileName": self.fileName}
                        with open(f"output/{self.new_name}.json", "w", encoding="utf-8") as f:
                            f.write(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=False))
                        f.close()
                        self.operationStatus = False

                        return []
                    text = text[:-30] + response.json()["text"] + html[30:]
                else:
                    text += html
            except Exception as e:
                logging.error(str(e) + ": Не удалось отправить запрос для проставления ссылок")

                result = {"successStatus": "False", "errorCode": "5", "sourceFileName": self.fileName}
                with open(f"output/{self.new_name}.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=False))
                f.close()
                self.operationStatus = False

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
                curDocContext = htmls[i - 1][-50:]
            except:
                curDocContext = htmls[i - 1]

            curDocContext += "<a href=\"" + htmls[i] + "</a>"

            try:
                if len(htmls) > i + 1:
                    curDocContext += htmls[i + 1][:50]
            except:
                if len(htmls) > i + 1:
                    curDocContext += htmls[i + 1]

            curDocContext = curDocContext.replace("<p>", "")
            curDocContext = curDocContext.replace("</p>", "")  # Контекст

            if link not in docsLinksList:
                docsLinksList.append(link)
                curDocContext = [curDocContext]
            else:
                requestslist[requestslist.index(list(filter(lambda x: x.link == link, requestslist))[0])].context.append(f" ...{curDocContext}...")
                continue

            htmlc = str(htmlc[0])
            htmlc = htmlc.split('document/')
            htmlc = htmlc[1]
            htmlc = htmlc.split('/')
            number = htmlc[0]  # Номер в системе Гарант

            url = self.apiUrlGetModifications

            payload = json.dumps({"topics": [number], "modDate": self.dateToCheck})
            headers = {
                'Authorization': f'Bearer {self.APIToken}mem',
                'Content-type': self.apiContentType,
                'Accept': self.apiAccept
            }
            try:
                response = requests.post(url, headers=headers, data=payload, timeout=30).json()[
                    "topics"]  # Запрос для получения сведений об акутальности документа на данную дату
            except Exception as e:
                logging.error(str(e) + ": Не удалось отправить запрос для получения изменений в документе с данной даты")

                result = {"successStatus": "False", "errorCode": "6", "sourceFileName": self.fileName}
                with open(f"output/{self.new_name}.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=False))
                f.close()
                self.operationStatus = False

                return []

            if len(response) == 0:
                isActiveThen = True
            else:
                isActiveThen = False
            print(number)
            url1 = f'{self.apiUrlGetDocInfo}{number}'
            headers1 = {
                'Accept': self.apiAccept,
                'Content-type': self.apiContentType,
                'Authorization': f'Bearer {self.APIToken}',
            }

            try:
                response1 = requests.get(url1,
                                     headers=headers1, timeout=30).json()  # Запрос для получения названия документа и сведений об актуальности на сегодня
            except Exception as e:
                logging.error(str(e) + ": Не удалось отправить запрос для проучения информации о документе")

                result = {"successStatus": "False", "errorCode": "7", "sourceFileName": self.fileName}
                with open(f"output/{self.new_name}.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=False))
                f.close()
                self.operationStatus = False

                return []
            # print(response1)
            curDocName = response1['name']
            isActiveNow = response1['status']
            if isActiveNow == "Действующие":
                isActiveNow = True
            else:
                isActiveNow = False

            a = Document(str(i // 2 + 1), number, link, curDocName, isActiveThen, isActiveNow, curDocContext,
                         self.dateToCheck)  # Создание объекта документа
            requestslist.append(a)

        return requestslist

    def create_table(self):  # Метод для формирования HTML - Файла с таблицой документов
        data = self.make_doc_list()
        if not self.operationStatus:
            return

        changed = inactive = 0
        docLinksList = []
        for i, doc in enumerate(data, 1):
            docLinksList.append({"id": i, "docName": doc.name, "docLink": doc.link,
                                 "abolishedStatus": "True" if not doc.isActiveNow else "False",
                                 "changedStatus": "True" if not doc.isActiveThen else "False",
                                 "linkContext": doc.context})
            if not doc.isActiveNow:
                inactive += 1
            if not doc.isActiveThen:
                changed += 1

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
                                <td>{{doc.name}}</td>{% if doc.isActiveNow %}
                                <td>Действующий</td>{% else %}
                                <td>Недействующий</td>{% endif %}{% if doc.isActiveThen %}
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
            html = template.render(docs=data, given_date=self.dateToCheck)  # Формирование HTML
        except Exception as e:
            logging.error(str(e) + ": Не удалось сформировать HTML")

            result = {"successStatus": "False", "errorCode": "8", "sourceFileName": self.fileName}
            with open(f"output/{self.new_name}.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=False))
            f.close()

            return

        result = {"successStatus": "True", "errorCode": None, "sourceFileName": self.fileName,
                  "docLinksCount": len(data), "abolishedDocsCount": inactive,
                  "changedDocsCount": changed, "htmlResult": f"{self.new_name}.html", "docLinksList": docLinksList}

        with open(f"output/{self.new_name}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=False))
        f.close()

        # print(html)
        with open(f"output/{self.new_name}.html", "w", encoding='utf-8') as f:  # Запись в файл "output/template.html"
            f.write(html)
        f.close()


def start(date="2021-10-25"):  # Функция обработки множества файлов в папке input
    input_files = os.listdir("input")  # Список входных файлов
    for old_file in os.listdir("output"):
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)) + "/output", old_file))  # Удаление всех старых файлов в папке output

    for i, newFile in enumerate(input_files):  # Перебор входных файлов
        obj = checkDocsRelevance(newFile, date, f"out_{str(i + 1)}")  # Создание экземпляра основного класса
        obj.create_table()  # Вызов метода для формирования таблицы


start()
