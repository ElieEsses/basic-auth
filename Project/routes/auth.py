from fastapi import APIRouter, HTTPException
from Project.db.DBUtils import get_db
from Project.models.auth import SignupRequest, LoginRequest, TokenResponse, UserResponse
from Project.services.auth import _hash_password, _verify_email_shape, _verify_password, _generate_token

router = APIRouter()


@router.post("/auth/signup")
def signup(user_data: SignupRequest) -> UserResponse:
    # validate email shape, check if email already exists
    if not _verify_email_shape(user_data.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    if not user_data.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    hashed_password = _hash_password(user_data.password)

    with get_db() as db:
        # Check if email already exists
        existing = db.execute("SELECT id FROM users WHERE email = ?", (user_data.email,)).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Insert new user
        cursor = db.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (user_data.name, user_data.email, hashed_password),
        )
        return UserResponse(id=cursor.lastrowid, name=user_data.name, email=user_data.email)

@router.post("/auth/login")
def login(login_data: LoginRequest) -> TokenResponse:
    # validate email shape
    if not _verify_email_shape(login_data.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    with get_db() as db:
        user = db.execute("SELECT * FROM users WHERE email = ?", (login_data.email,)).fetchone()
        if not user or not _verify_password(login_data.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = _generate_token(user["id"])
        return TokenResponse(access_token=token)
    
@router.get("/auth/me")
def get_current_user():
    pass
