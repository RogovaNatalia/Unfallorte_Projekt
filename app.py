
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# RADAR | Fahrradsicherheit in Deutschland
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

FILES = {
    2020: "Unfallorte2020_LinRef.csv",
    2021: "Unfallorte_2021_LinRef.txt",
    2022: "Unfallorte2022_LinRef.csv",
    2023: "Unfallorte2023_LinRef.csv",
    2024: "Unfallorte2024_LinRef.csv",
    2025: "Unfallorte_2025_LR_BasisDLM.csv",
}

STATES = {
    1: "Schleswig-Holstein",
    2: "Hamburg",
    3: "Niedersachsen",
    4: "Bremen",
    5: "Nordrhein-Westfalen",
    6: "Hessen",
    7: "Rheinland-Pfalz",
    8: "Baden-Württemberg",
    9: "Bayern",
    10: "Saarland",
    11: "Berlin",
    12: "Brandenburg",
    13: "Mecklenburg-Vorpommern",
    14: "Sachsen",
    15: "Sachsen-Anhalt",
    16: "Thüringen",
}

MONTHS = {
    1: "Jan", 2: "Feb", 3: "Mär", 4: "Apr",
    5: "Mai", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Okt", 11: "Nov", 12: "Dez",
}

WEEKDAYS = {
    1: "Montag", 2: "Dienstag", 3: "Mittwoch",
    4: "Donnerstag", 5: "Freitag",
    6: "Samstag", 7: "Sonntag",
}

BG = "#0B1120"
PANEL = "#111C2E"
GRID = "#273449"
TEXT = "#F1F5F9"
MUTED = "#94A3B8"
GREEN = "#A3E635"
RED = "#FB7185"
BLUE = "#60A5FA"
TEAL = "#2DD4BF"

st.set_page_config(
    page_title="RADAR | Fahrradsicherheit",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {BG};
        color: {TEXT};
    }}
    [data-testid="stHeader"] {{
        background: {BG};
    }}
    [data-testid="stSidebar"] {{
        background: #0E1727;
        border-right: 1px solid {GRID};
    }}
    [data-testid="stMetric"] {{
        background: {PANEL};
        border: 1px solid {GRID};
        padding: 18px 20px;
        border-radius: 14px;
    }}
    [data-testid="stMetricLabel"] {{
        color: {MUTED};
    }}
    [data-testid="stMetricValue"] {{
        color: {TEXT};
    }}
    h1, h2, h3 {{
        letter-spacing: -0.025em;
    }}
    .eyebrow {{
        color: {GREEN};
        text-transform: uppercase;
        letter-spacing: 0.16em;
        font-size: 0.72rem;
        font-weight: 700;
    }}
    .hero {{
        padding: 12px 0 22px 0;
    }}
    .hero-sub {{
        color: {MUTED};
        font-size: 1rem;
    }}
    .note {{
        color: {MUTED};
        font-size: 0.83rem;
    }}
    div[data-testid="stTabs"] button {{
        font-weight: 600;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Hilfsfunktionen
# =========================================================

def find_column(df, *names):
    lookup = {
        str(c).strip().upper(): c
        for c in df.columns
    }
    for name in names:
        if name.upper() in lookup:
            return lookup[name.upper()]
    return None


def numeric(series):
    return pd.to_numeric(series, errors="coerce")


def binary(series):
    """Wandelt übliche binäre Werte in 0/1 um."""
    if pd.api.types.is_bool_dtype(series):
        return series.astype("Int64")

    text = series.astype("string").str.strip().str.lower()
    mapping = {
        "1": 1, "1.0": 1, "true": 1,
        "ja": 1, "yes": 1,
        "0": 0, "0.0": 0, "false": 0,
        "nein": 0, "no": 0,
    }
    return text.map(mapping).astype("Int64")


def fmt(value):
    return f"{int(value):,}".replace(",", ".")


def chart_layout(fig, height=360):
    fig.update_layout(
        height=height,
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font=dict(
            family="Inter, sans-serif",
            color=TEXT,
            size=12,
        ),
        title=dict(
            font=dict(size=16, color=TEXT),
            x=0.02,
            xanchor="left",
        ),
        margin=dict(l=18, r=18, t=62, b=25),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=MUTED),
        ),
        hoverlabel=dict(
            bgcolor="#172338",
            font_color=TEXT,
        ),
    )
    fig.update_xaxes(
        gridcolor=GRID,
        zerolinecolor=GRID,
        linecolor=GRID,
        tickfont=dict(color=MUTED),
        title_font=dict(color=MUTED),
    )
    fig.update_yaxes(
        gridcolor=GRID,
        zerolinecolor=GRID,
        linecolor=GRID,
        tickfont=dict(color=MUTED),
        title_font=dict(color=MUTED),
    )
    return fig


def show_chart(fig, height=360):
    chart_layout(fig, height)
    st.plotly_chart(fig, use_container_width=True)


# =========================================================
# Datenimport
# =========================================================

@st.cache_data(show_spinner="Lade Unfallatlas 2020–2025 …")
def load_data():
    frames = []
    problems = []

    for year, filename in FILES.items():
        path = DATA_DIR / filename

        if not path.is_file():
            problems.append(f"Datei fehlt: {filename}")
            continue

        loaded = None
        errors = []

        for encoding in ("utf-8-sig", "cp1252", "latin1"):
            for separator in (";", ",", "\t", "|"):
                try:
                    candidate = pd.read_csv(
                        path,
                        sep=separator,
                        encoding=encoding,
                        low_memory=False,
                    )
                    candidate.columns = (
                        candidate.columns.astype(str).str.strip()
                    )

                    if (
                        len(candidate.columns) > 5
                        and "IstRad" in candidate.columns
                    ):
                        loaded = candidate
                        break
                except Exception as exc:
                    errors.append(str(exc))

            if loaded is not None:
                break

        if loaded is None:
            problems.append(
                f"{filename} konnte nicht gelesen werden. "
                + " | ".join(errors[-2:])
            )
            continue

        loaded["Jahr"] = year
        frames.append(loaded)

    if not frames:
        raise RuntimeError(
            "Keine Unfall-Datei erfolgreich geladen.\n"
            + "\n".join(problems)
        )

    return pd.concat(frames, ignore_index=True, sort=False), problems


try:
    raw, load_problems = load_data()
except Exception as exc:
    st.error(f"Datenimport fehlgeschlagen: {exc}")
    st.write(f"Erwarteter Ordner: `{DATA_DIR}`")
    if DATA_DIR.exists():
        st.write(
            "Vorhandene Dateien:",
            sorted(p.name for p in DATA_DIR.iterdir() if p.is_file()),
        )
    st.stop()


# =========================================================
# Aufbereitung
# =========================================================

rad_col = find_column(raw, "IstRad")
category_col = find_column(raw, "UKATEGORIE")
state_col = find_column(raw, "ULAND")
district_col = find_column(raw, "UKREIS")
municipality_col = find_column(raw, "UGEMEINDE")
month_col = find_column(raw, "UMONAT")
hour_col = find_column(raw, "USTUNDE")
weekday_col = find_column(raw, "UWOCHENTAG")
lon_col = find_column(raw, "XGCSWGS84")
lat_col = find_column(raw, "YGCSWGS84")

if rad_col is None:
    st.error("Die Spalte IstRad wurde nicht gefunden.")
    st.stop()

raw["_Rad"] = binary(raw[rad_col])
bike = raw.loc[raw["_Rad"].eq(1)].copy()

if bike.empty:
    st.error("Keine Datensätze mit IstRad = 1 gefunden.")
    st.write(
        raw[rad_col]
        .astype("string")
        .value_counts(dropna=False)
        .head(20)
    )
    st.stop()

bike["Jahr"] = numeric(bike["Jahr"]).astype("Int64")
bike["_Kategorie"] = (
    numeric(bike[category_col])
    if category_col else pd.NA
)

# Unfallatlas-Kategorien:
# 1 = mit Getöteten, 2 = mit Schwerverletzten,
# 3 = mit Leichtverletzten.
bike["Unfallschwere"] = bike["_Kategorie"].map({
    1: "Getötete",
    2: "Schwerverletzte",
    3: "Leichtverletzte",
}).fillna("Unbekannte Kategorie")

bike["Schwer oder tödlich"] = bike["_Kategorie"].isin([1, 2])

bike["Bundesland"] = (
    numeric(bike[state_col]).map(STATES).fillna("Unbekannt")
    if state_col else "Unbekannt"
)

bike["Landkreis-Code"] = (
    bike[district_col].astype("string")
    if district_col else "Unbekannt"
)
bike["Gemeinde-Code"] = (
    bike[municipality_col].astype("string")
    if municipality_col else "Unbekannt"
)

bike["Monat-Nr"] = numeric(bike[month_col]) if month_col else pd.NA
bike["Stunde"] = numeric(bike[hour_col]) if hour_col else pd.NA
bike["Wochentag-Nr"] = (
    numeric(bike[weekday_col]) if weekday_col else pd.NA
)

bike["Monat"] = bike["Monat-Nr"].map(MONTHS)
bike["Wochentag"] = bike["Wochentag-Nr"].map(WEEKDAYS)

bike["Longitude"] = numeric(bike[lon_col]) if lon_col else pd.NA
bike["Latitude"] = numeric(bike[lat_col]) if lat_col else pd.NA

participant_fields = {
    "PKW": find_column(bike, "IstPKW"),
    "Fußgänger": find_column(bike, "IstFuss"),
    "Kraftrad": find_column(bike, "IstKrad"),
    "Güterkraftfahrzeug": find_column(bike, "IstGkfz"),
    "Sonstige": find_column(bike, "IstSonstige"),
}

for label, column in participant_fields.items():
    if column:
        bike[f"Beteiligung: {label}"] = binary(
            bike[column]
        ).eq(1)

# =========================================================
# Sidebar und Filter
# =========================================================

st.sidebar.markdown("## RADAR")
st.sidebar.caption("FAHRRADUNFÄLLE · DEUTSCHLAND")
st.sidebar.divider()

years = sorted(bike["Jahr"].dropna().astype(int).unique())
selected_years = st.sidebar.multiselect(
    "Unfalljahre",
    years,
    default=years,
)

states = sorted(bike["Bundesland"].dropna().unique())
selected_states = st.sidebar.multiselect(
    "Bundesländer",
    states,
    default=states,
)

severity_options = {
    "Alle Fahrradunfälle": None,
    "Schwer oder tödlich": [1, 2],
    "Mit Getöteten": [1],
    "Mit Schwerverletzten": [2],
    "Mit Leichtverletzten": [3],
}

severity_label = st.sidebar.selectbox(
    "Unfallschwere",
    list(severity_options),
)

df = bike[
    bike["Jahr"].isin(selected_years)
    & bike["Bundesland"].isin(selected_states)
].copy()

categories = severity_options[severity_label]
if categories is not None:
    df = df[df["_Kategorie"].isin(categories)]

if df.empty:
    st.warning("Keine Daten für die ausgewählte Filterkombination.")
    st.stop()

# =========================================================
# Kopfbereich
# =========================================================

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Mobility intelligence / Germany</div>
      <h1 style="font-size:2.55rem; margin-bottom:0.3rem;">
        RADAR<span style="color:#A3E635;">.</span>
      </h1>
      <div class="hero-sub">
        Fahrradsicherheit verstehen. Risiken sichtbar machen.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if load_problems:
    with st.expander("Datenimport-Hinweise"):
        for problem in load_problems:
            st.warning(problem)

# =========================================================
# Kennzahlen
# =========================================================

total = len(df)
severe = int(df["Schwer oder tödlich"].sum())
fatal = int(df["_Kategorie"].eq(1).sum())
share = severe / total * 100 if total else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Fahrradunfälle", fmt(total))
k2.metric("Schwer / tödlich", fmt(severe))
k3.metric("Mit Getöteten", fmt(fatal))
k4.metric("Anteil schwer / tödlich", f"{share:.1f} %")

st.caption(
    "Auswertung nur für Datensätze mit IstRad = 1. "
    "Absolute Unfallzahlen sind keine direkten Risikowerte."
)

# =========================================================
# Tabs
# =========================================================

overview, time_tab, region_tab, map_tab, details_tab, population_tab = (
    st.tabs([
        "Overview",
        "Zeit & Saison",
        "Regionen",
        "Unfallkarte",
        "Schwere & Beteiligte",
        "Bevölkerung & Daten",
    ])
)

# =========================================================
# Overview
# =========================================================

with overview:
    st.subheader("Entwicklung der Fahrradunfälle")

    left, right = st.columns([1.5, 1])

    yearly = (
        df.groupby("Jahr")
        .agg(
            Unfälle=("_Kategorie", "size"),
            Schwere_Unfälle=("Schwer oder tödlich", "sum"),
        )
        .reset_index()
    )

    with left:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=yearly["Jahr"],
            y=yearly["Unfälle"],
            mode="lines+markers",
            name="Alle Fahrradunfälle",
            line=dict(color=GREEN, width=3),
            marker=dict(size=8),
        ))
        fig.add_trace(go.Scatter(
            x=yearly["Jahr"],
            y=yearly["Schwere_Unfälle"],
            mode="lines+markers",
            name="Schwer / tödlich",
            line=dict(color=RED, width=2),
            marker=dict(size=6),
        ))
        fig.update_layout(
            title="Unfälle im Zeitverlauf",
            xaxis_title="Jahr",
            yaxis_title="Anzahl",
            legend_title="",
        )
        show_chart(fig, 390)

    with right:
        state_top = (
            df.groupby("Bundesland")
            .size()
            .sort_values(ascending=False)
            .head(8)
            .sort_values()
            .reset_index(name="Unfälle")
        )
        fig = px.bar(
            state_top,
            x="Unfälle",
            y="Bundesland",
            orientation="h",
            title="Bundesländer nach Unfallzahl",
            color_discrete_sequence=[GREEN],
        )
        show_chart(fig, 390)

    st.subheader("Monatliches Muster")
    monthly = (
        df.dropna(subset=["Monat-Nr"])
        .groupby("Monat-Nr")
        .size()
        .reindex(range(1, 13), fill_value=0)
        .rename("Unfälle")
        .reset_index()
    )
    monthly["Monat"] = monthly["Monat-Nr"].map(MONTHS)
    fig = px.bar(
        monthly,
        x="Monat",
        y="Unfälle",
        title="Wann passieren Fahrradunfälle?",
        color="Unfälle",
        color_continuous_scale=["#365314", GREEN],
        category_orders={"Monat": list(MONTHS.values())},
    )
    fig.update_layout(coloraxis_showscale=False)
    show_chart(fig, 330)

# =========================================================
# Zeit und Saison
# =========================================================

with time_tab:
    st.subheader("Zeitliche Muster")
    c1, c2 = st.columns(2)

    with c1:
        monthly_year = (
            df.dropna(subset=["Monat-Nr"])
            .groupby(["Jahr", "Monat-Nr"])
            .size()
            .reset_index(name="Unfälle")
        )
        monthly_year["Monat"] = monthly_year["Monat-Nr"].map(MONTHS)
        fig = px.line(
            monthly_year,
            x="Monat",
            y="Unfälle",
            color="Jahr",
            markers=True,
            title="Saisonverlauf im Jahresvergleich",
            category_orders={"Monat": list(MONTHS.values())},
            color_discrete_sequence=px.colors.sequential.Greens_r,
        )
        show_chart(fig, 400)

    with c2:
        weekday = (
            df.dropna(subset=["Wochentag-Nr"])
            .groupby("Wochentag-Nr")
            .size()
            .reindex(range(1, 8), fill_value=0)
            .rename("Unfälle")
            .reset_index()
        )
        weekday["Wochentag"] = weekday["Wochentag-Nr"].map(WEEKDAYS)
        fig = px.bar(
            weekday,
            x="Wochentag",
            y="Unfälle",
            title="Unfälle nach Wochentag",
            color_discrete_sequence=[TEAL],
        )
        show_chart(fig, 400)

    hourly = (
        df.dropna(subset=["Stunde"])
        .groupby("Stunde")
        .size()
        .reindex(range(24), fill_value=0)
        .rename("Unfälle")
        .reset_index()
    )
    fig = px.area(
        hourly,
        x="Stunde",
        y="Unfälle",
        title="Unfälle nach Tageszeit",
    )
    fig.update_traces(
        line_color=GREEN,
        fillcolor="rgba(163,230,53,0.15)",
    )
    show_chart(fig, 350)

# =========================================================
# Regionale Vergleiche
# =========================================================

with region_tab:
    st.subheader("Bundesländer im Vergleich")

    state_stats = (
        df.groupby("Bundesland")
        .agg(
            Unfälle=("_Kategorie", "size"),
            Schwer=("Schwer oder tödlich", "sum"),
            Anteil_schwer=("Schwer oder tödlich", "mean"),
        )
        .reset_index()
    )
    state_stats["Anteil_schwer"] *= 100

    left, right = st.columns(2)

    with left:
        fig = px.bar(
            state_stats.sort_values("Unfälle"),
            x="Unfälle",
            y="Bundesland",
            orientation="h",
            title="Anzahl der Fahrradunfälle",
            color_discrete_sequence=[GREEN],
        )
        show_chart(fig, 520)

    with right:
        fig = px.bar(
            state_stats.sort_values("Anteil_schwer"),
            x="Anteil_schwer",
            y="Bundesland",
            orientation="h",
            title="Anteil schwerer / tödlicher Unfälle (%)",
            color_discrete_sequence=[RED],
        )
        show_chart(fig, 520)

    st.subheader("Landkreise")
    district_stats = (
        df.groupby(["Bundesland", "Landkreis-Code"])
        .size()
        .reset_index(name="Unfälle")
        .sort_values("Unfälle", ascending=False)
        .head(25)
    )
    fig = px.bar(
        district_stats.sort_values("Unfälle"),
        x="Unfälle",
        y="Landkreis-Code",
        color="Bundesland",
        orientation="h",
        title="25 Landkreise mit den meisten Unfällen",
    )
    show_chart(fig, 600)

    st.subheader("Gemeinden")
    city_stats = (
        df.groupby(["Bundesland", "Gemeinde-Code"])
        .size()
        .reset_index(name="Unfälle")
        .sort_values("Unfälle", ascending=False)
        .head(25)
    )
    fig = px.bar(
        city_stats.sort_values("Unfälle"),
        x="Unfälle",
        y="Gemeinde-Code",
        color="Bundesland",
        orientation="h",
        title="25 Gemeinden mit den meisten Unfällen",
    )
    show_chart(fig, 600)

    st.dataframe(
        state_stats.sort_values("Unfälle", ascending=False).round(2),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Regionale Ranglisten zeigen absolute Fallzahlen. "
        "Sie sind keine Rangliste des individuellen Unfallrisikos."
    )

# =========================================================
# Karte
# =========================================================

with map_tab:
    st.subheader("Geografische Verteilung")

    map_df = df.dropna(subset=["Longitude", "Latitude"]).copy()
    map_df = map_df[
        map_df["Longitude"].between(5, 16)
        & map_df["Latitude"].between(47, 56)
    ]

    if map_df.empty:
        st.warning(
            "Keine plausiblen Koordinaten gefunden. "
            "Bitte XGCSWGS84 und YGCSWGS84 prüfen."
        )
    else:
        st.caption(
            f"{fmt(len(map_df))} Datensätze mit plausiblen Koordinaten. "
            "Zur Performance werden höchstens 10.000 Punkte dargestellt."
        )

        map_sample = map_df.sample(
            n=min(10000, len(map_df)),
            random_state=42,
        )

        fig = px.scatter_mapbox(
            map_sample,
            lat="Latitude",
            lon="Longitude",
            color="Unfallschwere",
            hover_data=["Jahr", "Bundesland", "Unfallschwere"],
            zoom=4,
            height=680,
            mapbox_style="open-street-map",
            color_discrete_map={
                "Getötete": RED,
                "Schwerverletzte": "#FB923C",
                "Leichtverletzte": GREEN,
                "Unbekannte Kategorie": MUTED,
            },
        )
        fig.update_layout(
            paper_bgcolor=PANEL,
            font_color=TEXT,
            margin=dict(l=0, r=0, t=20, b=0),
        )
        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# Schwere und Beteiligte
# =========================================================

with details_tab:
    st.subheader("Unfallschwere")

    left, right = st.columns(2)

    severity_counts = (
        df["Unfallschwere"]
        .value_counts()
        .rename_axis("Kategorie")
        .reset_index(name="Unfälle")
    )

    with left:
        fig = px.pie(
            severity_counts,
            names="Kategorie",
            values="Unfälle",
            hole=0.55,
            title="Verteilung nach Unfallschwere",
            color="Kategorie",
            color_discrete_map={
                "Getötete": RED,
                "Schwerverletzte": "#FB923C",
                "Leichtverletzte": GREEN,
                "Unbekannte Kategorie": MUTED,
            },
        )
        show_chart(fig, 390)

    with right:
        yearly_severity = (
            df.groupby(["Jahr", "Unfallschwere"])
            .size()
            .reset_index(name="Unfälle")
        )
        fig = px.bar(
            yearly_severity,
            x="Jahr",
            y="Unfälle",
            color="Unfallschwere",
            barmode="stack",
            title="Unfallschwere nach Jahr",
            color_discrete_map={
                "Getötete": RED,
                "Schwerverletzte": "#FB923C",
                "Leichtverletzte": GREEN,
                "Unbekannte Kategorie": MUTED,
            },
        )
        show_chart(fig, 390)

    st.subheader("Weitere Unfallbeteiligte")

    counts = []
    for label in [
        "PKW", "Fußgänger", "Kraftrad",
        "Güterkraftfahrzeug", "Sonstige",
    ]:
        col = f"Beteiligung: {label}"
        if col in df.columns:
            counts.append({
                "Beteiligte": label,
                "Unfälle": int(df[col].sum()),
            })

    if counts:
        participants = pd.DataFrame(counts)
        fig = px.bar(
            participants.sort_values("Unfälle"),
            x="Unfälle",
            y="Beteiligte",
            orientation="h",
            title="Weitere Beteiligte bei Fahrradunfällen",
            color_discrete_sequence=[TEAL],
        )
        show_chart(fig, 400)
        st.caption(
            "Ein Unfall kann mehrere Beteiligungsarten aufweisen. "
            "Die Werte sind daher nicht additiv."
        )
    else:
        st.info("Keine passenden Beteiligungsfelder verfügbar.")

# =========================================================
# Bevölkerung und Datenqualität
# =========================================================

with population_tab:
    st.subheader("Bevölkerung und Unfallraten")

    st.markdown(
        """
        ### Warum absolute Zahlen nicht ausreichen

        Große Bundesländer und Städte können viele Unfälle haben,
        weil dort mehr Menschen leben oder mehr Rad gefahren wird.

        Für einen faireren Vergleich benötigen wir:
        - Einwohnerzahlen mit passendem Gebietsstand,
        - eindeutige Gemeinde- oder Kreisschlüssel,
        - idealerweise Daten zur Fahrradnutzung oder zum Radverkehrsaufkommen.
        """
    )

    population_dir = DATA_DIR / "population"
    if population_dir.exists():
        population_files = sorted(
            p.name for p in population_dir.glob("*.xlsx")
        )
        st.write("Gefundene Bevölkerungsdateien:")
        st.write(population_files)
    else:
        st.warning(
            "Der Unterordner data/population wurde nicht gefunden."
        )

    st.info(
        "Die Einwohnerzahlen sind noch nicht mit den Unfall-Datensätzen "
        "verknüpft. Deshalb werden hier bewusst keine Unfallraten pro "
        "100.000 Einwohner ausgegeben. Die Verknüpfung muss anhand der "
        "Gemeinde- oder Kreisschlüssel und des jeweiligen Jahres erfolgen."
    )

    st.subheader("Datenqualität")
    quality = pd.DataFrame({
        "Prüfung": [
            "Geladene Rohdatensätze",
            "Datensätze mit IstRad = 1",
            "Datensätze ohne Unfallkategorie",
            "Datensätze ohne Bundeslandzuordnung",
            "Datensätze ohne Koordinaten",
        ],
        "Anzahl": [
            len(raw),
            len(bike),
            int(bike["_Kategorie"].isna().sum()),
            int(bike["Bundesland"].eq("Unbekannt").sum()),
            int(bike[["Longitude", "Latitude"]].isna().any(axis=1).sum()),
        ],
    })
    st.dataframe(quality, use_container_width=True, hide_index=True)

# =========================================================
# Datenexport
# =========================================================

st.divider()
st.subheader("Datenexport")

export = df.copy()
csv = export.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    "Gefilterte Fahrradunfälle als CSV herunterladen",
    data=csv,
    file_name="radar_fahrradunfaelle_2020_2025.csv",
    mime="text/csv",
)

with st.expander("Rohdaten-Vorschau"):
    preview = df.head(500).copy()
    for col in preview.columns:
        if preview[col].dtype == "object":
            preview[col] = preview[col].map(
                lambda value: (
                    str(value)
                    if isinstance(value, int)
                    and abs(value) > 2**63 - 1
                    else value
                )
            )
    st.dataframe(preview, use_container_width=True, hide_index=True)

st.markdown(
    f"""
    <div style="padding:24px 0;color:{MUTED};font-size:0.8rem;">
    RADAR · Fahrradsicherheit in Deutschland · Unfallatlas 2020–2025
    <br>
    Lokale Analyse · Datenquelle: lokale Unfallatlas-Dateien
    </div>
    """,
    unsafe_allow_html=True,
)
