from fastapi import APIRouter, Query, HTTPException
from services.page_service import process_target_url

router = APIRouter()

@router.get("/pages")
async def get_target_page(target: str = Query(..., description="URL of the page to crawl")):
    try:
        return await process_target_url(target)
        #return {"message": f"URL to Crawl is: {target}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=429, detail=str(e))
