from fastapi import APIRouter
from app.api.endPoint import createFaissIndex, createElasticIndex

api_router = APIRouter()

api_router.include_router(createFaissIndex.router, prefix="/faiss/create")
api_router.include_router(createElasticIndex.router, prefix="/elastic/create")