from fastapi import APIRouter

router = APIRouter(prefix="/occupations", tags=["occupations"])


@router.get("/")
async def list_occupations():
    """Placeholder: return a paginated list of occupations."""
    return {"items": [], "total": 0}
