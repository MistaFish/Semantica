import os
import openai
from dotenv import load_dotenv


class DicoBuilder:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        self.api_key = api_key
        openai.api_key = self.api_key

    def build_semantic_dico(self, reviews:str, nb_reviews:int):
        system_message = {
          "role": "system",
          "content": f"Tu es un expert en analyse sémantique et plus précisement d'avis en restauration. Tu vas aider en créant un dictionnaire sémantique.  Il doit être contruit avec des catégories générales et des sous-catégories. Le rendu attendu est d'avoir des catégories et sous-catégories sémantique. Il ne doit pas y avoir de redondance entre les sous-catégories.Dans ta réponse, tu ne rajoute aucune phrase de courstoisie, de conversation ou de Nota. Voici un exemple concret de format de réponse "" 1. : Personnel et service\n 1.1 : Courtoisie et disponibilit\u00e9 du personnel\n1.2 : Rapidit\u00e9 du service en caisse\n\n2. : Nourriture\n 2.1 : Qualité de la nourriture\n2.2 : Cuisson des viandes\n\n3. : Propreté\n 3.1 : Propreté générale du restaurant\n 3.2 : Propreté des Toilettes "". Il ne doit y avoir aucun doublon dans les catégories et sous-catégories. Les catégories et sous-catégories doivent rester générales pour que le user puisse analyser le sentiments des avis par sous-catégories. Une catégorie ne peut pas avoir une seul sous-catégories. Si tu en identifie, c'est que les sous-catégories peuvent être fusionnées avec d'autres sur un thème plus large. Tu ne peux pas créer une catégorie avec un sentiment. Suis ces étapes pour construire ta réponse à l'utilisateur : 1 : idéntifie les catégories et sous catégories abordées dans les commentaires. 2 : Attribue leur des nombres suivant cette forme CATEGORIE.SOUS-CATEGORIE (exemple 1.1, 1.2,2.1...) Tu va recevoir {nb_reviews} avis de mon restaurant (délimités avec des tags XML: <avis></avis>). Chaque avis précise le numéro de la personne qui l'a donné (exemple : ""P12 :"")",
        }
        user_message = {
    			"role": "user",
    			"content": f"A partir des {nb_reviews} avis que j'ai reçu concernant mon restaurant, crée un dictionnaire sémantique."
				}
        reviews_message={
        	"role": "user",
          "content":reviews
				}
        
        response_start_building_dico = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                system_message,
                user_message,
                reviews_message,
            ]
        )
        dico_seman = response_start_building_dico['choices'][0].message.content
        return dico_seman
    
    def enrich_semantic_dico(self, reviews:str, previous_dico:str, nb_reviews:int):
        system_message = {
          "role": "system",
          "content": f"Tu es un expert en analyse sémantique et plus précisement d'avis en restauration. Tu vas aider en enrichissant un dictionnaire sémantique.  Il doit être contruit avec des catégories générales et des sous-catégories. Il ne doit pas y avoir de redondance entre les sous-catégories. Il ne doit pas y avoir de redondance entre les sous-catégories. Le rendu attendu est d'avoir des catégories et sous-catégories sémantique. Dans ta réponse, tu ne rajoute aucune phrase de courstoisie, de conversation ou de Nota. Voici un exemple concret de format de réponse "" 1. : Personnel et service\n 1.1 : Courtoisie et disponibilit\u00e9 du personnel\n1.2 : Rapidit\u00e9 du service en caisse\n\n2. : Nourriture\n 2.1 : Qualité de la nourriture\n2.2 : Cuisson des viandes\n\n3. : Propreté\n 3.1 : Propreté générale du restaurant\n 3.2 : Propreté des Toilettes "". Il ne doit y avoir aucun doublon dans les catégories et sous-catégories. Les catégories et sous-catégories doivent rester générales pour que le user puisse analyser le sentiments des avis par sous-catégories. Une catégorie ne peut pas avoir une seul sous-catégories. Si tu en identifie, c'est que les sous-catégories peuvent être fusionnées avec d'autres sur un thème plus large. Tu ne peux pas créer une catégorie avec un sentiment. Suis ces étapes pour construire ta réponse à l'utilisateur : 1 : comprends le dictionnaire sémantique d'origine. 2 : idéntifie les catégories et sous catégories abordées dans les nouveaux commentaires. 3 : Harmonise ces catégories et sous catégories. Attribue leur des nombres suivant cette forme CATEGORIE.SOUS-CATEGORIE (exemple 1.1, 1.2,2.1...) Tu va recevoir {nb_reviews} avis supplémentaires de mon restaurant (délimités avec des tags XML: <avis></avis>). Chaque avis précise le numéro de la personne qui l'a donné (exemple : ""P12 :"").",
        }
        user_message = {
    			"role": "user",
    			"content": f"A partir des {nb_reviews} avis supplémentaires que j'ai reçu concernant mon restaurant, complète le dictionnaire sémantique existant.\n{previous_dico}. Si il n'y a pas de catégorie à rajouter n'en rajoute pas. Si tu vois des redondence, tu peux regrouper et harmoniser les catégories et sous-catégories. Je veux uniquement que tu renvoies le dictionnaire sémantique à jour. Aucun phrase de conversation, de politesse, de note ou de warnings"
				}
        reviews_message={
        	"role": "user",
          "content":reviews
				}
        
        response_enrich_dico = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                system_message,
                user_message,
                reviews_message,
            ]
        )
        dico_seman_enriched = response_enrich_dico['choices'][0].message.content
        return dico_seman_enriched
    
    def harmonize_semantic_dico(self, dico_seman:str):
        system_message = {
          "role": "system",
          "content": f"Tu es un expert en analyse sémantique et plus précisement d'avis en restauration. Tu vas aider en harmonisant un dictionnaire sémantique déjà existant. Voici un exemple concret de format de réponse "" 1. : Personnel et service\n 1.1 : Courtoisie et disponibilit\u00e9 du personnel\n1.2 : Rapidit\u00e9 du service en caisse\n\n2. : Nourriture\n 2.1 : Qualité de la nourriture\n2.2 : Cuisson des viandes\n\n3. : Propreté\n 3.1 : Propreté générale du restaurant\n 3.2 : Propreté des Toilettes "". Je ne veux aucune phrase de politesse, de conversation, de nota ou de remarques. Je veux juste les catégories et sous-catégories."
        }
        user_message = {
    			"role": "user",
    			"content": "Voici un dictionnaire sémantique que j'ai créer en me basant sur des avis que j'ai reçu sur mon restaurant. Certaines catégories peuvent être regroupées. Je veux que les catégories et sous-catégories restent généraliste dans l'analyse de satisfaction d'un restaurant. Si une catégorie possède une seul sous-catégorie, je veux que c'est sous-catégories soient regroupées en ""Autres Observations"". Harmonise le en suivant mes indications."
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
        print(response_enrich_dico)
        dico_seman_harmonized = response_enrich_dico['choices'][0].message.content
        return dico_seman_harmonized
