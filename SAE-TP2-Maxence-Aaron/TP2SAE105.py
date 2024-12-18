import csv
import matplotlib.pyplot as plt

file_path = 'RTE_2022.csv'

with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]

consommation = []
production_totale = []
part_renouvelable = []
mois_list = []

for row in data:
    try:
        consommation_val = float(row["Consommation"]) if row["Consommation"] else None
        production_fioul = float(row["Fioul"]) if row["Fioul"] else 0
        production_charbon = float(row["Charbon"]) if row["Charbon"] else 0
        production_gaz = float(row["Gaz"]) if row["Gaz"] else 0
        production_nucleaire = float(row["Nucleaire"]) if row["Nucleaire"] else 0
        production_eolien = float(row["Eolien"]) if row["Eolien"] else 0
        production_solaire = float(row["Solaire"]) if row["Solaire"] else 0
        production_hydraulique = float(row["Hydraulique"]) if row["Hydraulique"] else 0

        prod_totale = (
            production_fioul
            + production_charbon
            + production_gaz
            + production_nucleaire
            + production_eolien
            + production_solaire
            + production_hydraulique
        )

        prod_renouvelable = production_eolien + production_solaire + production_hydraulique

        if row["Date"]:
            mois = int(row["Date"].split("-")[1])
        else:
            mois = None

        if consommation_val is not None and mois is not None:
            consommation.append(consommation_val)
            production_totale.append(prod_totale)
            part_renouvelable.append((prod_renouvelable / prod_totale) * 100 if prod_totale > 0 else 0)
            mois_list.append(mois)
    except Exception as e:
        continue

consommation_par_mois = {}
for i in range(len(mois_list)):
    mois = mois_list[i]
    if mois not in consommation_par_mois:
        consommation_par_mois[mois] = []
    consommation_par_mois[mois].append(consommation[i])

moyenne_consommation_par_mois = {
    mois: sum(valeurs) / len(valeurs) for mois, valeurs in consommation_par_mois.items()
}

mois_labels = [
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
]
x_mois = list(sorted(moyenne_consommation_par_mois.keys()))
y_consommation = [moyenne_consommation_par_mois[mois] for mois in x_mois]

plt.figure(figsize=(10, 6))
plt.plot(x_mois, y_consommation, marker='o', label='Consommation moyenne')
#xsticks     ticks permet de mettre une ordonée pour quache point, donc x. Labels permet de remplacer l'échelle chiffrée par autre chose, ici, les mois de l'année. Rotation permet d'incliner les legendes donc, dans ce graphique, le nom des mois est incliné de 45°
plt.xticks(ticks=x_mois, labels=[mois_labels[m-1] for m in x_mois], rotation=45)
plt.title("Consommation moyenne mensuelle en 2022")
plt.xlabel("Mois")
plt.ylabel("Consommation (MW)")
plt.grid()
plt.legend()
#Ajuste la taille des légendes pour ne pas quelles débordent automatiquement
plt.tight_layout()
plt.show()

moyenne_part_renouvelable = sum(part_renouvelable) / len(part_renouvelable)
part_fossiles_nucleaire = 100 - moyenne_part_renouvelable

labels = ["Renouvelables", "Fossiles + Nucléaire"]
parts = [moyenne_part_renouvelable, part_fossiles_nucleaire]

plt.figure(figsize=(8, 8))
plt.pie(parts, labels=labels, autopct='%1.1f%%', startangle=90, colors=["#8dd3c7", "#fb8072"])
plt.title("Part des énergies renouvelables en 2022")
plt.show()
