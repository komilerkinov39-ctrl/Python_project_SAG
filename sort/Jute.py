import pandas as pd
from pathlib import Path

FILE = Path(r"C:\Users\M313\Desktop\Python_project_SAG\Sop for Oktober\Джут\JUTE.XLSX")
OUT = Path(r"C:\Users\M313\Desktop\Python_project_SAG\Cleaned\Jute\jute_clean.csv")

TIPY_NITI = ["J8/1LBS", "J10/1LBS", "J12/2LBS", "J13/2LBS", "J16/1LBS"]


def read_sheet(sheet, zavod):

    # читаем нужный лист и оставляем первые 6 столбцов
    df = pd.read_excel(FILE, sheet_name=sheet).iloc[:, :6]

    # переименовываем столбцы
    df.columns = ["data"] + TIPY_NITI

    # преобразуем дату в формат datetime
    df["data"] = pd.to_datetime(df["data"])

    # преобразуем таблицу из широкого формата в длинный
    df = df.melt(
        id_vars="data",
        var_name="tip_niti",
        value_name="raskhod_kg"
    )

    # добавляем название завода
    df["zavod"] = zavod

    return df[["data", "zavod", "tip_niti", "raskhod_kg"]]


antp = read_sheet("ANTP", "ANTP")
xiva = read_sheet("XIVA", "XIVA")

# объединяем таблицы и создаём новые индексы
result = pd.concat([antp, xiva], ignore_index=True)

# сортируем по дате, заводу и типу нити
result = result.sort_values(["data", "zavod", "tip_niti"])


print("\nПервые 10 строк:")
print(result.head(10).to_string(index=False))


check = (
    result[result["data"] == "2025-10-01"]
    .groupby("zavod")["raskhod_kg"]
    .sum()
)

print("\nПроверка за октябрь 2025:")
print(check.to_string())


result.to_csv(OUT, index=False, encoding="utf-8-sig")
print(f"\nСохранено: {OUT}")