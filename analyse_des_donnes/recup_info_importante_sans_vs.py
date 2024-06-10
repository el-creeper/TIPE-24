import pandas as pd

# Charger le fichier CSV dans un DataFrame
data = pd.read_csv("analyse_des_donnes/donnes_a_traiter.csv")

# Supprimer les colonnes "moy_vs" et "vs"
data = data.drop(columns=["moy_vs", "vs"])

# Enregistrer le nouveau DataFrame dans un fichier CSV
data.to_csv("analyse_des_donnes/donnes_a_traiter_sans_vs.csv", index=False)
