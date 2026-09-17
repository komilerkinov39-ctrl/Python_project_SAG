import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:ПАРОЛЬ@localhost:5432/sag_project")

query = """
SELECT v.zavod, v.berdo, k.kollection, v.kolichestvo
FROM (
    SELECT zavod, berdo, kachestvo, kolichestvo FROM vypusk_antp_10_25
    UNION ALL
    SELECT zavod, berdo, kachestvo, kolichestvo FROM vypusk_xiva_10_25
) v
JOIN konstanta k ON v.kachestvo = k.kachestvo
"""
df = pd.read_sql(query, engine)

top = df.groupby("kollection")["kolichestvo"].sum().nlargest(8).index
df["kollection"] = df["kollection"].where(df["kollection"].isin(top), "Прочие")

df["berdo"] = "бердо " + df["berdo"].astype(str)

fig = px.sunburst(
    df,
    path=["zavod", "berdo", "kollection"],
    values="kolichestvo",
    color="zavod",
    color_discrete_map={"ANTP": "#0C447C", "XIVA": "#C0491F"},
)

fig.update_layout(
    title="Структура выпуска: завод --> бердо --> коллекция (октябрь 2025)",
    font=dict(family="Segoe UI", size=17, color="black"),
    margin=dict(t=60, l=0, r=0, b=0),
)
fig.update_traces(textinfo="label+percent parent")

fig.write_image("sunburst_vypusk.png", width=900, height=900, scale=2)
fig.show()