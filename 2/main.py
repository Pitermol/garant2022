import time

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from striprtf.striprtf import rtf_to_text
import difflib as df
from docx import Document
from docx.shared import Pt, RGBColor
import docx
import jinja2
from dataclasses import dataclass
import sys
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.opc.constants import RELATIONSHIP_TYPE
from docx.oxml.shared import OxmlElement


class docGeneration:
    def __init__(self, name_orig, name_ready):
        self.orig_text = ""
        self.ready_text = ""
        self.name_old = ""
        self.name_changing = ""
        self.name_new = ""
        self.type = ""
        self.name_changing = ""
        self.new_date = ""
        self.filename_orig = name_orig
        self.filename_ready = name_ready

    def set_orig_text(self):
        with open(f"input/{self.filename_orig}", "r") as f:
            text = f.read()
        f.close()
        self.name_old = text.split("\n")[24].split("{\\cs24\\b0\\cf18 ")[1].split("}}}")[0]
        if "постановление" in self.name_old.lower():  # Всегда ли тип документа это первые слова?
            self.type = "Постановление"
        elif "закон" in self.name_old.lower():
            self.type = "Закон"
        elif "указ" in self.name_old:
            self.type = "Указ"
        else:
            self.type = "Неизвестный тип"

        self.orig_text = rtf_to_text(text, errors='ignore').replace("\xa0", " ").split("\n")

    def set_ready_text(self):
        with open(f"input/{self.filename_ready}", "r") as f:
            text = f.read()
        f.close()

        self.name_new = text.split("\n")[24].split("{\\cs24\\b0\\cf18 ")[1].split("}}}")[0]
        self.name_changing = f"{self.name_new.split(' от ')[0]} от {self.new_date} "
        self.new_date = text.split(" от ")[1].split(" г. ")[0] + " г."
        self.ready_text = rtf_to_text(text, errors='ignore').replace("\xa0", " ").split("\n")

    def get_orig_text(self):
        return self.orig_text

    def get_changing_text(self):
        return self.ready_text

    def main(self):
        self.set_ready_text()
        self.set_orig_text()
        # print("\n".join(self.orig_text))
        diff = df.unified_diff(self.orig_text, self.ready_text, n=0)
        diff = list(diff)[2:]
        differences = []
        cur = []

        for i in diff:
            if i[0] != "@":
                cur.append(i)
            else:
                if cur:
                    differences.append(cur)
                    cur = []
        if cur:
            differences.append(cur)
        # print(differences)

        for difference in differences:
            place = []
            if len(difference) == 1:
                difference = difference[0]
                if difference[0] == "-":
                    difference = difference[1:]
                    if difference.startswith("Статья") or difference.startswith("Пункт") or \
                            difference.startswith("Глава") or difference.startswith("Раздел") \
                            or difference.startswith("Часть"):
                        place.append(difference.split()[:2])
                    else:
                        if "." in difference:
                            if difference.split(".")[0].isnumeric():
                                if difference.split(".")[1].isnumeric():
                                    place.append(
                                        "Подпункт " + difference.split(".")[0] + "." + difference.split(".")[1] + ".")
                                else:
                                    place.append(
                                        "Пункт " + difference.split(".")[0] + ".")
                        elif ")" in difference:
                            if difference.split(")")[0].isnumeric():
                                place.append("Подпункт " + difference.split(")")[0])
                    ind = self.orig_text.index(difference)
                    while ind != 1 and not (
                            self.orig_text[ind] == self.orig_text[ind - 2] == "\n" and self.orig_text[ind - 1] != "\n"):
                        ind -= 1
                    if ind != 1:
                        if "." in self.orig_text[ind].split()[0] and self.orig_text[ind].split(".")[0].isnumeric():
                            place.append("Раздел " + self.orig_text[ind].split(".")[0] + " ")
                    place = place[::-1]
                    doc_name = self.doc_name
                    with open("parts/start.txt", "r", encoding="utf-8") as f:
                        ready = f.read()
                    f.close()

                else:
                    pass

    def create_docx(self, name_changing="", name_new="", name_old="", link_changing="", type="", new_date="", changes=None):
        if changes is None:
            changes = []
        with open("double.html", "r", encoding="utf-8") as f:
            html = f.read()
        f.close()
        html = html.replace("@@@name_new@@@", name_new)
        html = html.replace("@@@name_old@@@", name_old)
        html = html.replace("@@@link_changing@@@", link_changing)
        html = html.replace("@@@type@@@", type)
        html = html.replace("@@@new_date@@@", new_date)
        html = html.replace("@@@link_changing@@@", "http://municipal.garant.ru/document/redirect/198237358/0")

        body = []
        if type.lower() == "постановление":
            html = html.replace("@@@ability_doc_if_needed@@@", "В соответствии с @@@connected_doc@@@ @@@authority@@@")
            html = html.replace("@@@start_word_if_needed@@@", "ПОСТАНОВЛЯЕТ")
            body.append(
                f"<p lang='ru-RU' class='western' style='line-height: 100%; text-indent: 0.39in; margin-bottom: 0in'>\n1. Внести в {name_old} следующие изменения: \n</p>\n")
            for i, change in enumerate(changes, 1):
                body.append(
                    f"<p lang='ru-RU' class='western' style='line-height: 100%; text-indent: 0.39in; margin-bottom: 0in'>\n1.{str(i)}. {change}\n</p>\n")
            body.append(
                "<p lang='ru-RU' class='western' style='line-height: 100%; text-indent: 0.39in; margin-bottom: 0in'>\n2. Настоящее постановление вступает в силу со дня подписания. \n</p>\n")
        elif type.lower() == "закон":
            for i, change in enumerate(changes, 1):
                body.append(
                    f"<p lang='ru-RU' class='western' style='font-weight: bold; line-height: 100%; text-indent: "
                    f"0.39in; margin-bottom: 0in'>Статья {str(i)}</p>\n")
                for j, cur_change in enumerate(change):
                    body.append(f"<p lang='ru-RU' class='western' style='line-height: 100%; text-indent: "
                                f"0.39in; margin-bottom: 0in'>Статья {str(i)}.{str(j)} {change}</p>\n")

        html = "".join(body)
        with open("test1.html", "w", encoding="utf-8") as f:
            f.write(html)
        f.close()


def html2pdf():
    app = QtWidgets.QApplication(sys.argv)
    loader = QtWebEngineWidgets.QWebEnginePage()
    loader.setZoomFactor(1)

    def handle_print_finished(filename, status):
        print("finished", filename, status)
        QtWidgets.QApplication.quit()

    def handle_load_finished(status):
        if status:
            loader.printToPdf("test.pdf")
        else:
            print("Failed")
            QtWidgets.QApplication.quit()

    loader.pdfPrintingFinished.connect(handle_print_finished)
    loader.loadFinished.connect(handle_load_finished)
    loader.load(QtCore.QUrl.fromLocalFile("C:\\Users\\admin\\PycharmProjects\\garant2022\\2\\test1.html"))

    app.exec()
    return


with open("input/Оригинал.rtf", "r", encoding="cp1251") as f:
    text = f.read()
f.close()
print(text.split("\n")[24].split("{\\cs24\\b0\\cf18 ")[1].split("}}}")[0])

# obj = docGeneration("Оригинал.rtf", "Новый документ.rtf")
# obj.main()
