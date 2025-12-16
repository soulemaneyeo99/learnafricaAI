import asyncio
import json
from app.services.ai.gemini_service import generate_response, generate_quiz_for_topic

async def main():
    print("--- Testing Chat (generate_response) ---")
    response = await generate_response(
        "Explique-moi la différence entre une IA et un algorithme classique.",
        context="Cours d'introduction à l'Informatique. Chapitre 1: Les bases."
    )
    print(f"Chat Response:\n{response}\n")

    print("--- Testing Quiz (generate_quiz_for_topic) - JSON Mode ---")
    quiz_json_str = await generate_quiz_for_topic(
        "Les bases de Python",
        num_questions=3,
        context="Python est un langage interprété. Il utilise l'indentation pour les blocs. Les variables ne sont pas typées statiquement."
    )
    
    print(f"Raw Quiz Response:\n{quiz_json_str}\n")
    
    try:
        quiz_data = json.loads(quiz_json_str)
        print("✅ JSON Parsing Successful!")
        print(json.dumps(quiz_data, indent=2, ensure_ascii=False))
        
        if "questions" in quiz_data and len(quiz_data["questions"]) > 0:
            print("✅ 'questions' key found and not empty.")
        else:
            print("❌ 'questions' key missing or empty.")
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parsing Failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
