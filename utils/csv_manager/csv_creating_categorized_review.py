import csv

# Étape 1: Lire le premier CSV et extraire les noms de sous-catégories
def create_csv_categorize_review_by_categories(satisfaction_data:any):
    sous_categories = []
    num_to_full = {}  # This will hold the mapping
    with open('./outputs/dico_semantique.csv', mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            sous_categorie = f"{row['num_sous_categorie']} - {row['nom_sous_categorie']}"
            sous_categories.append(sous_categorie)
            num_to_full[row['num_sous_categorie']] = sous_categorie  # Store the mapping

    # Étape 2: Créer un second CSV avec ces noms de sous-catégories comme en-têtes de colonnes
    with open('./outputs/enriched_reviews.csv', mode='w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['ID_personne'] + sous_categories
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()

    # Exemple de données (à remplacer par les vraies données)

    # Créer un dictionnaire pour stocker les données de chaque personne
    persons_data = {}

    # Étape 3: Remplir les données de chaque personne
    for sub_cat, values in satisfaction_data.items():
        full_sub_cat = num_to_full.get(sub_cat)  # Convert to full name
        for s_or_ns, persons in values.items():
            for person in persons:
                if person not in persons_data:
                    persons_data[person] = {}
                persons_data[person][full_sub_cat] = s_or_ns  # Use the full name as key

    # Écrire les nouvelles lignes dans le fichier CSV
    with open('./outputs/enriched_reviews.csv', mode='a', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for person, values in persons_data.items():
            row = {'ID_personne': person}
            for sub_cat in fieldnames[1:]:
                row[sub_cat] = values.get(sub_cat, 'PDC')  # Use the full name as key
            csvwriter.writerow(row)

    # Étape 4: Sort the CSV file by ID_personne
    # Read the CSV into a list of dictionaries
    rows = []
    with open('./outputs/enriched_reviews.csv', mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            rows.append(row)

    # Sort the list of dictionaries by the 'ID_personne' field
    sorted_rows = sorted(rows, key=lambda x: int(x['ID_personne'][1:]))

    # Write the sorted list of dictionaries back to the same CSV file
    with open('./outputs/enriched_reviews.csv', mode='w', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        for row in sorted_rows:
            csvwriter.writerow(row)
    