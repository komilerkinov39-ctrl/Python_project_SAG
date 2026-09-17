import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:ПАРОЛЬ@localhost:5432/sag_project")

query = """
SELECT o.magazin, o.ostatok_m2, COALESCE(p.prodano_m2, 0) AS prodano_m2
FROM (
    SELECT sklad_nazvanie AS magazin, SUM(konechnyy_ostatok_m2) AS ostatok_m2
    FROM ostatka_10_25 GROUP BY sklad_nazvanie
) o
LEFT JOIN (
    SELECT magazin, SUM(kolichestvo_m2) AS prodano_m2
    FROM sales
    WHERE tip_dokumenta IN ('Продажа','Реализиция')
      AND period >= (SELECT MAX(period) FROM sales) - INTERVAL '12 months'
    GROUP BY magazin
) p ON o.magazin = p.magazin
"""
df = pd.read_sql(query, engine)
df = df[df["ostatok_m2"] > 0].reset_index(drop=True)
df["magazin"] = df["magazin"].str.replace("Магазин ", "")
df["v_mesyac"] = df["prodano_m2"] / 12
df["mesyacy"] = df["ostatok_m2"] / df["v_mesyac"].replace(0, 0.1)
df["mesyacy"] = df["mesyacy"].clip(upper=60)
df = df.sort_values("mesyacy").reset_index(drop=True)

colors = ["#C0491F" if v > 12 else "#3E9A66" for v in df["mesyacy"]]

fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor("white")
ax.set_facecolor("#FAFAF8")

for i, (v, c) in enumerate(zip(df["mesyacy"], colors)):
    ax.plot([0, v], [i, i], color=c, linewidth=1.8, alpha=0.5, zorder=1)
    ax.scatter(v, i, s=130, color=c, zorder=3, edgecolors="white", linewidth=1.3)
    ax.text(v + 1.5, i, f"{v:.0f} мес", va="center", fontsize=9, color="#555")

ax.set_yticks(range(len(df)))
ax.set_yticklabels(df["magazin"], fontsize=9)
ax.axvline(12, color="#B4B2A9", linestyle="--", linewidth=1.2)
ax.text(12, len(df) - 0.3, " год запаса", fontsize=9, color="#888")



ax.set_xlabel("На сколько месяцев хватит остатка при продажах за последний год",
              fontsize=10, color="#444")
ax.set_title("Запас товара в магазинах, месяцев", fontsize=15, pad=14, color="#1A1A1A")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="x", color="#E8E6DE", linewidth=0.7)
ax.set_axisbelow(True)

from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor="#3E9A66", label="здоровый запас (<12 мес)"),
                   Patch(facecolor="#C0491F", label="затоварен (>12 мес)")],
          loc="lower right", frameon=False, fontsize=10)

plt.tight_layout()
plt.savefig("mesyacy_zapasa.png", dpi=200,  bbox_inches="tight")
plt.show()