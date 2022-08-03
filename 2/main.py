import configparser
import time

from striprtf.striprtf import rtf_to_text
import difflib as df
import docx
import jinja2
import unicodedata
from dataclasses import dataclass
import sys
import requests
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets


class docGeneration:
    def __init__(self, name_orig, name_ready):
        self.origText = ""
        self.readyText = ""
        self.nameOld = ""
        self.name_changing = ""
        self.name_new = ""
        self.type = ""
        config = configparser.ConfigParser()
        config.read('settings.ini')
        self.APIToken = config["api"]["token"]
        self.apiUrlMakeLinks = config["api"]["url_make_links"]
        self.apiAccept = config["api"]["accept"]
        self.apiContentType = config["api"]["content-type"]
        self.new_date = ""
        self.filenameOrig = name_orig
        self.filenameReady = name_ready

    def set_origText(self):
        with open(f"input/{self.filenameOrig}", "r") as f:
            text = f.read()
        f.close()
        link = list(filter(lambda x: "HYPERLINK \"" in x, text.split("\n")))[0].split("\"")[1]
        topic = link.split("redirect/")[1].split("/0")[0]

        try:
            url = f"https://api.garant.ru/v1/topic/{topic}"
            headers = {
                'Authorization': f'Bearer {self.APIToken}',
                'Content-type': self.apiContentType,
                'Accept': self.apiAccept,
            }
            response = requests.get(url, headers=headers).json()
            self.nameOld = response["name"]
        except Exception as e:
            print(str(e) + ": Не удалось отправить запрос для получения информации по документу")
            self.nameOld = "Постановление от 27 января 2022 г. N 43 \"\""

        # self.nameOld = \
        # list(filter(lambda x: "fldinst {HYPERLINK" in x, text.split("\n")))[0].split("{\\cs24\\b0\\cf18 ")[1].split(
        #     "}}}")[0]
        if "постановление" in self.nameOld.lower():  # Всегда ли тип документа это первые слова?
            self.type = "Постановление"
        elif "закон" in self.nameOld.lower():
            self.type = "Закон"
        elif "указ" in self.nameOld:
            self.type = "Указ"
        else:
            self.type = "Неизвестный тип"

        self.origText = rtf_to_text(text, errors='ignore').replace("\xa0", " ").replace("  ", " ").split("\n")
        # print(rtf_to_text(text, errors='ignore'))

    def set_readyText(self):
        with open(f"input/{self.filenameReady}", "r", encoding="cp1251") as f:
            text = f.read()
        f.close()
        link = list(filter(lambda x: "HYPERLINK \"" in x, text.split("\n")))[1].split("\"")[1]
        topic = link.split("redirect/")[1].split("/")[0]

        try:
            url = f"https://api.garant.ru/v1/topic/{topic}"
            headers = {
                'Authorization': f'Bearer {self.APIToken}',
                'Content-type': self.apiContentType,
                'Accept': self.apiAccept,
            }
            response = requests.get(url, headers=headers).json()
            self.name_new = response["name"]
        except Exception as e:
            print(str(e) + ": Не удалось отправить запрос для получения информации по документу")
            self.name_new = "Постановление от 27 января 2022 г. N 43 \"\""

        # self.name_new = \
        # list(filter(lambda x: "fldinst {HYPERLINK" in x, text.split("\n")))[0].split("{\\cs24\\b0\\cf18 ")[1].split(
        #     "}}}")[0]
        self.name_changing = f"{self.name_new.split(' от ')[0]} об изменениях от {self.new_date} "
        self.new_date = self.name_new.split(" от ")[1].split(" г. ")[0] + " г."
        self.readyText = rtf_to_text(text, errors='ignore').replace("\xa0", " ").replace("  ", " ").split("\n")
        # print(self.readyText)
        # print(self.origText)
        while "" in self.readyText:
            self.readyText.remove("")
        while "" in self.origText:
            self.origText.remove("")
        while "\n" in self.readyText:
            self.readyText.remove("\n")
        while "\n" in self.origText:
            self.origText.remove("\n")
        while " " in self.readyText:
            self.readyText.remove(" ")
        while " " in self.origText:
            self.origText.remove(" ")
        while "С изменениями и дополнениями от:" in self.readyText:
            ind = self.readyText.index("С изменениями и дополнениями от:")
            del self.readyText[ind]
            del self.readyText[ind]
        while "Информация об изменениях:" in self.readyText:
            ind = self.readyText.index("Информация об изменениях:")
            del self.readyText[ind]
            del self.readyText[ind]
        while "ГАРАНТ:" in self.readyText:
            ind = self.readyText.index("ГАРАНТ:")
            del self.readyText[ind]
            del self.readyText[ind]
        while "ГАРАНТ:" in self.origText:
            ind = self.origText.index("ГАРАНТ:")
            del self.origText[ind]
            del self.origText[ind]
        # print(rtf_to_text(text, errors='ignore'))
        # for i in range(15):
        #     print(self.origText[i])
        #     print(self.readyText[i])
        #     print()

    def get_origText(self):
        return self.origText

    def get_changing_text(self):
        return self.readyText

    def create_docx(self, name_changing="", name_new="", nameOld="", link_changing="", type="", new_date="",
                    changes=None):
        if changes is None:
            changes = []
        with open("double.html", "r", encoding="utf-8") as f:
            html = f.read()
        f.close()
        # print(html)
        html = html.replace("@@@name_new@@@", name_new)
        html = html.replace("@@@name_old@@@", nameOld)
        html = html.replace("@@@link_changing@@@", link_changing)
        html = html.replace("@@@type@@@", type)
        html = html.replace("@@@new_date@@@", new_date)
        html = html.replace("@@@link_changing@@@", "http://municipal.garant.ru/document/redirect/198237358/0")

        body = []
        if type.lower() == "постановление":
            print(1)
            html = html.replace("@@@ability_doc_if_needed@@@", "В соответствии с @@@connected_doc@@@ @@@authority@@@")
            html = html.replace("@@@start_word_if_needed@@@", "ПОСТАНОВЛЯЕТ")
            body.append(
                f"\t\t<p lang='ru-RU' class='western' style='line-height: 100%; font-weight: bold; text-indent: 0.39in; margin-bottom: 0in'>\n\t\t\t1. Внести в {nameOld} следующие изменения: \n\t\t</p>\n")
            for i, change in enumerate(changes, 1):
                body.append(
                    f"\t\t<p lang='ru-RU' class='western' style='line-height: 100%; text-indent: 0.39in; margin-bottom: 0in'>\n\t\t\t1.{str(i)}. {change}\n\t\t</p>\n")
            body.append(
                f"\t\t<p lang='ru-RU' class='western' style='line-height: 100%; text-indent: 0.39in; margin-bottom: 0in'>\n\t\t\t2. Настоящее {self.type} вступает в силу со дня подписания. \n\t\t</p>\n")
        elif type.lower() == "закон":
            print(len(changes))
            for i, change in enumerate(changes, 1):
                body.append(
                    f"\t\t<p lang='ru-RU' class='western' style='font-weight: bold; line-height: 100%; text-indent: "
                    f"0.39in; margin-bottom: 0in'>\n\t\t\tСтатья {str(i)} {change}</p>\n")
                # for j, cur_change in enumerate(change):
                #     body.append(f"\t\t<p lang='ru-RU' class='western' style='line-height: 100%; text-indent: "
                #                 f"0.39in; margin-bottom: 0in'>Статья {str(i)}.{str(j)} {change}</p>\n")

        body = "".join(body)
        html = html.replace("@@@body@@@", body)
        # print(html)
        with open("output/template.html", "w", encoding="utf-8") as f:
            f.write(html)
        f.close()

        html2pdf()

    def main(self):
        self.set_origText()
        self.set_readyText()
        # print("\n".join(self.origText))
        # print(self.readyText)
        diff = df.Differ().compare(self.origText, self.readyText)
        # print(*list(diff), sep="\n")
        diff = list(filter(lambda x: x[0] != "?" and (x[0] == "-" or x[0] == "+"), diff))
        # print(*diff, sep="\n")
        differences = []
        cur = []
        changes = []
        # Почистить differences

        for i in diff:
            if i.split()[1:3] == "В соответствии".split():
                print(2)
                continue
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
        # print(*differences, sep="\n")

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
                old = difference[0][2:].strip()
                new = difference[1][2:].strip()
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
                while ind > 1 and not (
                        self.origText[ind] == self.origText[ind - 2] == "\n" and self.origText[ind - 1] != "\n"):
                    ind -= 1
                if ind != 1:
                    if "." in self.origText[ind].split()[0] and self.origText[ind].split(".")[0].isnumeric():
                        place.append("Раздел " + self.origText[ind].split(".")[0] + " ")
                place = "".join(place[::-1])
                old = [old]
                new = [new]
                diff = list(df.Differ().compare(old, new))
                print(*diff, sep="\n")
                ready = []
                changingIndexes = []
                changingIndexes1 = []
                if len(diff) > 2:
                    if len(diff) == 4:
                        diff1 = diff[1].replace("\n", "")[2:]
                        diff2 = diff[3].replace("\n", "")[2:]
                        new1 = new[0]
                        old1 = old[0]
                        old = old[0].split()
                        new = new[0].split()
                        ind = 0
                        curInd = 0
                        for j, i in enumerate(old):
                            if diff1[ind:len(i)] == "-" * len(i):
                                if ind >= 30:
                                    ready.append(f"Исключить слово \"{i}\" после слов \"...{old1[ind - 30:ind]}\"")
                                elif len(old1) - 30 >= ind + len(i):
                                    ready.append(
                                        f"Исключить слово \"{i}\" перед словами\"{old1[ind + len(i) + 1:ind + len(i) + 30]}...\"")
                                else:
                                    ready.append(f"Исключить слово \"{i}\" из предложения \"{old1}\"")
                            elif diff1[ind:ind + len(i)] != " " * len(i) and diff1[ind:ind + len(i)] != "":
                                if j - 1 in changingIndexes1:
                                    if "после слов" in ready[-1]:
                                        prev = ready[-1].split("\" после слов")[0].split("\"")[1]
                                    elif "перед словами" in ready[-1]:
                                        prev = ready[-1].split("\" перед словами")[0].split("\"")[1]
                                    else:
                                        prev = ready[-1].split("\" из предложения")[0].split("\"")[1]
                                    ready[-1] = ready[-1].replace(prev, prev + " " + i)
                                    # print("@", ready[-1])
                                    # changingIndexes.append(j)
                                    continue

                                print(i, diff1[ind:ind + len(i)])
                                if ind >= 30:
                                    ready.append(f"Изменить \"{i}\" после слов \"...{old1[ind - 30:ind]}\" на \"")
                                elif len(old1) - 30 >= ind + len(i):
                                    ready.append(
                                        f"Изменить \"{i}\" перед словами \"{old1[ind + len(i) + 1:ind + len(i) + 30]}...\" на \"")
                                else:
                                    ready.append(f"Изменить \"{i}\" из предложения \"{old1}\" на \"")

                                changingIndexes.append(len(ready) - 1)
                                changingIndexes1.append(j)
                            ind += len(i) + 1
                            if ind >= len(diff1):
                                break

                        ind = 0
                        for j, i in enumerate(new):
                            if diff2[ind:ind + len(i)] == "+" * len(i):
                                if ind >= 30:
                                    ready.append(f"Добавить слово \"{i}\" после слов \"...{new1[ind - 30:ind]}...\"")
                                elif len(new1) - 30 >= ind + len(i):
                                    ready.append(
                                        f"Добавить слово \"{i}\" перед словами\"...{new1[ind + len(i):ind + len(i) + 30]}...\"")
                                else:
                                    ready.append(f"Добавить слово \"{i}\" в предложение \"...{new1}...\"")
                            elif diff2[ind:ind + len(i)] != " " * len(i) and diff2[ind:ind + len(i)] != "":
                                try:
                                    if new[j - 1] in ready[changingIndexes[curInd - 1]].split("\" на")[-1]:
                                        curInd -= 1
                                        ready[changingIndexes[curInd]] = ready[changingIndexes[curInd]][:-1] + " " + i + "\""
                                        curInd += 1
                                        print(1, new[j - 1], ready[changingIndexes[curInd - 1]])
                                    else:
                                        print(2, i, diff2[ind:ind + len(i)])
                                        ready[changingIndexes[curInd]] += i + "\""
                                        curInd += 1
                                except Exception as e:
                                    print(e)
                            ind += len(i) + 1
                            if ind >= len(diff2):
                                break
                        print(ready)
                        for i in ready:
                            change = f"{place} {self.nameOld} {i}"
                            changes.append(change)

                    elif diff[1].startswith("?"):
                        diff1 = diff[1].replace("\n", "")[2:]
                        old1 = old[0]
                        old = old[0].split()
                        ind = 0
                        for i in old:
                            if diff1[ind:len(i)] == "-" * len(i):
                                if ind >= 30:
                                    ready.append(f"Исключить слово \"{i}\" после слов \"...{old1[ind - 30:ind]}...\"")
                                elif len(old1) - 30 >= ind + len(i):
                                    ready.append(
                                        f"Исключить слово \"{i}\" перед словами\"...{old1[ind + len(i) + 1:ind + len(i) + 30]}...\"")
                                else:
                                    ready.append(f"Исключить слово \"{i}\" из предложения \"...{old1}...\"")

                                changingIndexes.append(len(ready) - 1)
                            ind += len(i) + 1
                            if ind >= len(diff1):
                                break
                        for i in ready:
                            change = f"{place} {self.nameOld} {i}"
                            changes.append(change)
                    else:
                        diff2 = diff[3].replace("\n", "")[2:]
                        new1 = new[0]
                        new = new[0].split()
                        ind = 0
                        curInd = 0
                        for i in new:
                            if diff2[ind:ind + len(i)] == "+" * len(i):
                                if ind >= 30:
                                    ready.append(f"Добавить слово \"{i}\" после слов \"...{new1[ind - 30:ind]}...\"")
                                elif len(new1) - 30 >= ind + len(i):
                                    ready.append(
                                        f"Добавить слово \"{i}\" перед словами\"...{new1[ind + len(i):ind + len(i) + 30]}...\"")
                                else:
                                    ready.append(f"Добавить слово \"{i}\" в предложение \"...{new1}...\"")
                            elif diff2[ind:ind + len(i)] != " " * len(i) and diff2[ind:ind + len(i)] != "":
                                try:
                                    ready[changingIndexes[curInd]] += i + "\""
                                    curInd += 1
                                except Exception as e:
                                    print(e)
                            ind += len(i) + 1
                            if ind >= len(diff2):
                                break
                        for i in ready:
                            change = f"{place} {self.nameOld} {i}"
                            changes.append(change)

                else:
                    change = f"{place} {self.nameOld} изложить в редакции: <br>    \"{new}\""
                    changes.append(change)

        self.create_docx(name_new=self.name_new, nameOld=self.nameOld, link_changing="https://ya.ru", type=self.type,
                         new_date=self.new_date, changes=changes)


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
    loader.load(QtCore.QUrl.fromLocalFile("C:\\Users\\admin\\PycharmProjects\\garant2022\\2\\output\\template.html"))

    app.exec()
    return


obj = docGeneration("старая.rtf", "новая.rtf")
obj.main()
# Почистить differences
