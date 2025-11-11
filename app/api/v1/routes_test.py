from fastapi import APIRouter

router = APIRouter()

@router.get("/greet")
def greet():
    return{"greeting":"Hello, GoodMorning!"}