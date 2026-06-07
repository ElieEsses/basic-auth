from fastapi import APIRouter, Depends, HTTPException, Response

from Project.config import DEBUG_MODE
from Project.db.DBUtils import get_db
from Project.models.auth import LoginRequest, SignupRequest, UserResponse
from Project.services import auth

router = APIRouter()


@router.post("/auth/signup")
def signup(user_data: SignupRequest) -> UserResponse:
    # validate email shape, check if email already exists
    if not auth.verify_email_shape(user_data.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    if not user_data.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    hashed_password = auth.hash_password(user_data.password)

    with get_db() as db:
        # Check if email already exists
        existing = db.execute(
            "SELECT id FROM users WHERE email = ?", (user_data.email,)
        ).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Insert new user
        cursor = db.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (user_data.name, user_data.email, hashed_password),
        )
        return UserResponse(
            id=cursor.lastrowid, name=user_data.name, email=user_data.email
        )


@router.post("/auth/login")
def login(login_data: LoginRequest, response: Response) -> dict[str, bool]:
    if not auth.verify_email_shape(login_data.email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    with get_db() as db:
        user = db.execute(
            "SELECT * FROM users WHERE email = ?",
            (login_data.email,),
        ).fetchone()

    if not user or not auth.verify_password(
        login_data.password,
        user["password_hash"],
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token(user["id"])

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=not DEBUG_MODE,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )

    return {"success": True}


@router.post("/auth/logout")
def logout(response: Response) -> dict[str, bool]:
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=not DEBUG_MODE,
        samesite="lax",
    )
    return {"success": True}


@router.get("/auth/me")
def me(user: UserResponse = Depends(auth.get_current_user)) -> UserResponse:
    return user
