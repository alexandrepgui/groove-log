from fastapi import APIRouter, Depends, Query

from deps import get_repo
from repository.mongo import MongoRepository

router = APIRouter()


@router.get("/api/usage")
async def get_usage_summary(
    days: int = Query(30, ge=1, le=365),
    repo: MongoRepository = Depends(get_repo),
):
    """Return aggregated LLM usage stats over the last N days."""
    return repo.get_usage_summary(days=days)
