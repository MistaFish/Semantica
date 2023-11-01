import openai
from utils.batch import Batch
from utils.categorize.class_dico_manager import Dico_manager
from utils.constants.loading_indicator import LoadingBar
from utils.constants.params import GET_ENRICHMENT_CONTENT
from utils.csv_manager.csv_extractor import CSVExtractor, get_total_line_count
from utils.constants.params import CALL_API

filename = "datasource.csv"


def enrich_user_request(dico_manager: Dico_manager, batch: Batch) -> str:
  system_message = {
      "role": "system",
        "content": (
          "Tu es un expert en analyse sémantique et plus précisement d'avis en restauration. "
          "Tu vas aider en identifiant des avis basé sur un dictionnaire sémantique qui t'ai envoyé. "
          "Pour chaque avis : "
          "Tu dois identifier les sous-catégories abordées dans l'avis. "
          "Le format de réponse attendu est un objet JSON où chaque clé est l'ID de l'avis (P1, P2, etc.), "
          "et la valeur est un objet contenant des paires clé-valeur pour chaque sous-catégorie identifiée, "
          "avec 'S' si l'avis est satisfaisant ou 'NS' si l'avis est non satisfaisant pour cette sous-catégorie. "
          "Exemple : { ""PX"": { ""1.1"": ""S"", ""1.2"": ""S"", ""2.1"": ""NS"" }, ""PY"": {...}, ... }"
          "Ta réponse contiendra uniquement l'objet."
          "Tu ne dois pas inventer de nouvelles sous-catégories. Utilise seulement celles du dictionnaire initial."
          "Suis ces étapes pour construire ta réponse à l'utilisateur : "
          "1 : comprends le dictionnaire sémantique en intégrant les catégories et sous-catégories."
          "2 : Pour chaque avis, identifie les sous-catégories abordées dans l'avis. "
          "3 : détermine si l'avis est satisfait ou instatisfait. "
      ),
  }
  user_message = {
      "role": "user",
      "content": (
          "Tu as a disposition un dictionnaire sémantique. "
          "Tu as également des avis de clients. "
          f"Tu vas recevoir {batch.batch_size} avis de restaurants (délimités avec des tags XML: <avis></avis>). "
          "Analyse les avis et répond moi avec l'objet JSON demandé."

      ),
  }
  dico_seman_message={
      "role": "user",
      "content": dico_manager.get_categories_prompt()
}
  reviews_message={
      "role": "user",
      "content": batch.get_comments()
  }

  messages=[
          system_message,
          user_message,
          dico_seman_message,
          reviews_message,
      ]

  if GET_ENRICHMENT_CONTENT:
    print(messages)
    return
  else:
    if (CALL_API):
      response = openai.ChatCompletion.create(
          model="gpt-4",
          max_tokens=1500,
          messages=messages,
      )
      print(f"BATCH COMPLETED WITH REASON : {response['choices'][0].finish_reason}")
  print(f'RESPONSE OPEN AI : {response}')
  return response['choices'][0].message.content


def enrichment_builder():
  dico_manager = Dico_manager()
  total_batches = 47
  total_line_count = get_total_line_count(filename)
  extractor = CSVExtractor(filename, total_line_count, 1040)
  loading_bar = LoadingBar(total_batches)
  
  retry : bool = False
  while True:
    if retry is False :
      batch = extractor.extract_comments_in_batches()
    if extractor.eof is True:
      break
    retry = False
    response: str = enrich_user_request(dico_manager, batch)
    if (GET_ENRICHMENT_CONTENT):
      return
    retry = dico_manager.process_reviews(response)
    if retry is True :
      continue

    dico_manager.write_to_enriched_reviews('outputs/enriched_reviews.csv')
    loading_bar.update()
  loading_bar.close() 
