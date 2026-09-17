import pandas as pd
from pathlib import Path

src = Path(r"C:\Users\M313\Desktop\Python_project_SAG\Sop for Oktober\продажа_с_2024.xlsx")
out = Path(r"C:\Users\M313\Desktop\Python_project_SAG\Cleaned\prodazha_clean.csv")

df = pd.read_excel(src, sheet_name="Sheet1")
df = df.drop(columns=["Период.1", "Номенклатура", "Магазин / Склад", "Документ, Магазин", "Коллекция"])

# проверка точности данных
print("Размер:", df.shape)
print("Колличество м2:", df["Количество м2"].sum())
print("Сумма:", df["Сумма"].sum())
print("Магазинов:", df["Магазин"].nunique())
print("Период:", df["Период"].min(), "по", df["Период"].max())

df.to_csv(out, index=False, encoding="utf-8-sig")


