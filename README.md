# Fahrradunfälle in Deutschland 2020–2025

Explorative Datenanalyse der Unfälle mit Fahrradbeteiligung auf Basis des Unfallatlas der Statistischen Ämter des Bundes und der Länder.

## Aufgabenstellung

Ziel ist es, Unfälle mit Fahrradbeteiligung in Deutschland zu untersuchen und Muster zu erkennen, die für die Verkehrssicherheit relevant sind. Folgende Fragen sollen beantwortet werden:

1. **Zeitliche Entwicklung:** Wie hat sich die Zahl der Fahrradunfälle zwischen 2020 und 2025 entwickelt? In welchen Monaten, an welchen Wochentagen und zu welchen Tageszeiten werden die meisten Unfälle registriert?
2. **Räumliche Verteilung** Wie verteilen sich die Unfälle auf Bundesländer, Landkreise und Gemeinden? Wo werden besonders viele Unfälle registriert, und wie unterscheidet sich der Anteil schwerer Unfälle zwischen den Regionen?
3. **Unfallschwere:** Wie verteilen sich die Unfälle auf die Unfallkategorien? Unterscheidet sich der Anteil schwerer Unfälle nach Tageszeit und Lichtverhältnissen?
4. **Unfallbedingungen:** Welche Straßenzustände und Unfalltypen treten häufig auf? Welche weiteren Verkehrsteilnehmer sind an den Unfällen beteiligt?
5. **Modellierung:** Lässt sich anhand der bisherigen Entwicklung eine erste Prognose der Unfallzahlen für 2026 erstellen?
7. **Fazit:** Welche Erkenntnisse lassen sich aus den Ergebnissen ableiten, und welche Einschränkungen müssen bei ihrer Interpretation berücksichtigt werden?

## Daten

### Quelle

Die Unfalldaten stammen aus dem [Unfallatlas der Statistischen Ämter des Bundes und der Länder](https://unfallatlas.statistikportal.de/). Der Unfallatlas enthält georeferenzierte Daten zu Straßenverkehrsunfällen mit Personenschaden. Unfälle mit reinem Sachschaden sind nicht enthalten.

Verwendet werden die Daten der Jahre 2020 bis 2025. In diesem Zeitraum sind alle 16 Bundesländer vertreten.

### Jährliche Unfalldaten

Die jährlichen Unfalldaten werden nicht im Repository gespeichert und müssen manuell heruntergeladen werden.

1. Die Jahresdateien für 2020 bis 2025 vom [Unfallatlas](https://unfallatlas.statistikportal.de/) herunterladen.
2. Die Dateien im Ordner `data/` im Projektverzeichnis ablegen. Falls der Ordner noch nicht existiert, muss er angelegt werden.
3. Die Dateinamen müssen genau so lauten, wie sie im Notebook verwendet werden:

```text
data/
├── Unfallorte2020_LinRef.csv
├── Unfallorte_2021_LinRef.txt
├── Unfallorte2022_LinRef.csv
├── Unfallorte2023_LinRef.csv
├── Unfallorte2024_LinRef.csv
└── Unfallorte_2025_LR_BasisDLM.csv
```

Der Ordner `data/` ist in der `.gitignore` eingetragen, damit die umfangreichen jährlichen Unfalldaten nicht versehentlich in das Repository aufgenommen werden.

### Verwaltungsverzeichnis

Für die räumliche Analyse auf Ebene der Landkreise und kreisfreien Städte wird zusätzlich folgende Excel-Datei verwendet:

`data/20260131_Anschriften_der_Gemeinde_und_Stadtverwaltungen.xlsx`

Die Datei enthält das Verwaltungsverzeichnis mit Stand vom 31. Januar 2026. Sie wird verwendet, um Gebietsschlüssel den Namen der Landkreise und kreisfreien Städte zuzuordnen.

Im Gegensatz zu den jährlichen Unfalldaten ist diese Referenzdatei im Repository enthalten und muss nicht separat heruntergeladen werden.

Bei der Zuordnung der Unfalldaten zu den Landkreisen konnten 63 von insgesamt 500.799 Datensätzen aufgrund eines im Verwaltungsverzeichnis nicht enthaltenen Gebietsschlüssels nicht zugeordnet werden. Dies entspricht etwa 0,013 % aller Datensätze. Die nicht zugeordneten Datensätze werden bei der Auswertung auf Kreisebene nicht berücksichtigt.

### Definition schwerer Unfälle

Für die Analyse werden Unfälle der Kategorien 1 und 2 als schwere Unfälle zusammengefasst:

Kategorie 1: Unfall mit Getöteten
Kategorie 2: Unfall mit Schwerverletzten

Die entsprechende Variable schwer wird in der Datenaufbereitung erstellt und in den nachfolgenden Auswertungen verwendet.

### Methodik

Die Analyse wird mit Python und den Bibliotheken pandas und Matplotlib durchgeführt.

Die Arbeitsschritte umfassen:

- Einlesen und Zusammenführen der jährlichen Unfalldaten
- Aufbereitung und Prüfung der Daten
- Zuordnung der Unfälle zu Bundesländern, Landkreisen und Gemeinden
- Deskriptive Analyse der zeitlichen und räumlichen Verteilung
- Untersuchung der Unfallschwere und der Unfallbedingungen
- Analyse der Beteiligung weiterer Verkehrsteilnehmer
- Erstellung und Bewertung einer ersten Prognose für 2026

Die Auswertungen zu den absoluten Unfallzahlen und zum Anteil schwerer Unfälle beantworten unterschiedliche Fragen. Absolute Zahlen zeigen, wo viele Unfälle registriert werden. Prozentuale Anteile beschreiben dagegen die Zusammensetzung der erfassten Unfälle.

Bei Vergleichen zwischen Städten und Gemeinden werden, sofern Einwohnerzahlen einbezogen werden, auch Unfallzahlen je 100.000 Einwohner betrachtet. Diese Kennzahl berücksichtigt die Einwohnerzahl, ist jedoch keine direkte Messung des individuellen Fahrradrisikos, da beispielsweise die Zahl der Fahrradfahrten nicht berücksichtigt wird.

Die Prognose für 2026 ist als explorative Schätzung zu verstehen. Sie stellt keine gesicherte Vorhersage dar.

## Ergebnisse

*Folgt nach Abschluss der Analyse.*

## Installation

Die Python-Umgebung und die Projektabhängigkeiten werden mit [uv](https://docs.astral.sh/uv/) verwaltet.

### 1. Repository klonen

```bash
git clone https://github.com/RogovaNatalia/Unfallorte_Projekt.git
cd Unfallorte_Projekt
```

### 2. Abhängigkeiten installieren

```bash
uv sync
```

### 3. Daten vorbereiten

Die jährlichen Unfalldaten wie im Abschnitt [Daten](#daten) beschrieben herunterladen und im Ordner `data/` ablegen.

Die Excel-Datei mit dem Verwaltungsverzeichnis ist bereits im Repository enthalten.

### 4. Notebook ausführen

1. Das Projekt in Visual Studio Code öffnen.
2. Die Datei `analyse.ipynb` öffnen.
3. Die virtuelle Umgebung `.venv` als Python-Kernel auswählen.
4. Den Kernel neu starten und alle Zellen der Reihe nach von oben nach unten ausführen.
5. Prüfen, ob alle Zellen ohne Fehler durchlaufen und die Diagramme korrekt erstellt werden.

### Projektstruktur

```text
Unfallorte_Projekt/
├── data/
│   ├── population/
│   │   ├── 31122020_Auszug_GV.xlsx
│   │   ├── 31122021_Auszug_GV.xlsx
│   │   ├── 31122022_Auszug_GV.xlsx
│   │   ├── 31122023_Auszug_GV.xlsx
│   │   ├── 31122024_Auszug_GV.xlsx
│   │   └── 31122025_Auszug_GV.xlsx
│   ├── Unfallorte2020_LinRef.csv
│   ├── Unfallorte_2021_LinRef.txt
│   ├── Unfallorte2022_LinRef.csv
│   ├── Unfallorte2023_LinRef.csv
│   ├── Unfallorte2024_LinRef.csv
│   ├── Unfallorte_2025_LR_BasisDLM.csv
│   └── 20260131_Anschriften_der_Gemeinde_und_Stadtverwaltungen.xlsx
├── analyse.ipynb
├── pyproject.toml
├── uv.lock
├── .gitignore
└── README.md
```

Die jährlichen Unfalldateien werden lokal im Ordner data/ abgelegt und nicht mit dem Repository versioniert.
### Einschränkungen

Der Unfallatlas enthält Unfälle mit Personenschaden, nicht alle Verkehrsunfälle.
Die Anzahl registrierter Unfälle ist nicht gleichbedeutend mit dem individuellen Unfallrisiko.
Einwohnerbezogene Kennzahlen berücksichtigen nicht, wie häufig oder wie weit Menschen Fahrrad fahren.
Die Beteiligung weiterer Verkehrsteilnehmer kann sich zwischen den Kategorien überschneiden.
Die Ergebnisse beschreiben beobachtete Zusammenhänge und belegen keine Kausalität.
Die Prognose für 2026 ist vorläufig und aufgrund der begrenzten Datenbasis mit Unsicherheit verbunden.

### Verwendete Technologien

Python
pandas
Matplotlib
Jupyter Notebook
uv