import pandas as pd
from pathlib import Path

FILE = Path(
    r"C:\Users\M313\Desktop\Python_project_SAG\Sop for Oktober\Остатка\остатка_10_25.xlsx"
)
OUT = Path(
    r"C:\Users\M313\Desktop\Python_project_SAG\Cleaned\Остатки\ostatka_10_25_clean.csv"
)


df = pd.read_excel(
    FILE,
    sheet_name="Sheet1",
    skiprows=[0],
    keep_default_na=False,
    na_values=[""]
)


print(f"Прочитано: {df.shape[0]} строк, {df.shape[1]} столбцов")


# Убираем лишние пробелы из названий столбцов
df.columns = [str(c).strip() for c in df.columns]

# Переименовываем два одинаковых столбца "Склад"
sklad_indexes = [
    i for i, column in enumerate(df.columns)
    if column == "Склад"
]

if len(sklad_indexes) == 2:
    columns = df.columns.tolist()

    columns[sklad_indexes[0]] = "Склад_код"
    columns[sklad_indexes[1]] = "Склад_название"

    df.columns = columns


# Удаляем ненужный столбец
df = df.drop(columns=["Номенклатура, Артикул"])


# Проверка итоговой суммы
total = pd.to_numeric(
    df["Конечный остаток м2"],
    errors="coerce"
).sum()

print(
    f"Конечный остаток м2: {total:,.5f}"
)


# Сохраняем подготовленные данные
df.to_csv(
    OUT,
    index=False,
    encoding="utf-8-sig"
)

print(f"Сохранено: {OUT}")