from functions.dico_builder import DicoBuilder
from utils.csv_manager.csv_extractor import CSVExtractor
from utils.csv_manager.csv_creating_dico_seman import create_csv_dico_semantic
from utils.csv_manager.csv_creating_categorized_review import create_csv_categorize_review_by_categories
from utils.csv_manager.csv_creating_enriched_data_source import create_csv_enriched_data_source
from utils.constants.title import title
from utils.constants.loading_indicator import LoadingBar
import json

title()
def get_total_line_count(filename: str) -> int:
    with open(filename, "r") as file:
        return sum(1 for _ in file)

dico_builder = DicoBuilder()
filename = "datasource.csv"
total_line_count = get_total_line_count(filename)
extractor = CSVExtractor(filename, total_line_count)
dico_enriched = None

total_batches = 4
print("\033[95m********************************************************************\033[0m")
print("\033[92m___________________CONSTRUCTION DICTIONNAIRE________________________\033[0m")
loading_bar = LoadingBar(total_batches)
# # i = 0
# # while True:
# #     batch = extractor.extract_comments_in_batches()
# #     if extractor.eof is True:
# #         break
# #     dico_enriched = dico_builder.semantic_dico(
# #     		extractor.extract_comments_in_batches().get_comments(),
# #     		40,
# #     		dico_enriched
# #     )
# #     i = i + 1
# #     print(f"Batch : {i}, batchSize:{batch.batch_size}")

for i in range (total_batches) :
    batch = extractor.extract_comments_in_batches()
    if extractor.eof is True:
      break
    dico_enriched = dico_builder.semantic_dico(
	  	extractor.extract_comments_in_batches().get_comments(),
	  	batch.batch_size,
	  	dico_enriched
	  )
    # print(f"Batch : {i}, batchSize:{batch.batch_size}")
    loading_bar.update()
loading_bar.close() 
print(dico_enriched)
# dico_done = dico_builder.harmonize_semantic_dico(dico_enriched)

create_csv_dico_semantic(dico_enriched)

print("\033[91m_________________FIN CONSTRUCTION DICTIONNAIRE______________________\033[0m")
print("\n\033[95m********************************************************************\033[0m")
print("\n\033[92m________________DEBUT AFFECTATION DES PERSONNES_____________________\033[0m")
# JSON A OBTENIR AVEC CHAT GPT

create_csv_categorize_review_by_categories()

print("\033[91m_________________FIN AFFECTATION DES PERSONNES______________________\033[0m")      
print("\n\033[95m********************************************************************\033[0m")
print("\n\033[92m________________DEBUT ENRICHISSEMENT DATASOURCE_____________________\033[0m")

create_csv_enriched_data_source()

print("\033[91m_________________FIN ENRICHISSEMENT DATASOURCE______________________\033[0m")      
print("\n\033[95m********************************************************************\033[0m")

