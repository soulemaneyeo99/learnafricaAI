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
    Génère une réponse pédagogique et empathique via Gemini.
    """
    if context:
        full_prompt = f"""
        Tu es un tuteur personnel intelligent pour LearnAfrica AI.
        Ton rôle est d'aider l'étudiant à comprendre le cours, en étant encourageant, clair et concis.
        
        CONTEXTE DU COURS :
        {context}
        
        Question de l'apprenant : {prompt}
        
        Réponds en utilisant le contexte ci-dessus. Si la réponse n'est pas dans le contexte, dis-le poliment et propose d'élargir la recherche (tes connaissances générales).
        Sois structuré (utilise des listes si nécessaire).
        """
    else:
        full_prompt = f"""
        Tu es un tuteur personnel intelligent pour LearnAfrica AI.
        Question de l'apprenant : {prompt}
        Réponds de manière pédagogique et encourageante.
        """

    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        return "Désolé, je ne peux pas répondre pour le moment. Erreur technique."

async def generate_quiz_for_topic(topic: str, num_questions: int = 5, context: str = "") -> str:
    """
    Génère un quiz professionnel au format JSON strict sur un sujet donné.
    Utilise le mode JSON natif de Gemini 1.5 Flash.
    """
    
    # Prompt optimisé pour la qualité pédagogique
    prompt = f"""
    Tu es un expert pédagogique et tuteur pour LearnAfrica AI.
    Ta tâche est de créer un quiz d'évaluation précis et pertinent.
    
    Sujet : {topic}
    Nombre de questions : {num_questions}
    
    Instructions Pédagogiques :
    1. Les questions doivent être claires, sans ambiguïté.
    2. Les réponses fausses (distracteurs) doivent être plausibles mais clairement incorrectes.
    3. Le niveau de difficulté doit être adapté à un apprenant motivé.
    """

    if context:
        prompt += f"""
        
        CONTEXTE STRICT DU COURS :
        Utilise EXCLUSIVEMENT les informations fournies ci-dessous pour formuler tes questions et réponses.
        Si l'information n'est pas dans le contexte, ne l'invente pas.
        ---
        {context}
        ---
        """

    # Schéma JSON attendu (documentation pour le modèle)
    prompt += """
    
    Format de sortie attendu (JSON) :
    {
      "questions": [
        {
          "question": "Texte de la question",
          "options": ["Option A", "Option B", "Option C", "Option D"],
          "answer": 0, // Index de la bonne réponse (0 pour A, 1 pour B, etc.)
          "explanation": "Brève explication de la bonne réponse"
        }
      ]
    }
    """
    
    try:
        # Configuration spécifique pour forcer le JSON
        # Nécessite un modèle compatible comme gemini-1.5-flash ou gemini-1.5-pro
        json_config = generation_config.copy()
        json_config["response_mime_type"] = "application/json"
        
        # On utilise le même modèle mais avec la config JSON surchargée pour cet appel
        # Note: genai.GenerativeModel est stateful pour la config, donc on réinstancie ou on passe la config
        # La méthode generate_content accepte generation_config en surcharge
        
        response = model.generate_content(prompt, generation_config=json_config)
        return response.text
    except Exception as e:
        logger.error(f"Error generating quiz: {e}")
        # En cas d'erreur, on retourne un JSON vide valide pour éviter le crash
        return '{ "questions": [] }'
