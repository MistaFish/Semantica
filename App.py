from functions.dico_builder import DicoBuilder
from functions.enrichment_builder import enrichment_builder
from utils.constants.params import DICO_SEMANTIC, ENRICHMENT, DEBUG, BATCH, HARMONIZE_SEMANTIC
from utils.csv_manager.csv_extractor import CSVExtractor, get_total_line_count
from utils.csv_manager.csv_creating_dico_seman import create_csv_dico_semantic
from utils.constants.loading_indicator import LoadingBar
from utils.constants.title import title
from utils.constants.footer import footer
import time


title()

start_time = time.time()

dico_builder = DicoBuilder()
filename = "datasource.csv"
total_line_count = get_total_line_count(filename)
extractor = CSVExtractor(filename, total_line_count)
dico_enriched = None

if DICO_SEMANTIC:
  print("\033[195m********************************************************************\033[0m")
  print("\033[92m___________________CONSTRUCTION DICTIONNAIRE________________________\033[0m")
  total_batches = 5
  loading_bar = LoadingBar(total_batches)
  if (BATCH):
    total_reviews = 0
    for i in range (total_batches) :
        batch = extractor.extract_comments_in_batches()
        if extractor.eof is True:
          break
        total_reviews += batch.batch_size
        dico_enriched = dico_builder.semantic_dico(
          extractor.extract_comments_in_batches().get_comments(),
          batch.batch_size,
          dico_enriched
        )
        loading_bar.update()
    print(f"\033[92m ====> TOTAL REVIEWS : {total_reviews}\033[0m")
  else:
    i = 0
    while True:
        batch = extractor.extract_comments_in_batches()
        if extractor.eof is True:
            break
        dico_enriched = dico_builder.semantic_dico(
            extractor.extract_comments_in_batches().get_comments(),
            40,
            dico_enriched
        )
        i = i + 1
  
  print(dico_enriched)
    
  if HARMONIZE_SEMANTIC:
    print("\033[92m ====> HARMONISATION DU DICTIONNAIRE\033[0m")
    dico_done = dico_builder.harmonize_semantic_dico(dico_enriched)
    if (DEBUG):
      print(dico_done)

  loading_bar.close()

  create_csv_dico_semantic(dico_enriched)

  print("\033[91m_________________FIN CONSTRUCTION DICTIONNAIRE______________________\033[0m")
  print("\n\033[95m********************************************************************\033[0m")

if (ENRICHMENT):
  print("\n\033[92m___________________DEBUT ANALYSE DES REVIEWS________________________\033[0m")
  enrichment_builder()
  print("\033[91m____________________FIN ANALYSE DES REVIEWS_________________________\033[0m")
  print("\033[95m********************************************************************\033[0m")

end_time = time.time()
elapsed_time_seconds = end_time - start_time
elapsed_time_minutes = elapsed_time_seconds // 60
elapsed_time_remaining_seconds = elapsed_time_seconds % 60
print(f"\033[92m ====> FIN DU TRAVAIL EN : {elapsed_time_minutes:.0f}min : {elapsed_time_remaining_seconds:.2f}sec\033[0m")

footer()