import pandas as pd
from pathlib import Path

src = Path(r"C:\Users\M313\Desktop\Python_project_SAG\Sop for Oktober\Выпуск_10_2025.xlsx")
out = Path(r"C:\Users\M313\Desktop\Python_project_SAG\Cleaned\vypusk_po_godam.csv")

MONTHS = ["Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]

raw = pd.read_excel(src, sheet_name="Лист1", header=None)

antp = raw.iloc[19:28, 1:14]
xiva = raw.iloc[36:38, 1:14]
antp.columns = ["Бердо"] + MONTHS
xiva.columns = antp.columns

antp["Завод"] = "ANTP"
xiva["Завод"] = "XIVA"

df = pd.concat([antp, xiva])
df = df.melt(id_vars=["Завод","Бердо"], var_name="Месяц", value_name="м2")
df = df[df["м2"] != 0]
df["Год"] = 2025

# что бы не хранил старое значение DataFrame, например что бы не было 1, 2, 4, 7....
df = df.reset_index(drop=True)

print("Размер:", df.shape)
# print("\nПроверка сумм за октябрь:")
print("Проверка сумм за октябрь:\n", df[df["Месяц"]=="Октябрь"].groupby("Завод")["м2"].sum())
print(df.head(5))

df.to_csv(out, index=False, encoding="utf-8-sig")

