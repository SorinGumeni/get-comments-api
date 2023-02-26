from typing import List

from fastapi import APIRouter, Query
from fastapi_paginate import Page, Params, paginate

from models.comments_model import CommentsModel
from services import comments_service

router = APIRouter()


@router.get("/comments", response_model=Page[CommentsModel])
async def get_comments(
    omit: List[str] = Query(None),
    page: int = Query(default=1, ge=1),
    total: int = Query(default=25, ge=1),
):
    comments_list = comments_service.get_comments(omit)
    pagination_params = Params.construct(size=total, page=page)

    return paginate(comments_list, pagination_params)
