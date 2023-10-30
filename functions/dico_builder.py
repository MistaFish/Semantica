import os
import openai
from dotenv import load_dotenv

class DicoBuilder:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        self.api_key = api_key
        openai.api_key = self.api_key
    
    def semantic_dico(self, reviews:str, nb_reviews:int, previous_dico: str = None):
      try:
          reviews_message={
              "role": "user",
              "content":reviews
            }

          if (previous_dico == None):
            model_gpt = "gpt-3.5-turbo"
            system_message = {
              "role": "system",
              "content": f"Tu es un expert en analyse sémantique et plus précisement d'avis en restauration. Tu vas aider en créant un dictionnaire sémantique.  Il doit être contruit avec des catégories générales et des sous-catégories. Il ne doit pas y avoir de redondance entre les sous-catégories. Dans ta réponse, tu ne rajoute aucune phrase de courstoisie, de conversation ou de Nota. Voici un exemple concret de format de réponse "" 1. : Personnel et service\n 1.1 : Courtoisie et disponibilit\u00e9 du personnel\n1.2 : Rapidit\u00e9 du service en caisse\n\n2. : Nourriture\n 2.1 : Qualité de la nourriture\n2.2 : Cuisson des viandes\n\n3. : Propreté\n 3.1 : Propreté générale du restaurant\n 3.2 : Propreté des Toilettes "". Il ne doit y avoir aucun doublon dans les catégories et sous-catégories. Les catégories et sous-catégories doivent rester générales pour que le user puisse analyser le sentiments des avis par sous-catégories. Une catégorie ne peut pas avoir une seul sous-catégories. Si tu en identifie, c'est que les sous-catégories peuvent être fusionnées avec d'autres sur un thème plus large. Tu ne peux pas créer une catégorie avec un sentiment. Suis ces étapes pour construire ta réponse à l'utilisateur : 1 : idéntifie les catégories et sous catégories abordées dans les commentaires. 2 : Attribue leur des nombres suivant cette forme CATEGORIE.SOUS-CATEGORIE (exemple 1.1, 1.2,2.1...) Tu va recevoir {nb_reviews} avis de mon restaurant (délimités avec des tags XML: <avis></avis>). Chaque avis précise le numéro de la personne qui l'a donné (exemple : ""P12 :"")",
            }
            user_message = {
              "role": "user",
              "content": f"A partir des {nb_reviews} avis que j'ai reçu concernant mon restaurant, crée un dictionnaire sémantique."
            }
          else:
            model_gpt = "gpt-3.5-turbo"
            system_message = {
              "role": "system",
              "content": f"Tu es un expert en analyse sémantique et plus précisement d'avis en restauration. Tu vas aider en enrichissant un dictionnaire sémantique. Il doit être contruit avec des catégories générales et des sous-catégories. Il ne doit pas y avoir de redondance entre les sous-catégories. Dans ta réponse, tu ne rajoute aucune phrase de courstoisie, de conversation ou de Nota. Les catégories et sous-catégories doivent rester généralistes (pas de sentiments en nom de sous-catégories). Une catégorie ne peut pas avoir une seul sous-catégories. Si tu en identifie, c'est que les sous-catégories peuvent être fusionnées avec d'autres sur un thème plus large. Tu ne peux pas créer une catégorie avec un sentiment. Suis ces étapes pour construire ta réponse à l'utilisateur : 1 : comprends le dictionnaire sémantique d'origine. 2 : idéntifie les catégories et sous catégories abordées dans les nouveaux commentaires. 3 : Harmonise ces catégories et sous catégories. Tu va recevoir {nb_reviews} avis supplémentaires de mon restaurant (délimités avec des tags XML: <avis></avis>).",
            }
            user_message = {
              "role": "user",
              "content": f"A partir des {nb_reviews} avis supplémentaires que j'ai reçu concernant mon restaurant, harmonise le dictionnaire sémantique existant: \n{previous_dico}.\nSi il n'y a pas de catégorie à rajouter n'en rajoute pas. Tu dois garder exactement le même format que celui que je t'envoie. Tu dois te limiter à 12 catégories et 50 sous-catégorie."
            }
            

          response_start_building_dico = openai.ChatCompletion.create(
              model=model_gpt,
              messages=[
                  system_message,
                  user_message,
                  reviews_message,
              ],
          )

          print(f"BATCH COMPLETED WITH REASON : {response_start_building_dico['choices'][0].finish_reason}")
          dico_seman = response_start_building_dico['choices'][0].message.content
          return dico_seman
      
      except Exception as e:
          print(f"An error occurred while building semantic dictionary: {e}")
          return previous_dico
    
    def harmonize_semantic_dico(self, dico_seman:str):
        system_message = {
          "role": "system",
          "content": f"Tu es un expert en analyse sémantique et plus précisement d'avis en restauration. Tu vas aider en harmonisant un dictionnaire sémantique déjà existant. Voici un exemple concret de format de réponse "" 1. : Personnel et service\n 1.1 : Courtoisie et disponibilit\u00e9 du personnel\n1.2 : Rapidit\u00e9 du service en caisse\n\n2. : Nourriture\n 2.1 : Qualité de la nourriture\n2.2 : Cuisson des viandes\n\n3. : Propreté\n 3.1 : Propreté générale du restaurant\n 3.2 : Propreté des Toilettes "". Je ne veux aucune phrase de politesse, de conversation, de nota ou de remarques. Je veux juste les catégories et sous-catégories."
        }
        user_message = {
    			"role": "user",
    			"content": "Voici un dictionnaire sémantique. Certaines catégories peuvent être regroupées. Harmonise aven un maximum de 10 catégories et de 50 sous-catégories."
				}
        dico_seman_message={
        	"role": "user",
          "content":dico_seman
				}
        
        response_enrich_dico = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                system_message,
                user_message,
                dico_seman_message,
            ]
        )
        print(f"BATCH COMPLETED WITH REASON : {response_enrich_dico['choices'][0].finish_reason}")
        dico_seman_harmonized = response_enrich_dico['choices'][0].message.content
        return dico_seman_harmonized