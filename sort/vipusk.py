import pandas as pd
from pathlib import Path

FILE = Path(r"C:\Users\M313\Desktop\Python_project_SAG\Sop for Oktober\Выпуск\Выпуск_XIVA_10_25.XLSX")
OUT = Path(r"C:\Users\M313\Desktop\Python_project_SAG\фильтрованные\vypusk_xiva_10_25_clean.csv")

df = pd.read_excel(
    FILE,
    sheet_name="Sheet1",
    skiprows=[0],
    keep_default_na=False,
    na_values=[""]
)

print(f"Прочитано: {df.shape[0]} строк, {df.shape[1]} столбцов")

total = df["Количество"].sum()
print(f"Сумма 'Количество': {total:,.2f}")
print(f"Завод: {df['Завод'].unique()}")

df.to_csv(OUT, index=False, encoding="utf-8-sig")

print(f"Сохранено: {OUT}")
