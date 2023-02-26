from pydantic import BaseModel
from typing import Any, Dict, Optional


class CommentsModel(BaseModel):
    body: Optional[str]
    email: Optional[str]
    id: Optional[int]
    name: Optional[str]
    postId: Optional[int]

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        kwargs.pop("exclude_none", None)
        return super().dict(*args, exclude_none=True, **kwargs)

    class Config:
        orm = True
