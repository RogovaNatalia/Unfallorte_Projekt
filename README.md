# Fahrradunfälle in Deutschland 2020–2025

Explorative Datenanalyse von Straßenverkehrsunfällen mit Fahrradbeteiligung auf Basis des Unfallatlas der Statistischen Ämter des Bundes und der Länder.

## Aufgabenstellung

Ziel ist es, Unfälle mit Fahrradbeteiligung in Deutschland zu untersuchen und Muster zu erkennen, die für die Verkehrssicherheit relevant sind. Im Mittelpunkt stehen folgende Fragen:

1. **Zeitliche Entwicklung:** Wie hat sich die Zahl der Fahrradunfälle zwischen 2020 und 2025 entwickelt? In welchen Monaten, an welchen Wochentagen und zu welchen Tageszeiten werden die meisten Unfälle registriert?
2. **Räumliche Verteilung:** Wie verteilen sich die Unfälle auf Bundesländer, Landkreise und Gemeinden? Wo werden besonders viele Unfälle registriert, und wie unterscheidet sich der Anteil schwerer Unfälle zwischen den Regionen?
3. **Unfallschwere:** Wie verteilen sich die Unfälle auf die Unfallkategorien? Unterscheidet sich der Anteil schwerer Unfälle nach Tageszeit und Lichtverhältnissen?
4. **Unfallbedingungen:** Welche Straßenzustände und Unfalltypen treten häufig auf? Welche weiteren Verkehrsteilnehmer sind an den Unfällen beteiligt?
5. **Modellierung:** Lässt sich anhand der bisherigen Entwicklung eine erste Prognose der Unfallzahlen für 2026 erstellen?

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

Die jährlichen Unfalldateien sind in `.gitignore` ausgeschlossen und werden nicht mit dem Repository versioniert.

### Verwaltungsverzeichnis

Für die räumliche Analyse auf Ebene der Landkreise und kreisfreien Städte wird zusätzlich folgende Excel-Datei verwendet:

`data/20260131_Anschriften_der_Gemeinde_und_Stadtverwaltungen.xlsx`

Die Datei enthält das Verwaltungsverzeichnis mit Stand vom 31. Januar 2026. Sie wird verwendet, um Gebietsschlüssel den Namen der Landkreise und kreisfreien Städte zuzuordnen. Die Referenzdatei ist im Repository enthalten und muss nicht separat heruntergeladen werden.

Bei der Zuordnung der Unfalldaten zu den Landkreisen konnten 63 von insgesamt 500.799 Datensätzen aufgrund eines im Verwaltungsverzeichnis nicht enthaltenen Gebietsschlüssels nicht zugeordnet werden. Dies entspricht etwa 0,013 % aller Datensätze. Diese Datensätze werden bei Auswertungen auf Kreisebene nicht berücksichtigt.

### Einwohnerzahlen

Für die Berechnung von Unfallzahlen je 100.000 Einwohner werden die Einwohnerzahlen der Gemeinden aus dem Gemeindeverzeichnis des Statistischen Bundesamtes (GV-ISys, „Gemeinden in Deutschland nach Fläche, Bevölkerung und Postleitzahl“) mit Stand vom 31. Dezember verwendet.

Die Dateien für die Jahre 2020 bis 2025 liegen im Ordner `data/population/`:

```text
data/population/
├── 31122020_Auszug_GV.xlsx
├── 31122021_Auszug_GV.xlsx
├── 31122022_Auszug_GV.xlsx
├── 31122023_Auszug_GV.xlsx
├── 31122024_Auszug_GV.xlsx
└── 31122025_Auszug_GV.xlsx
```

Quelle: [Statistisches Bundesamt – Gemeindeverzeichnis](https://www.statistikportal.de/de/gemeindeverzeichnis)

Die Einwohnerzahlen ergänzen die absoluten Unfallzahlen um eine bevölkerungsbezogene Kennzahl. Sie bilden jedoch nicht ab, wie häufig oder wie weit Menschen Fahrrad fahren.

### Definition schwerer Unfälle

Für die Analyse werden Unfälle der Kategorien 1 und 2 als schwere Unfälle zusammengefasst:

- **Kategorie 1:** Unfall mit Getöteten
- **Kategorie 2:** Unfall mit Schwerverletzten

Die Variable `schwer` wird während der Datenaufbereitung erstellt und in den nachfolgenden Auswertungen verwendet.

## Methodik

Die Analyse wird mit Python und den Bibliotheken pandas, Matplotlib sowie statsmodels für die lineare Regression durchgeführt. Die Auswertung erfolgt in einem Jupyter Notebook.

Die Arbeitsschritte umfassen:

- Einlesen und Zusammenführen der jährlichen Unfalldaten
- Aufbereitung und Prüfung der Daten
- Zuordnung der Unfälle zu Bundesländern, Landkreisen und Gemeinden
- Deskriptive Analyse der zeitlichen und räumlichen Verteilung
- Untersuchung der Unfallschwere und der Unfallbedingungen
- Analyse der Beteiligung weiterer Verkehrsteilnehmer
- Erstellung und Bewertung einer explorativen Prognose für 2026

Absolute Unfallzahlen und Anteile schwerer Unfälle beantworten unterschiedliche Fragen: Absolute Zahlen zeigen, wo viele Unfälle registriert werden; prozentuale Anteile beschreiben die Zusammensetzung der erfassten Unfälle.

Für Städtevergleiche werden, sofern die Einwohnerzahlen vorliegen, zusätzlich Unfallzahlen je 100.000 Einwohner betrachtet. Diese Kennzahl berücksichtigt die Einwohnerzahl, ist aber keine direkte Messung des individuellen Fahrradrisikos, da beispielsweise die Zahl der Fahrradfahrten nicht berücksichtigt wird.

## Ergebnisse

Die Analyse umfasst 500.799 Unfälle mit Fahrradbeteiligung aus den Jahren 2020 bis 2025. Die Daten beziehen sich auf Straßenverkehrsunfälle mit Personenschaden und bilden daher nicht sämtliche Fahrradunfälle ab.

### Zeitliche Entwicklung

Die Zahl der Fahrradunfälle stieg von 78.187 im Jahr 2020 auf 89.521 im Jahr 2025 (rund +14,5 %). Der niedrigste Wert lag 2021 bei 77.316. Der Anteil der Fahrradunfälle an allen Unfällen mit Personenschaden blieb mit 32,0 bis 32,9 % nahezu konstant.

Die meisten Fahrradunfälle wurden im Juni (64.150), Juli (59.907) und September (57.613) registriert. Die höchsten Fallzahlen nach Tageszeit traten am Nachmittag auf (16 Uhr: 47.107; 15 Uhr: 45.561; 17 Uhr: 43.846). Von Dienstag bis Donnerstag wurden mit jeweils rund 81.000 Unfällen die meisten Unfälle registriert; am Wochenende waren es deutlich weniger (Samstag: 58.520, Sonntag: 46.759).

### Räumliche Verteilung

Die meisten Fahrradunfälle wurden in Nordrhein-Westfalen (109.796), Bayern (95.069) und Baden-Württemberg (58.337) registriert. Zusammen entfallen rund 53 % aller erfassten Unfälle auf diese drei Bundesländer.

Auf Ebene der Gemeinden liegen Berlin (27.751), Hamburg (16.655), München (14.244) und Köln (11.108) vorn. Die zehn Gemeinden mit den meisten Fahrradunfällen vereinen rund 21 % aller Unfälle. Diese absoluten Zahlen spiegeln auch Unterschiede bei Einwohnerzahl, Verkehrsaufkommen und Fahrradnutzung wider.

Der Anteil schwerer Fahrradunfälle liegt bundesweit bei 16,8 %. Am höchsten ist er im Saarland (22,6 %), in Thüringen (22,3 %) und in Sachsen (21,1 %), am niedrigsten in Hamburg (8,9 %), Bremen (11,5 %) und Berlin (12,8 %). Zwischen 2020 und 2025 sank der Anteil in allen 16 Bundesländern. In den zehn einwohnerstärksten Städten lagen die schweren Fahrradunfälle je 100.000 Einwohner im Jahr 2025 zwischen 7,2 (Dortmund) und 18,5 (Köln).

### Unfallschwere und Unfallbedingungen

Der Anteil schwerer Fahrradunfälle lag bei Dunkelheit bei 18,7 %, bei Tageslicht bei 16,6 % und in der Dämmerung bei 15,2 %. Dies zeigt einen Zusammenhang zwischen Lichtverhältnissen und Unfallschwere, belegt jedoch keine Ursache-Wirkungs-Beziehung.

Die meisten Unfälle ereigneten sich auf trockenen Straßen (81,9 %), gefolgt von nassen oder schlüpfrigen Straßen (17,0 %) und winterglatten Straßen (1,0 %).

Der häufigste Unfalltyp war der Einbiegen-/Kreuzen-Unfall (29,8 %), gefolgt vom Fahrunfall (19,6 %) und sonstigen Unfällen (16,3 %). Die Häufigkeiten beschreiben die registrierten Unfälle, erlauben aber keine direkten Rückschlüsse auf das Risiko unter den jeweiligen Bedingungen.

### Prognose für 2026

Für die zehn einwohnerstärksten Städte wurde je Stadt ein linearer Trend aus den Jahren 2020 bis 2025 fortgeschrieben. Die Summe der Prognosen für 2026 beträgt rund 16.700 Unfälle. Die höchsten prognostizierten Werte ergeben sich für Berlin (4.483), Hamburg (3.053) und München (2.487). Bei den schweren Unfällen liegen die Prognosen für Berlin (512), Hamburg (243) und München (192) am höchsten.

Die zeitliche Verteilung nach Monat, Wochentag und Uhrzeit wurde anhand der Anteile aus den Jahren 2020 bis 2025 auf die Jahresprognose übertragen. Die Prognose beruht auf nur sechs Jahreswerten je Stadt. Das Bestimmtheitsmaß R² beschreibt, wie gut die Gerade zu den bisherigen Daten passt, nicht die Genauigkeit der Vorhersage. Wetter, Veranstaltungen und verkehrspolitische Änderungen werden nicht gesondert berücksichtigt. Da Daten zur Zahl der Radfahrenden fehlen, beschreibt die Prognose die erwartete Unfallhäufigkeit, nicht das persönliche Unfallrisiko.

## Fazit

Die Analyse zeigt zeitliche und regionale Unterschiede bei den registrierten Fahrradunfällen. Besonders viele Unfälle wurden in den Sommermonaten und am Nachmittag erfasst; zugleich unterscheidet sich der Anteil schwerer Unfälle zwischen den Regionen.

Die Prognose für 2026 ist eine explorative Schätzung und aufgrund der kurzen Zeitreihe mit Unsicherheit verbunden. Insgesamt beschreiben die Ergebnisse Muster in den registrierten Unfällen, erlauben aber weder direkte Aussagen über das individuelle Unfallrisiko noch sichere Schlussfolgerungen über Unfallursachen.

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

Die jährlichen Unfalldaten wie im Abschnitt [Jährliche Unfalldaten](#jährliche-unfalldaten) beschrieben herunterladen und im Ordner `data/` ablegen.

Die Excel-Datei mit dem Verwaltungsverzeichnis sowie die Einwohnerdateien für 2020 bis 2025 sind im Repository enthalten.

### 4. Notebook ausführen

1. Das Projekt in Visual Studio Code öffnen.
2. Die Datei `analyse.ipynb` öffnen.
3. Die virtuelle Umgebung `.venv` als Python-Kernel auswählen.
4. Den Kernel neu starten und alle Zellen der Reihe nach von oben nach unten ausführen.
5. Prüfen, ob alle Zellen ohne Fehler durchlaufen und die Diagramme korrekt erstellt werden.

## Projektstruktur

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

Die jährlichen Unfalldateien werden lokal im Ordner `data/` abgelegt und nicht mit dem Repository versioniert. Die Referenzdatei und die Einwohnerdateien sind dagegen im Repository enthalten.

## Einschränkungen

- Der Unfallatlas enthält Unfälle mit Personenschaden, nicht alle Verkehrsunfälle.
- Die Unfallkategorie richtet sich nach der schwersten Folge aller Beteiligten, nicht nur der Radfahrenden.
- Die absolute Zahl registrierter Unfälle entspricht nicht dem individuellen Unfallrisiko. Einwohnerbezogene Kennzahlen berücksichtigen nicht, wie häufig oder wie weit Rad gefahren wird.
- Die Einwohnerzahlen beruhen bis 2023 und ab 2024 auf unterschiedlichen Grundlagen (ab 2024 Zensus 2022). Kennzahlen je 100.000 Einwohner sind über diese Grenze hinweg nur eingeschränkt vergleichbar.
- Die Beteiligung weiterer Verkehrsteilnehmer kann sich zwischen den Kategorien überschneiden.
- Berlin und Hamburg sind in den Unfalldaten in Bezirke unterteilt und wurden für die Stadtvergleiche jeweils zusammengefasst. Insgesamt konnten 618 Unfälle (0,12 %) keiner Gemeinde zugeordnet werden.
- Die Ergebnisse beschreiben beobachtete Zusammenhänge und belegen keine Kausalität.
- Die Prognose für 2026 ist vorläufig und mit erheblicher Unsicherheit verbunden.

## Verwendete Technologien

- Python
- pandas
- Matplotlib
- statsmodels
- Jupyter Notebook
- uv
