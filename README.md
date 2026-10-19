# Fahrradunfälle in Deutschland 2020–2025

Explorative Datenanalyse der Unfälle mit Fahrradbeteiligung auf Basis des Unfallatlas der Statistischen Ämter des Bundes und der Länder.

## Aufgabenstellung

Ziel ist es, Unfälle mit Fahrradbeteiligung in Deutschland zu untersuchen und Muster zu erkennen, die für die Verkehrssicherheit relevant sind. Folgende Fragen sollen beantwortet werden:

1. **Zeitliche Entwicklung:** Wie hat sich die Zahl der Fahrradunfälle zwischen 2020 und 2025 entwickelt? In welchen Monaten, an welchen Wochentagen und zu welchen Tageszeiten passieren die meisten?
2. **Räumliche Verteilung:** In welchen Bundesländern, Landkreisen und Gemeinden gibt es die meisten Fahrradunfälle? Wo liegen Hotspots, und gibt es Regionen mit besonders hohem Anteil schwerer Unfälle?
3. **Unfallschwere:** Wie verteilen sich Fahrradunfälle auf die Unfallkategorien? Unterscheidet sich die Schwere nach Tageszeit, Monat und Lichtverhältnissen, und im Vergleich zu Unfällen ohne Fahrrad?
4. **Unfallbedingungen:** Bei welchen Lichtverhältnissen, Unfalltypen, Unfallarten und Straßenzuständen passieren Fahrradunfälle am häufigsten?
5. **Vergleich:** Welchen Anteil haben Fahrradunfälle an allen Unfällen mit Personenschaden, und wie unterscheiden sich ihre zeitlichen Muster von denen anderer Unfälle?
6. **Modellierung:** Welche Faktoren erhöhen die Wahrscheinlichkeit, dass ein Fahrradunfall schwer endet? (logistische Regression)
7. **Fazit:** Welche Erkenntnisse lassen sich daraus für die Verkehrssicherheit ableiten?

## Daten

**Quelle:** Unfallatlas der Statistischen Ämter des Bundes und der Länder (Unfälle mit Personenschaden im Straßenverkehr): https://unfallatlas.statistikportal.de/

Jede Zeile entspricht einem Unfall. Unfälle mit reinem Sachschaden sind nicht enthalten. Verwendet werden die Jahre 2020 bis 2025, in denen alle 16 Bundesländer vertreten sind. 

**Die Daten liegen nicht im Repository** (der Ordner `data/` steht in der `.gitignore`) und müssen manuell heruntergeladen werden:

1. Die Jahresdateien 2020 bis 2025 (CSV bzw. TXT) von der oben genannten Quelle herunterladen.
2. Die Dateien in den Ordner `data/` im Projektverzeichnis legen (Ordner bei Bedarf anlegen).
3. Die Dateinamen müssen genau so lauten, wie sie im Notebook angegeben sind:

```
data/
├── Unfallorte2020_LinRef.csv
├── Unfallorte_2021_LinRef.txt
├── Unfallorte2022_LinRef.csv
├── Unfallorte2023_LinRef.csv
├── Unfallorte2024_LinRef.csv
└── Unfallorte_2025_LR_BasisDLM.csv
```

## Installation

Die Umgebung wird mit [uv](https://docs.astral.sh/uv/) verwaltet.

```bash
git clone https://github.com/RogovaNatalia/Unfallorte_Projekt.git
cd Unfallorte_Projekt
uv sync
```

Danach die Daten wie im Abschnitt "Daten" beschrieben in `data/` ablegen, `analyse.ipynb` in VS Code öffnen, den Kernel `.venv` auswählen und die Zellen von oben nach unten ausführen.

## Ergebnisse

_Folgt nach Abschluss der Analyse._