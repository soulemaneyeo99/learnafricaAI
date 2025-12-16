import google.generativeai as genai
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)

# Configuration du modèle
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-flash-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

async def generate_response(prompt: str, context: str = "") -> str:
    """
    Génère une réponse simple à partir d'un prompt via Gemini, avec contexte optionnel.
    """
    full_prompt = prompt
    if context:
        full_prompt = f"Tu es un tuteur intelligent pour LearnAfrica AI.\n\nContexte:\n{context}\n\nQuestion de l'apprenant: {prompt}"

    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        return "Désolé, je ne peux pas répondre pour le moment. Erreur technique."

async def generate_quiz_for_topic(topic: str, num_questions: int = 5, context: str = "") -> str:
    """
    Génère un quiz sur un sujet donné, avec contexte optionnel (contenu du cours).
    """
    base_prompt = f"Génère un quiz de {num_questions} questions à choix multiples sur le sujet : {topic}."
    
    if context:
        base_prompt += f"\n\nUtilise EXCLUSIVEMENT le contenu du cours suivant pour générer les questions et réponses :\n{context}"
    
    prompt = (
        f"{base_prompt}\n"
        "Le format de sortie DOIT être un JSON valide sans markdown, respectant cette structure : "
        "{ \"questions\": [ { \"question\": \"...\", \"options\": [\"...\", \"...\"], \"answer\": 0 } ] }"
    )
    # Note: On pourra utiliser response_mime_type="application/json" avec gemini-1.5-flash dans le futur
    # pour garantir le JSON. Pour l'instant on force via le prompt.
    
    try:
        # Pour le quiz, on peut vouloir forcer le JSON si le modèle le supporte via config locale
        json_config = generation_config.copy()
        # json_config["response_mime_type"] = "application/json" 
        
        response = model.generate_content(prompt, generation_config=json_config)
        return response.text
    except Exception as e:
        logger.error(f"Error generating quiz: {e}")
        return "{}"
