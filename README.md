# Fahrradunfälle in Deutschland 2020–2025

Explorative Datenanalyse der Unfälle mit Fahrradbeteiligung auf Basis des Unfallatlas der Statistischen Ämter des Bundes und der Länder.

## Aufgabenstellung

Ziel ist es, Unfälle mit Fahrradbeteiligung in Deutschland zu untersuchen und Muster zu erkennen, die für die Verkehrssicherheit relevant sind. Folgende Fragen sollen beantwortet werden:

1. **Zeitliche Entwicklung:** Wie hat sich die Zahl der Fahrradunfälle zwischen 2020 und 2025 entwickelt? In welchen Monaten, an welchen Wochentagen und zu welchen Tageszeiten passieren die meisten?
2. **Räumliche Verteilung** In welchen Bundesländern, Landkreisen und Gemeinden werden die meisten Fahrradunfälle registriert? Wo lassen sich geografische Häufungen von Fahrradunfällen erkennen, und gibt es Regionen mit besonders hohen Anteilen schwerer Fahrradunfälle?
3. **Unfallschwere:** Wie verteilen sich Fahrradunfälle auf die Unfallkategorien? Unterscheidet sich die Schwere nach Tageszeit und Lichtverhältnissen?
4. **Unfallbedingungen:** Wie verteilen sich Fahrradunfälle nach dem Straßenzustand? Welche   Unfalltypen treten bei Fahrradunfällen am häufigsten auf?
5. **Modellierung:** 
7. **Fazit:** Welche Erkenntnisse lassen sich daraus für die Verkehrssicherheit ableiten?

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
4. Die Zellen des Notebooks der Reihe nach von oben nach unten ausführen.

## Ergebnisse

*Folgt nach Abschluss der Analyse.*