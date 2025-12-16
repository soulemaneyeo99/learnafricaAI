from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.ai.gemini_service import generate_response, generate_quiz_for_topic

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class QuizRequest(BaseModel):
    topic: str
    num_questions: int = 5
    course_id: int | None = None

@router.post("/chat", response_model=ChatResponse)
async def chat_with_tutor(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)  # Injection DB
):
    """
    Interagit avec le tuteur virtuel IA (Powered by Gemini).
    """
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # 1. Récupérer le contexte des cours
    from app.services.course_service import get_all_courses_context
    context = await get_all_courses_context(db)
    
    # 2. Générer la réponse avec contexte
    ai_response = await generate_response(request.message, context=context)
    return ChatResponse(response=ai_response)

@router.post("/generate-quiz")
async def generate_quiz(
    request: QuizRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Génère un quiz éducatif sur un sujet donné, ou basé sur un cours spécifique.
    """
    context = ""
    if request.course_id:
        from app.services.course_service import get_course_context
        context = await get_course_context(db, request.course_id)
        if not context:
            # On pourrait lever une 404, ou continuer sans contexte
            pass
            
    quiz_json = await generate_quiz_for_topic(request.topic, request.num_questions, context=context)
    return {"quiz": quiz_json}

@router.get("/recommendations/{user_id}")
async def get_recommendations(user_id: int):
    """
    Obtenir des recommandations de cours personnalisées via IA / Algo.
    """
    # Pour l'instant on mocke, mais on pourrait appeler le recommendation_engine ici
    from app.services.recommendation.engine import recommendation_engine
    recs = await recommendation_engine.get_recommendations_for_user(user_id)
    return {"recommendations": recs}
