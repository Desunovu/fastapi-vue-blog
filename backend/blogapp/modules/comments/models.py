from datetime import datetime
from enum import Enum

from beanie import Link, PydanticObjectId
from pydantic import BaseModel, Field

from ..articles.models import ArticleDocument
from ..users.models import UserDocument
from ...utils.extended_document import ExtendedDocument


class CommentDocument(ExtendedDocument):
    content: str
    author: Link[UserDocument]
    disabled: bool = False
    is_reply: bool = False
    article: Link[ArticleDocument] | None = Field(None, exclude=True)
    replies: list[Link["CommentDocument"]] = []
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Settings:
        name = "comments"


class CommentDocumentResponse(CommentDocument):
    """Модель для ответа с fetch_links=True"""
    author: UserDocument
    replies: list[CommentDocument]


class CommentUpdate(BaseModel):
    """Тело запроса изменения комментария"""

    content: str = Field(..., min_length=2, max_length=120)


class CommentCreate(CommentUpdate):
    """Тело запроса создания комментария"""

    article_id: PydanticObjectId = Field(..., exclude=True)


class ReplyCreate(CommentUpdate):
    """Тело запроса создания ответа на комментарий"""

    parent_comment_id: PydanticObjectId = Field(..., exclude=True)


class CommentsResponse(BaseModel):
    comments: list[CommentDocumentResponse]


class CommentResponse(BaseModel):
    comment: CommentDocumentResponse


class CommentsSortField(str, Enum):
    created_at = "created_at"
