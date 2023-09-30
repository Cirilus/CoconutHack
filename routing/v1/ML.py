import random
import validators
from fastapi import APIRouter, HTTPException
from schemas.Categories import CategoryResponse, Categories, Themes
from starlette import status

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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The url isn't valid")

    themes_list = list(Themes)
    categories_list = list(Categories)

    random_theme = random.choice(themes_list)
    random_category = random.choice(categories_list)

    response = CategoryResponse()
    response.theme = random_theme
    response.category = random_category

    return response
