from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.video_service import video_service

router = APIRouter()

class MeetingRequest(BaseModel):
    topic: str
    duration_minutes: int = 60

@router.post("/create-meeting")
async def create_video_meeting(
    request: MeetingRequest,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Crée une salle de classe virtuelle via Moov Fibre.
    """
    try:
        meeting_details = await video_service.create_meeting(
            host_name=current_user.full_name,
            topic=request.topic,
            duration_minutes=request.duration_minutes
        )
        return meeting_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video Provider Error: {str(e)}")
