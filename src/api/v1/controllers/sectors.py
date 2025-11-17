from fastapi import APIRouter

router = APIRouter(prefix="/sectors", tags=["sectors"])


@router.get("/")
async def list_sectors():
    """Placeholder: return a paginated list of sectors/pathways."""
    return {"items": [], "total": 0}
