import json
import openai
from utils.batch import Batch
from utils.categorize.class_dico_manager import Dico_manager
from utils.constants.loading_indicator import LoadingBar
from utils.csv_manager.csv_extractor import CSVExtractor, get_total_line_count

filename = "/Users/mistafish/Desktop/FuckingDev/Présence/Semantica/datasource.csv"

def enrich_user_request(dico_manager: Dico_manager, batch: Batch) -> str:
  system_message = {
      "role": "system",
        "content": (
          "Tu es un expert en analyse sémantique et plus précisement d'avis en restauration. "
          "Tu vas aider en identifiant des avis basé sur un dictionnaire sémantique. "
          "Pour chaque avis : "
          "Tu dois identifier les catégories et sous catégories abordées dans l'avis. "
          "Je veux un json comme format de réponse."
      ),
  }
  user_message = {
      "role": "user",
      "content": (
          "Tu as a disposition un dictionnaire sémantique. "
          "Tu as également des avis de clients. "
          "Dans ta réponse, tu ne rajoutes aucune phrase de courstoisie, de conversation ou de Nota. "
          "Suis ces étapes pour construire ta réponse à l'utilisateur : "
          "Avant tout : comprends le dictionnaire sémantique "
          "Pour chaque avis : "
          "1 : Identifie les catégories et sous catégories abordées dans l'avis. "
          "2 : détermine si l'avis est satisfait ou instatisfait. "
          f"Tu vas recevoir {batch.batch_size} avis de restaurants (délimités avec des tags XML: <avis></avis>). "
          "Le format de réponse attendu est un objet JSON où chaque clé est l'ID de l'avis (P1, P2, etc.), "
          "et la valeur est un objet contenant des paires clé-valeur pour chaque ésous-catégorie identifiée, "
          "avec 'S' si l'avis est satisfaisant ou 'NS' si l'avis est non satisfaisant pour cette catégorie/sous-catégorie. "
          "Exemple : { 'PX': { '1.1': 'S', '1.2': 'S', '2.1': 'NS' }, 'PY': {...}, ... }"
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

  # print(messages)
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      max_tokens=1500,
      messages=messages,
  )
  print(f"BATCH COMPLETED WITH REASON : {response['choices'][0].finish_reason}")
  # print (response['choices'][0].message.content)
  return response['choices'][0].message.content


def enrichment_builder():
  dico_manager = Dico_manager()
  total_batches = 10
  loading_bar = LoadingBar(total_batches)

  total_line_count = get_total_line_count(filename)
  extractor = CSVExtractor(filename, total_line_count)
  for i in range(total_batches):
    batch = extractor.extract_comments_in_batches()
    response: str = enrich_user_request(dico_manager, batch)
    dico_manager.process_reviews(response)
    loading_bar.update()
  loading_bar.close() 

  dico_manager.write_to_enriched_reviews('/Users/mistafish/Desktop/FuckingDev/Présence/Semantica/outputs/enriched_reviews.csv')