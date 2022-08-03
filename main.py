# import difflib as df
import requests
import json
import datetime as dt
import re
import difflib as df


# from striprtf.striprtf import rtf_to_text
#
#
# with open("2/input/Оригинал.rtf", "r") as f:
#     text1 = f.read()
# f.close()
#
# text1 = rtf_to_text(text1, errors='igonre').replace("\xa0", " ").split("\n")
#
# with open("2/input/Новый документ.rtf", "rb") as f:
#     text2 = f.read().decode(encoding='utf-8')
#     # print(text2)
# f.close()
# # print(text2)
# text2 = rtf_to_text(text2, errors='igonre').replace("\xa0", " ").split("\n")
# # print("\n".join(text2))
#
# text1 = list(map(str, [1, 2, 3, 5]))
# text2 = list(map(str, [12, 2, 6, 3, 4, 5]))
# diff = df.unified_diff(text1, text2, n=0)
# diff = list(diff)[2:]
# differences = []
# cur= []
#
# for i in diff:
#     if i[0] != "@":
#         cur.append(i)
#     else:
#         if cur:
#             differences.append(cur)
#             cur = []
# if cur:
#     differences.append(cur)
#
# print(*differences, sep="\n")


# -------------------------------------------------------------------------------------
# changes = self.changing_text.split("\n\n")[-2]
#         while "\xa0" in changes:
#             changes = changes.replace("\xa0", " ")
#         changes = changes.split("\n")[1:]
#         need = []
#         ind = 0
#         while ". Настоящее постановление вступает в силу" not in changes[ind]:
#             need.append(changes[ind])
#             ind += 1
#         changes = need.copy()
#         ready = []
#         cur = changes[0]
#         if len(changes) > 1:
#             for i in changes[1:]:
#                 if (i.split()[0][:-1].isnumeric() and i.split()[0][-1] == ".") or \
#                         (len(i.split()[0].split(".")) == 2 and i.split()[0].split(".")[0].isnumeric()
#                          and i.split()[0].split(".")[1].isnumeric()):
#                     ready.append(cur)
#                     cur = i
#                 else:
#                     cur += " " + i
#             ready.append(cur)
#
#         for change in changes:
#             if "изложить в редакции: " in change:
#                 text_to_paste = change[change.index("изложить в редакции: ") + 22:-2]
#                 place = change.split(" ")[1:]
#                 for i in range(0, len(place), 2):
#                     pass
#


# url = "https://api.garant.ru/v1/find-modified"
#
# payload = json.dumps({"topics": ["70353464"], "modDate": "2021-11-25"})
# headers = {
#     'Authorization': 'Bearer f4e1a77c651811eab20b0050568d72f0',
#     'Content-type': 'application/json',
#     'Accept': 'application/json'
# }
#
# response = requests.post(url, headers=headers, data=payload).json()["topics"]
#
# if len(response) == 0:
#     is_active_then = True
# else:
#     is_active_then = False
#
# requestslist = []
# url = "https://api.garant.ru/v1/find-hyperlinks"
#
# payload = json.dumps({
#     "text": text,
#     "baseUrl": "https://internet.garant.ru"
# })
# headers = {
#     'Accept': 'application/json',
#     'Content-type': 'application/json',
#     'Authorization': 'Bearer f4e1a77c651811eab20b0050568d72f0'
# }
#
# response = requests.request("POST", url, headers=headers, data=payload)
# a = response.json()["text"]
#
# a = re.split("<a href=\"|</a>", a)
# for i in range(1, len(a), 2):
#     a = a[i]
#     a = re.split('"', a)
#     link = a[0]
#     a = str(a[0])
#     a = a.split('document/')
#     a = a[1]
#     a = a.split('/')
#     number = a[0]
#
#     a = [link, number]
#     requestslist.append(a)
#
# #
# # print(Request(""))
#
# url1 = 'https://api.garant.ru/v1/topic/72957500'
# headers1 = {
#     'Accept': 'application/json',
#     'Content-type': 'application/json',
#     'Authorization': 'Bearer f4e1a77c651811eab20b0050568d72f0',
# }
#
# response1 = requests.get(url1, headers=headers1).json()
# namme = response1['name']
# statuss = response1['status']
#
# print(namme, statuss)

old = ["Настоящее положение о муниципальной пожарной охране (далее - Положение) разработано в соответствии с Федеральным законом от 06 октября 2003 г. N 131-ФЗ \"Об общих принципах организации местного самоуправления в Российской Федерации\", статьей 1.2. Федеральным законом от 21 декабря 1994 г. N 69-ФЗ \"О пожарной безопасности\" и определяет цели, задачи, порядок создания, организацию деятельности, финансовое и материально- техническое обеспечение муниципальной пожарной охраны, порядок ее взаимодействия с другими видами пожарной охраны."]
new = ["Пастоящее xxx положение о муниципальной пожарной охране (далее - Положение) разработано в соответствии с Федеральным законом от 06 октября 2003 г. N 131-ФЗ \"Об общих принципах организации местного самоуправления в Российской Федерации\", статьей 11.1 Федеральным законом от 21 декабря 1994 г. N 69-ФЗ \"О пожарной безопасности\" и определяет цели, задачи, порядок создания, организацию деятельности, финансовое и материально- техническое обеспечение муниципальной пожарной охраны, порядок ее взаимодействия с другими видами пожарной охраны."]
diff = list(df.Differ().compare(old, new))
print(*diff, sep="\n")
ready = []
changingIndexes = []
if len(diff) > 2:
    diff1 = diff[1].replace("\n", "")[2:]
    diff2 = diff[3].replace("\n", "")[2:]
    new1 = new[0]
    old1 = old[0]
    old = old[0].split()
    new = new[0].split()
    ind = 0
    curInd = 0
    for i in old:
        if diff1[ind:len(i)] == "-" * len(i):
            if ind >= 30:
                ready.append(f"Исключить слово \"{i}\" после слов \"...{old1[ind - 30:ind]}...\"")
            elif len(old1) - 30 >= ind + len(i):
                ready.append(f"Исключить слово \"{i}\" перед словами\"...{old1[ind + len(i) + 1:ind + len(i) + 30]}...\"")
            else:
                ready.append(f"Исключить слово \"{i}\" из предложения \"...{old1}...\"")
        elif diff1[ind:ind + len(i)] != " " * len(i) and diff1[ind:ind + len(i)] != "":
            print(i, diff1[ind:ind + len(i)])
            if ind >= 30:
                ready.append(f"Изменить слово \"{i}\" после слов \"...{old1[ind - 30:ind]}...\" на \"")
            elif len(old1) - 30 >= ind + len(i):
                ready.append(f"Изменить слово \"{i}\" перед словами \"...{old1[ind + len(i) + 1:ind + len(i) + 30]}...\" на \"")
            else:
                ready.append(f"Изменить слово \"{i}\" из предложения \"{old1}\" на \"")

            changingIndexes.append(len(ready) - 1)
        ind += len(i) + 1
        if ind >= len(diff1):
            break

    ind = 0
    for i in new:
        if diff2[ind:ind + len(i)] == "+" * len(i):
            if ind >= 30:
                ready.append(f"Добавить слово \"{i}\" после слов \"...{new1[ind - 30:ind ]}...\"")
            elif len(new1) - 30 >= ind + len(i):
                ready.append(f"Добавить слово \"{i}\" перед словами\"...{new1[ind + len(i):ind + len(i) + 30]}...\"")
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

print(ready)
