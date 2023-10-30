import csv

def create_csv_dico_semantic(data:str):
    lignes = data.strip().split('\n')
    donnees_csv = []
    categorie_courante = None
    num_categorie_courante = None

    for ligne in lignes:
        if not ligne.strip():
            continue

        # Find the first space, which separates the category/sub-category number from the name
        if ligne[0] == " ":
            first_space_temp = ligne.find(' ')
            first_space = ligne.find(' ', first_space_temp + 1)
        else :
            first_space = ligne.find(' ')

        # Extract the first part and remaining part based on the first space position
        first_part = ligne[:first_space]
        first_dot = ligne.find('.')      
        remaining = ligne[first_space+1:]

        if '.' in first_part and (first_part[0].isdigit() or first_part[1].isdigit()):
            if ligne[0].isdigit() and first_part.count('.') == 1 and not ligne[first_dot+1].isdigit() :
                # This is a main category
                num_categorie_courante, categorie_courante = first_part, remaining
            else:
                # This is a sub-category
                num_sous_categorie, nom_sous_categorie = first_part, remaining
                donnees_csv.append([num_categorie_courante, categorie_courante, num_sous_categorie, nom_sous_categorie])

    # Write data to CSV
    with open('./outputs/dico_semantique.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['num_categorie', 'nom_categorie', 'num_sous_categorie', 'nom_sous_categorie'])
        writer.writerows(donnees_csv)
