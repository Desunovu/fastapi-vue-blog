from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from ..config import FASTAPI_MONGODB_URL, FASTAPI_MONGODB_DATABASE
from ...modules.articles.models import ArticleDocument
from ...modules.comments.models import CommentDocument
from ...modules.users.models import UserDocument


# Init beanie ODM
async def init_odm():
    mongo_client = AsyncIOMotorClient(FASTAPI_MONGODB_URL)
    await init_beanie(
        database=mongo_client[FASTAPI_MONGODB_DATABASE],
        document_models=[
            ArticleDocument,
            UserDocument,
            CommentDocument,
        ],
    )
