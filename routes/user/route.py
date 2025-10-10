from fastapi import APIRouter, HTTPException, Depends, Body
from sqlmodel import Session
from db.database import get_session
from user import delete_user, update_user

app = APIRouter()

@app.delete("/{user_id}")
def delete_user_root(user_id: str, session: Session = Depends(get_session)):
    success = delete_user(user_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted", "user_id": user_id}

@app.put("/{user_id}")
def update_user_root(
    user_id: str,
    updated_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    user = update_user(user_id, updated_data, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated", "user_id": user_id, "user": user}