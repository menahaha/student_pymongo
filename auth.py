from passlib.context import CryptContext
from jose import jwt, JWTError 
from datetime import datetime, timedelta, timezone


pwd_context = CryptContext(
    schemes = ["bcrypt"],
    deprecated = "auto"
)

SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data):
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes = 30)

    payload.update({
        "exp": expire
    })

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        return None 


