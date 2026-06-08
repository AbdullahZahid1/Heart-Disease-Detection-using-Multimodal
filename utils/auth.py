# File: utils/auth.py
import bcrypt

# Mock Database for prototyping. 
# "admin123" is pre-hashed using bcrypt here.
MOCK_USER_DB = {
    "doctor@hospital.com": b'$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjIQqiRQYq' 
}

def verify_password(plain_password, hashed_password):
    """Checks if the entered password matches the securely hashed password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)