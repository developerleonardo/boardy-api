from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class Card(BaseModel):
    list_id: str
    id: int
    name: str
    description: str
    order: int

card_list = [
    Card(list_id="list1", id=1, name="Task 1", description="This is the first task.", order=1),
    Card(list_id="list1", id=2, name="Task 2", description="This is the second task.", order=2),
    Card(list_id="list2", id=3, name="Task 3", description="This is the third task.", order=1),
]

router = APIRouter(prefix="/cards")
@router.get("/")
async def cards():
    return card_list   
@router.get("/{id}")
async def card(id: str):
    return search_card_by_id(id)
@router.post("/", response_model=Card ,status_code=201)
async def create_card(card: Card):
    if check_card_exists(card.id):
        raise HTTPException(status_code=400, detail="Card with this ID already exists")
    card_list.append(card)
    return card
@router.put("/{id}")
async def update_card(id: str, updated_card: Card):
    for index, card in enumerate(card_list):
        if card.id == id:
            card_list[index] = updated_card
            return updated_card
    raise HTTPException(status_code=404, detail="Card not found")
@router.delete("/{id}")
async def delete_card(id: str):
    for index, card in enumerate(card_list):
        if card.id == id:
            del card_list[index]
            return {"detail": "Card deleted successfully"}
    raise HTTPException(status_code=404, detail="Card not found")

def search_card_by_id(id: str):
    for card in card_list:
        if card.id == id:
            return card
    return None
def check_card_exists(id: str):
    return search_card_by_id(id) is not None      