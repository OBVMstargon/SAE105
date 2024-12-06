import csv
import matplotlib.pyplot as plt

communes_immediates = ["Appoigny", "Auxerre", "Monéteau", "Perrigny", "Saint-Georges-sur-Baulche"]
communes_totales = [
    "Appoigny", "Augy", "Auxerre", "Bleigny-le-Carreau", "Branches", "Champs-sur-Yonne", "Charbuy",
    "Chevannes", "Chitry", "Coulanges-la-Vineuse", "Escamps", "Escolives Sainte-Camille", "Gurgy",
    "Gy-l’Évêque", "Irancy", "Jussy", "Lindry", "Monéteau", "Montigny-la-Resle", "Perrigny", "Quenne",
    "Saint-Bris-le-Vineux", "Saint-Georges-sur-Baulche", "Vallan", "Venoy", "Villefargeau",
    "Villeneuve-Saint-Salves", "Vincelles", "Vincelottes"
]

files = {
    2008: {"file": "donnees_2008.csv", "delimiter": ",", "name_column": 6, "population_column": 7},
    2016: {"file": "donnees_2016.csv", "delimiter": ",", "name_column": 6, "population_column": 7},
    2021: {"file": "donnees_2021.csv", "delimiter": ";", "use_metadata": True},
    2023: {"file": "donnees_2023.csv", "delimiter": ";", "name_column": 6, "population_column": 8},
}
metadata_file = "metadonnees_communes.csv"

codes_to_communes = {}
try:
    with open(metadata_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            codes_to_communes[row[2].strip()] = row[3].strip()
except FileNotFoundError:
    print(f"Le fichier des métadonnées est introuvable : {metadata_file}")

population_data = []

for year, details in files.items():
    if not details["file"]:
        print(f"Fichier introuvable : {details['file']}")
        continue
    with open(details["file"], newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=details["delimiter"])
        if year != 2021:
            next(reader)
        for row in reader:
            try:
                if "use_metadata" in details and details["use_metadata"]:
                    code_commune = row[2].strip()
                    population = int(row[3].strip())
                    commune = codes_to_communes.get(code_commune, None)
                else:
                    commune = row[details["name_column"]].strip()
                    population = int(row[details["population_column"]].strip())
                
                if commune and (commune in communes_immediates or commune in communes_totales):
                    population_data.append({"Commune": commune, "Population": population, "Année": year})
            except (ValueError, IndexError):
                continue

resultats = {"Auxerre": {}, "Agglomération Immédiate": {}, "Agglomération Totale": {}}

for annee in {row["Année"] for row in population_data}:
    resultats["Auxerre"][annee] = sum(
        row["Population"] for row in population_data if row["Commune"] == "Auxerre" and row["Année"] == annee
    )
    resultats["Agglomération Immédiate"][annee] = sum(
        row["Population"] for row in population_data if row["Commune"] in communes_immediates and row["Année"] == annee
    )
    resultats["Agglomération Totale"][annee] = sum(
        row["Population"] for row in population_data if row["Commune"] in communes_totales and row["Année"] == annee
    )

for categorie, data in resultats.items():
    annees = sorted(data.keys())
    populations = [data[annee] for annee in annees]
    plt.plot(annees, populations, marker='o', label=categorie)

plt.xlabel("Année")
plt.ylabel("Population")
plt.title("Évolution de la population")
plt.legend()
plt.grid(True)
plt.show()
