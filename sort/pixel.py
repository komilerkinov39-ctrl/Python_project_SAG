import pandas as pd
from pathlib import Path
from datetime import datetime # Нужен для создания настоящих дат


FILE = Path(r"C:\Users\M313\Desktop\Python_project_SAG\Sop for Oktober\Пиксели\Пиксели_с_01_01_2024_по_01_01_2025.xlsx")
OUT = Path(r"C:\Users\M313\Desktop\Python_project_SAG\pikseli_clean.csv")

RU_MONTHS = {
    "янв": 1, "фев": 2, "мар": 3, "апр": 4,
    "май": 5, "июн": 6, "июл": 7, "авг": 8,
    "сен": 9, "окт": 10, "ноя": 11, "дек": 12
}


def parse_date(value):
    month, year = value.split(".")
    return datetime(2000 + int(year), RU_MONTHS[month], 1)


def prepare_antp():
    raw = pd.read_excel(FILE, sheet_name="Факт_пикс_antp", header=None)

    dates = [parse_date(x) for x in raw.iloc[0, 1:22]]

    df = raw.iloc[1:36, :22].copy()
    df.columns = ["stanok"] + dates

    df = df.melt(
        id_vars="stanok",
        var_name="data",
        value_name="pikseli"
    )

    df["zavod"] = "ANTP"

    return df[["data", "zavod", "stanok", "pikseli"]]


def prepare_xiva_block(raw, first_row, last_row, year):
    df = raw.iloc[first_row:last_row + 1, :13].copy()
    df.columns = ["stanok"] + list(range(1, 13))

    df = df.melt(
        id_vars="stanok",
        var_name="month",
        value_name="pikseli"
    )

    df["data"] = df["month"].apply(
        lambda month: datetime(year, int(month), 1)
    )

    df["zavod"] = "XIVA"
    df["pikseli"] = pd.to_numeric(df["pikseli"], errors="coerce")

    return df.dropna(subset=["pikseli"])[
        ["data", "zavod", "stanok", "pikseli"]
    ]


def prepare_xiva():
    raw = pd.read_excel(FILE, sheet_name="Факт_пикс_xiva", header=None)

    xiva_2024 = prepare_xiva_block(raw, 4, 22, 2024)
    xiva_2025 = prepare_xiva_block(raw, 28, 50, 2025)

    xiva = pd.concat([xiva_2024, xiva_2025], ignore_index=True)

    return xiva

antp = prepare_antp()
xiva = prepare_xiva()

result = pd.concat([antp, xiva], ignore_index=True)
result = result.sort_values(["data", "zavod", "stanok"])
result["pikseli"] = result["pikseli"].astype(int)

print(f"ANTP: {len(antp)} строк, {antp['stanok'].nunique()} станков")
print(f"XIVA: {len(xiva)} строк, {xiva['stanok'].nunique()} станков")
print(f"Период: {result['data'].min().date()} — {result['data'].max().date()}")
print(f"Итого: {len(result)} строк")

jan = (
    result[
        result["data"].isin([
            datetime(2024, 1, 1),
            datetime(2025, 1, 1)
        ])
    ]
    .groupby(["data", "zavod"])["pikseli"]
    .sum()
)

print("\nПроверка сумм за январь:")
print(jan.to_string())

# print("\nЭталоны:")
print("2024-01 — ANTP: 96 218 023 | XIVA: 51 375 475")
print("2025-01 — ANTP: 100 777 404 | XIVA: 47 586 647")

result.to_csv(OUT, index=False, encoding="utf-8-sig")
print(f"\nСохранено: {OUT}")