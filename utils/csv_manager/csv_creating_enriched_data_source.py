import pandas as pd

def create_csv_enriched_data_source():
	# Charger les données à pazrtir des fichiers CSV
	data_source = pd.read_csv("./datasource.csv")
	enriched_reviews = pd.read_csv("./outputs/enriched_reviews.csv")

	# Enrichir data_source avec les données de enriched_reviews
	for index, row in enriched_reviews.iterrows():
			line_number = int(row['ID_personne'][1:]) - 1  # Convertir 'P1' en 0, 'P2' en 1, etc.
			if line_number < len(data_source):
					for col in enriched_reviews.columns[1:]:
							data_source.at[line_number, col] = row[col]

	# Sauvegarder le DataFrame enrichi dans un nouveau fichier CSV
	data_source.to_csv("./outputs/data_source_enriched.csv", index=False)
