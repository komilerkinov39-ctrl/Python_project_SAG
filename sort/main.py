import pandas as pd
from pathlib import Path

src = Path(r"C:\Users\M313\Desktop\Python_project_SAG\Sop for Oktober\Константы.XLSX")
out = Path(r"C:\Users\M313\Desktop\Python_project_SAG\Cleaned\konstanta.csv")

df = pd.read_excel(src, sheet_name="ТКАЦКИЙ", keep_default_na=False, na_values=[""])

df = df[["Качество", "Quality Name", "Плотность по утку", "Плетение", "Бердо"]]
df.columns = ["kachestvo", "kollection", "plotnost_po_utku", "pletenie", "berdo"]

df = df.dropna(subset=["kachestvo"])
df["plotnost_po_utku"] = df["plotnost_po_utku"].astype("Int64")
df["berdo"] = df["berdo"].astype("Int64")

print("Размер:", df.shape)
print("Есть ли NA:", "NA" in df["kachestvo"].values)
print(df[df["kachestvo"] == "NA"])

df.to_csv(out, index=False, encoding="utf-8-sig")