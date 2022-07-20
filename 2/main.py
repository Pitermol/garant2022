from striprtf.striprtf import rtf_to_text
import difflib as df
import docx


class docGeneration:
    def __init__(self, name_orig, name_ready):
        self.orig_text = ""
        self.ready_text = ""
        self.doc_name = ""
        self.name_orig = name_orig
        self.name_ready = name_ready

    def set_orig_text(self):
        with open(f"input/{self.name_orig}", "r") as f:
            text = f.read()
        f.close()
        self.doc_name = text.split("\n")[24]

        self.orig_text = rtf_to_text(text, errors='ignore').replace("\xa0", " ").split("\n")

    def set_ready_text(self):
        with open(f"input/{self.name_ready}", "r") as f:
            text = f.read()
        f.close()

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
                    while ind != 1 and not (self.orig_text[ind] == self.orig_text[ind - 2] == "\n" and self.orig_text[ind - 1] != "\n"):
                        ind -= 1
                    if ind != 1:
                        if "." in self.orig_text[ind].split()[0] and self.orig_text[ind].split(".")[0].isnumeric():
                            place.append("Раздел " + self.orig_text[ind].split(".")[0] + " ")
                    place = place[::-1]
                    doc_name = self.doc_name

                else:
                    pass


# obj = docGeneration("Оригинал.rtf", "Новый документ.rtf")
# obj.main()

# with open("../1/input/file.docx", "r", encoding='utf-8') as f:
#     text = f.read()
# f.close()
# text = rtf_to_text(text)
# print(text)

text = ""
file = docx.Document("../1/input/file.docx")
for para in file.paragraphs:
    text += para.text + "\n\t"


with open("out.txt", "w", encoding='utf-8') as f:
    f.write(text)
f.close()
