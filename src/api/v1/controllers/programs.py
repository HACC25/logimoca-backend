from fastapi import APIRouter

router = APIRouter(prefix="/programs", tags=["programs"])


@router.get("/")
async def list_programs():
    """Placeholder: return a paginated list of programs."""
    return {"items": [], "total": 0}
