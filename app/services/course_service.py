from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.course import Course

async def get_all_courses_context(db: AsyncSession) -> str:
    """
    Récupère tous les cours et reformate une chaîne de contexte pour l'IA.
    """
    result = await db.execute(select(Course))
    courses = result.scalars().all()
    
    if not courses:
        return "Aucun cours n'est disponible pour le moment."
        
    context_lines = ["Voici la liste des cours disponibles sur la plateforme LearnAfrica AI :"]
    for course in courses:
        context_lines.append(f"- {course.title} ({course.level}): {course.description or 'Pas de description'}")
        
    return "\n".join(context_lines)

async def get_course_context(db: AsyncSession, course_id: int) -> str | None:
    """
    Récupère le contenu détaillé d'un cours spécifique pour le contexte du quiz.
    """
    result = await db.execute(select(Course).filter(Course.id == course_id))
    course = result.scalars().first()
    
    if not course:
        return None
        
    # On pourrait ajouter les leçons ici si elles existaient
    return (
        f"Titre du cours : {course.title}\n"
        f"Niveau : {course.level}\n"
        f"Description : {course.description}\n"
        f"Domaine : {course.category}"
    )
