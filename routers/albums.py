from fastapi import APIRouter
from services.google_drive import list_folders


router = APIRouter()

@router.get('/albums')
async def get_albums():
    return list_folders