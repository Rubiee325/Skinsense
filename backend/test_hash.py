from passlib.context import CryptContext

def test_hash():
    pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
    password = "a" * 100 # Very long password
    print(f"Hashing password of length {len(password)}...")
    h = pwd_context.hash(password)
    print(f"Hash: {h[:50]}...")
    print(f"Verifying: {pwd_context.verify(password, h)}")

if __name__ == "__main__":
    test_hash()
