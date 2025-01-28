import pandas as pd
import matplotlib.pyplot as plt

# Charger les données
file_path = r"C:\Users\erag9\Desktop\IUT\TP\Python\SAE105\SH_TN_metropole\SAE105\SH_MTN002705001.csv"

data = pd.read_csv(file_path, sep=';', comment='#')

# Convertir la colonne YYYYMM en format date
data['YYYYMM'] = pd.to_datetime(data['YYYYMM'], format='%Y%m')

# Filtrer les données homogénéisées (Q_HOM = 1)
data = data[data['Q_HOM'] == 1]

# Définir un seuil pour les mois froids (par exemple, -5°C)
seuil_froid = -5

# Identifier les mois froids
mois_froids = data[data['VALEUR'] < seuil_froid]

# Afficher les résultats
print("Mois exceptionnellement froids :")
print(mois_froids[['YYYYMM', 'VALEUR']])

# Tracer un graphique des mois les plus froids
plt.figure(figsize=(10, 6))
plt.bar(mois_froids['YYYYMM'].dt.strftime('%Y-%m'), mois_froids['VALEUR'], color='blue')
plt.title('Mois Exceptionnellement Froids (Température < -5°C)', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Température Minimale Moyenne (°C)', fontsize=14)
plt.xticks(rotation=45, fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Afficher le graphique
plt.show()
