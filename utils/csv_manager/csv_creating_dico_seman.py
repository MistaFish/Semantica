import csv

def create_csv_dico_semantic(data:str) : 
	lignes = data.strip().split('\n')
	donnees_csv = []
	categorie_courante = None
	num_categorie_courante = None

	# Iterate through each line in the data
	# Ignorer les lignes vides

	for ligne in lignes:
			# Ignorer les lignes vides
			if not ligne.strip():
					continue
			if len(ligne) > 1 and ligne[0].isdigit() and ligne[1] == '.' and not ligne[2].isdigit():
					# C'est une catégorie
					num_categorie_courante, categorie_courante = ligne.split(' ', 1)

			elif (len(ligne) > 2 and ligne[2] == '.') or (len(ligne) > 1 and ligne[0].isdigit() and ligne[1] == '.' and ligne[2].isdigit()):
					# C'est une sous-catégorie
					num_sous_categorie, nom_sous_categorie = ligne.strip().split(' ', 1)
					donnees_csv.append([num_categorie_courante, categorie_courante, num_sous_categorie, nom_sous_categorie])

	# Écrire les données dans un fichier CSV
	with open('./outputs/dico_semantique.csv', mode='w', newline='', encoding='utf-8') as file:
			writer = csv.writer(file)
			writer.writerow(['num_categorie', 'nom_categorie', 'num_sous_categorie', 'nom_sous_categorie'])  # Écrire l'en-tête
			writer.writerows(donnees_csv)  # Écrire les données