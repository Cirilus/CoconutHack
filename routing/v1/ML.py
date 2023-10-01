import random
import validators
from fastapi import APIRouter, HTTPException
from schemas.Categories import CategoryResponse, Categories, Themes
from starlette import status
from ML.main import classify_by_embeddings
from utils.utils import fetch_webpage_content, remove_html_tags
from loguru import logger

router = APIRouter(prefix="/api/v1/company", tags=["company"])


@router.get(
    "/check_url",
    response_model=CategoryResponse,
    description="получение всех company",
)
async def get_all_cfa(domain: str | None = None):
    if domain is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There is not url in request")

    if not validators.url(domain):
        logger.debug(f"The url isn't valid, url = {domain}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The url isn't valid")

    html = fetch_webpage_content(domain)

    if not html:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The url isn't valid")

    text = remove_html_tags(html)
    text = ' '.join(text.split())

    result = classify_by_embeddings(text)

    response = CategoryResponse()
    response.category = result[0]
    response.theme = result[1]

    return response
