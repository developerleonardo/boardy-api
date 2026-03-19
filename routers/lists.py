from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class List(BaseModel):
    id: str
    name: str
    boardId: str

list_list = [
    List(boardId=1, id="list1", name="To Do"),
    List(boardId=1, id="list2", name="In Progress"),
    List(boardId=1, id="list3", name="Done"),
]

router = APIRouter(prefix="/lists")
@router.get("/")
async def lists():
    return list_list

@router.get("/{id}")
async def list(id: str):
    return search_list_by_id(id)

@router.post("/", response_model=List ,status_code=201)
async def create_list(list: List):
    if check_list_exists(list.id):
        raise HTTPException(status_code=400, detail="List with this ID already exists")
    list_list.append(list)
    return list

@router.put("/{id}")
async def update_list(id: str, updated_list: List):
    for index, list in enumerate(list_list):
        if list.id == id:
            list_list[index] = updated_list
            return updated_list
    raise HTTPException(status_code=404, detail="List not found")

@router.delete("/{id}")
async def delete_list(id: str):
    for index, list in enumerate(list_list):
        if list.id == id:
            del list_list[index]
            return {"detail": "List deleted successfully"}
    raise HTTPException(status_code=404, detail="List not found")

def search_list_by_id(id: str):
    for list in list_list:
        if list.id == id:
            return list
    return None

def check_list_exists(id: str):
    if(type(search_list_by_id(id)) == List):
        return True
    return False