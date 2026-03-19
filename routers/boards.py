from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class Board(BaseModel):
    user_id: int
    id: str
    name: str
    description: str

board_list = [
    Board(userId=1, id="board1", name="Project Alpha", description="This is the first project board."),
    Board(userId=2, id="board2", name="Project Beta", description="This is the second project board."),
    Board(userId=3, id="board3", name="Project Gamma", description="This is the third project board."),
    ]

router = APIRouter(prefix="/boards")
@router.get("/")
async def boards():
    return board_list   
@router.get("/{id}")
async def board(id: str):
    return search_board_by_id(id)
@router.post("/", response_model=Board ,status_code=201)
async def create_board(board: Board):
    if check_board_exists(board.id):
        raise HTTPException(status_code=400, detail="Board with this ID already exists")
    board_list.append(board)
    return board
@router.put("/{id}")
async def update_board(id: str, updated_board: Board):
    for index, board in enumerate(board_list):
        if board.id == id:
            board_list[index] = updated_board
            return updated_board
    raise HTTPException(status_code=404, detail="Board not found")
@router.delete("/{id}")
async def delete_board(id: str):
    for index, board in enumerate(board_list):
        if board.id == id:
            del board_list[index]
            return {"detail": "Board deleted successfully"}
    raise HTTPException(status_code=404, detail="Board not found")

def search_board_by_id(id: str):
    for board in board_list:
        if board.id == id:
            return board
    return None
def check_board_exists(id: str):
    if(type(search_board_by_id(id)) == Board):
        return True
    return False