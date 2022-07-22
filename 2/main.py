import time

from striprtf.striprtf import rtf_to_text
import difflib as df
import docx
import jinja2
from dataclasses import dataclass
import sys
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets


class docGeneration:
    def __init__(self, name_orig, name_ready):
        self.origText = ""
        self.readyText = ""
        self.nameOld = ""
        self.name_changing = ""
        self.name_new = ""
        self.type = ""
        self.name_changing = ""
        self.new_date = ""
        self.filenameOrig = name_orig
        self.filenameReady = name_ready

    def set_origText(self):
        with open(f"input/{self.filenameOrig}", "r") as f:
            text = f.read()
        f.close()
        self.nameOld = text.split("\n")[24].split("{\\cs24\\b0\\cf18 ")[1].split("}}}")[0]
        if "постановление" in self.nameOld.lower():  # Всегда ли тип документа это первые слова?
            self.type = "Постановление"
        elif "закон" in self.nameOld.lower():
            self.type = "Закон"
        elif "указ" in self.nameOld:
            self.type = "Указ"
        else:
            self.type = "Неизвестный тип"

        self.origText = rtf_to_text(text, errors='ignore').replace("\xa0", " ").split("\n")

    def set_readyText(self):
        with open(f"input/{self.filenameReady}", "r") as f:
            text = f.read()
        f.close()

        self.name_new = text.split("\n")[24].split("{\\cs24\\b0\\cf18 ")[1].split("}}}")[0]
        self.name_changing = f"{self.name_new.split(' от ')[0]} от {self.new_date} "
        self.new_date = text.split(" от ")[1].split(" г. ")[0] + " г."
        self.readyText = rtf_to_text(text, errors='ignore').replace("\xa0", " ").split("\n")

    def get_origText(self):
        return self.origText

    def get_changing_text(self):
        return self.readyText

    def main(self):
        self.set_readyText()
        self.set_origText()
        # print("\n".join(self.origText))
        diff = df.Differ().compare(self.origText, self.readyText)
        diff = list(filter(lambda x: x[0] != "?", diff))
        differences = []
        cur = []
        changes = []

        for i in diff:
            if len(cur) == 0:
                cur.append(i)
            elif len(cur) == 1:
                if cur[0][0] != i[0]:
                    cur.append(i)
                    differences.append(cur)
                    cur = []
                else:
                    differences.append(cur)
                    cur = [i]
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
                    ind = self.origText.index(difference)
                    while ind != 1 and not (
                            self.origText[ind] == self.origText[ind - 2] == "\n" and self.origText[ind - 1] != "\n"):
                        ind -= 1
                    if ind != 1:
                        if "." in self.origText[ind].split()[0] and self.origText[ind].split(".")[0].isnumeric():
                            place.append("Раздел " + self.origText[ind].split(".")[0] + " ")
                    place = "".join(place[::-1])

                    change = f"{place} {self.nameOld} убрать {difference}"
                    changes.append(change)

                elif difference[0] == "+":
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
                    ind = self.origText.index(difference)
                    while ind != 1 and not (
                            self.origText[ind] == self.origText[ind - 2] == "\n" and self.origText[ind - 1] != "\n"):
                        ind -= 1
                    if ind != 1:
                        if "." in self.origText[ind].split()[0] and self.origText[ind].split(".")[0].isnumeric():
                            place.append("Раздел " + self.origText[ind].split(".")[0] + " ")
                    place = "".join(place[::-1])

                    change = f"{place} {self.nameOld} дополнить {difference}"
                    changes.append(change)
            else:
                old = difference[0][1:]
                new = difference[1][1:]
                if old.startswith("Статья") or old.startswith("Пункт") or \
                        old.startswith("Глава") or old.startswith("Раздел") \
                        or old.startswith("Часть"):
                    place.append(old.split()[:2])
                else:
                    if "." in old:
                        if old.split(".")[0].isnumeric():
                            if old.split(".")[1].isnumeric():
                                place.append(
                                    "Подпункт " + old.split(".")[0] + "." + old.split(".")[1] + ".")
                            else:
                                place.append(
                                    "Пункт " + old.split(".")[0] + ".")
                    elif ")" in old:
                        if old.split(")")[0].isnumeric():
                            place.append("Подпункт " + old.split(")")[0])
                ind = self.origText.index(old)
                while ind != 1 and not (
                        self.origText[ind] == self.origText[ind - 2] == "\n" and self.origText[ind - 1] != "\n"):
                    ind -= 1
                if ind != 1:
                    if "." in self.origText[ind].split()[0] and self.origText[ind].split(".")[0].isnumeric():
                        place.append("Раздел " + self.origText[ind].split(".")[0] + " ")
                place = "".join(place[::-1])
                # if
                change = f"{place} {self.nameOld} убрать {old}"
                changes.append(change)

    def create_docx(self, name_changing="", name_new="", nameOld="", link_changing="", type="", new_date="",
                    changes=None):
        if changes is None:
            changes = []
        with open("double.html", "r", encoding="utf-8") as f:
            html = f.read()
        f.close()
        html = html.replace("@@@name_new@@@", name_new)
        html = html.replace("@@@nameOld@@@", nameOld)
        html = html.replace("@@@link_changing@@@", link_changing)
        html = html.replace("@@@type@@@", type)
        html = html.replace("@@@new_date@@@", new_date)
        html = html.replace("@@@link_changing@@@", "http://municipal.garant.ru/document/redirect/198237358/0")

        body = []
        if type.lower() == "постановление":
            html = html.replace("@@@ability_doc_if_needed@@@", "В соответствии с @@@connected_doc@@@ @@@authority@@@")
            html = html.replace("@@@start_word_if_needed@@@", "ПОСТАНОВЛЯЕТ")
            body.append(
                f"<p lang='ru-RU' class='western' style='line-height: 100%; text-indent: 0.39in; margin-bottom: 0in'>\n1. Внести в {nameOld} следующие изменения: \n</p>\n")
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

        html += "".join(body)
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


# obj = docGeneration("Оригинал.rtf", "Новый документ.rtf")
# obj.main()

a = ["abcdef", "ghijkl", "456"]
b = ["acdf", "ghijklop", "123"]
diff = df.Differ().compare(a, b)
print(list(diff))
