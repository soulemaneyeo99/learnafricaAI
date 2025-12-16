from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api import deps
from app.db.session import get_db
from app.models.course import Course, Enrollment
from app.models.user import User
from app.schemas.course import Course as CourseSchema, CourseCreate, Enrollment as EnrollmentSchema

router = APIRouter()

@router.get("/", response_model=List[CourseSchema])
async def read_courses(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    level: Optional[str] = None
) -> Any:
    """
    Retrieve courses with optional filters.
    """
    query = select(Course)
    if category:
        query = query.filter(Course.category == category)
    if level:
        query = query.filter(Course.level == level)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    courses = result.scalars().all()
    return courses

@router.post("/", response_model=CourseSchema, status_code=201)
async def create_course(
    *,
    db: AsyncSession = Depends(get_db),
    course_in: CourseCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new course. (Admin/Teacher only - TODO: check permissions)
    """
    # Simple permission check
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    course = Course(**course_in.model_dump())
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course

@router.get("/{course_id}", response_model=CourseSchema)
async def read_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get course by ID.
    """
    result = await db.execute(select(Course).filter(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/{course_id}/enroll", response_model=EnrollmentSchema)
async def enroll_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Enroll current user in a course.
    """
    # Check if course exists
    result = await db.execute(select(Course).filter(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check already enrolled
    result = await db.execute(
        select(Enrollment).filter(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id
        )
    )
    enrollment = result.scalars().first()
    if enrollment:
        raise HTTPException(status_code=400, detail="Already enrolled")

    enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)
    return enrollment

@router.put("/{course_id}/progress", response_model=EnrollmentSchema)
async def update_progress(
    course_id: int,
    progress: float,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update progress for a course (0.0 to 100.0).
    """
    if not (0.0 <= progress <= 100.0):
        raise HTTPException(status_code=400, detail="Progress must be between 0 and 100")

    result = await db.execute(
        select(Enrollment).filter(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id
        )
    )
    enrollment = result.scalars().first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    enrollment.progress = progress
    if progress == 100.0:
        enrollment.status = "completed"
    
    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)
    return enrollment
