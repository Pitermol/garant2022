import json
import re

import PyPDF2
import docx
import jinja2
from dataclasses import dataclass
import requests
from tika import parser
import fitz


@dataclass
class Document:
    num: str
    index: str
    link: str
    name: str
    is_active_then: bool
    is_active_now: bool
    context: str
    date: str


class checkDocsRelevance:
    def __init__(self, name, date):
        self.date = date
        self.reader = None
        self.file = None
        self.text = ""
        self.name = name
        self.type = self.name.split(".")[-1]

    def open_doc(self):
        if self.type == "pdf":
            with fitz.open(f'input/{self.name}') as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
            self.text = text
            # self.file = open(f'input/{self.name}', "rb")
            # self.reader = PyPDF2.PdfFileReader(self.file)
            # for page in range(self.reader.numPages):
            #     try:
            #         page_text = self.reader.getPage(page).extractText()
            #         self.text += " " + page_text
            #     except:
            #         print(page)
            #         continue
            # print(self.text)

            self.text = self.text.replace("\n", " ")
            self.text = self.text.replace("\t", " ")
            self.text = self.text.strip()
            while "  " in self.text:
                self.text = self.text.replace("  ", " ")
        elif self.type == "docx":
            self.file = docx.Document(f'input/{self.name}')
            for para in range(len(self.file.paragraphs)):
                self.text += " " + self.file.paragraphs[para].text

            self.text = self.text.replace("\n", " ")
            self.text = self.text.replace("\t", " ")
            self.text = self.text.strip()
            while "  " in self.text:
                self.text = self.text.replace("  ", " ")
        elif self.type == "txt":
            self.file = open(f'input/{self.name}', "r")
            self.text = self.file.read()

            self.text = self.text.replace("\n", " ")
            self.text = self.text.replace("\t", " ")
            self.text = self.text.strip()
            while "  " in self.text:
                self.text = self.text.replace("  ", " ")

    def get_text(self) -> str:
        return self.text

    def make_doc_list(self):
        self.open_doc()
        requestslist = []
        url = "https://api.garant.ru/v1/find-hyperlinks"
        headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json',
            'Authorization': 'Bearer f4e1a77c651811eab20b0050568d72f0'
        }

        print(self.text)
        text = ""
        ind = 0
        while ind < len(self.text):
            ind += 2000
            cur = self.text[ind - 2000:ind]
            payload = json.dumps({
                "text": cur,
                "baseUrl": "https://internet.garant.ru"
            })
            response = requests.request("POST", url, headers=headers, data=payload)
            # print(response.text)
            html = response.json()["text"]
            text += html

        if len(self.text) % 2000 != 0:
            cur = self.text[ind:]
            payload = json.dumps({
                "text": cur,
                "baseUrl": "https://internet.garant.ru"
            })
            response = requests.request("POST", url, headers=headers, data=payload)
            # print(response.text)
            html = response.json()["text"]
            text += html

        html = text
        htmls = re.split("<a href=\"|</a>", html)
        # print(html)

        for i in range(1, len(htmls), 2):
            htmlc = htmls[i]
            htmlc = re.split('"', htmlc)
            link = htmlc[0]
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
            cur_context = cur_context.replace("</p>", "")
            htmlc = str(htmlc[0])
            htmlc = htmlc.split('document/')
            htmlc = htmlc[1]
            htmlc = htmlc.split('/')
            number = htmlc[0]

            url = "https://api.garant.ru/v1/find-modified"

            payload = json.dumps({"topics": [number], "modDate": self.date})
            headers = {
                'Authorization': 'Bearer f4e1a77c651811eab20b0050568d72f0',
                'Content-type': 'application/json',
                'Accept': 'application/json'
            }

            response = requests.post(url, headers=headers, data=payload).json()["topics"]

            if len(response) == 0:
                is_active_then = True
            else:
                is_active_then = False
            print(number)
            url1 = f'https://api.garant.ru/v1/topic/{number}'
            headers1 = {
                'Accept': 'application/json',
                'Content-type': 'application/json',
                'Authorization': 'Bearer f4e1a77c651811eab20b0050568d72f0',
            }

            response1 = requests.get(url1, headers=headers1).json()
            # print(response1)
            namme = response1['name']
            is_active_now = response1['status']
            if is_active_now == "Действующие":
                is_active_now = True
            else:
                is_active_now = False

            a = Document(str(i // 2 + 1), number, link, namme, is_active_then, is_active_now, cur_context, self.date)
            requestslist.append(a)

        return requestslist

    def create_table(self):
        data = self.make_doc_list()
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
        html = template.render(docs=data, given_date=self.date)
        # print(html)
        with open("output/template.html", "w", encoding='utf-8') as f:
            f.write(html)
        f.close()


obj = checkDocsRelevance("test.pdf", "2021-10-25")
obj.create_table()
