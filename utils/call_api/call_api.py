import openai
import dotenv
import os

# Assurez-vous de remplacer 'your-api-key-here' par votre clé API
dotenv.load_dotenv()

api_key: str | None = os.getenv("OPENAI_API_KEY")

if api_key is None:
    print("No API key found. Please create a .env file with your API key.")
    exit(1)

openai.api_key = api_key


def create_semantic_dictionnary(reviews: list[str]):
    print("Creating semantic dictionnary...")
    print(reviews[0])
    openai.ChatCompletion.create(
        
    )
