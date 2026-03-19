from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class BoardList(BaseModel):
    id: str
    name: str
    boardId: str
    order: int

mock_list = [
    BoardList(boardId=1, id="list1", name="To Do", order=1),
    BoardList(boardId=1, id="list2", name="In Progress", order=2),
    BoardList(boardId=1, id="list3", name="Done", order=3),
]

router = APIRouter(prefix="/lists")
@router.get("/")
async def lists():
    return mock_list

@router.get("/{id}")
async def get_list(id: str):
    return search_list_by_id(id)

@router.post("/", response_model=BoardList ,status_code=201)
async def create_list(list_item: BoardList):
    if check_list_exists(list_item.id):
        raise HTTPException(status_code=400, detail="List with this ID already exists")
    mock_list.append(list_item)
    return list_item

@router.put("/{id}")
async def update_list(id: str, updated_list: BoardList):
    for index, list_item in enumerate(mock_list):
        if list_item.id == id:
            mock_list[index] = updated_list
            return updated_list
    raise HTTPException(status_code=404, detail="List not found")

@router.delete("/{id}")
async def delete_list(id: str):
    for index, list_item in enumerate(mock_list):
        if list_item.id == id:
            del mock_list[index]
            return {"detail": "List deleted successfully"}
    raise HTTPException(status_code=404, detail="List not found")

def search_list_by_id(id: str):
    for list_item in mock_list:
        if list_item.id == id:
            return list_item
    return None

def check_list_exists(id: str):
    return search_list_by_id(id) is not None