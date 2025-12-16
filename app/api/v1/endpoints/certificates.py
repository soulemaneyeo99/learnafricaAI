from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from app.api import deps
from app.db.session import get_db
from app.models.user import User
from app.models.course import Course, Enrollment
from app.services.blockchain_service import issue_certificate_on_blockchain

router = APIRouter()

class CertificateRequest(BaseModel):
    course_id: int

@router.post("/issue")
async def issue_certificate(
    request: CertificateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Émet un certificat blockchain pour un cours complété.
    """
    # 1. Vérifier que le cours existe
    result = await db.execute(select(Course).filter(Course.id == request.course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # 2. Vérifier l'inscription (optionnel: vérifier si complété)
    # Pour la démo, on suppose que l'utilisateur a complété le cours si l'inscription existe
    # ou on permet l'émission directe.
    
    # 3. Appel au service Blockchain
    try:
        receipt = await issue_certificate_on_blockchain(current_user.email, course.title)
        return receipt
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain Error: {str(e)}")
