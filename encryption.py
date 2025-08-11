from dotenv import load_dotenv
import os

load_dotenv()
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', None)

def getEncryptionBackend():
    if ENCRYPTION_KEY:
        from cryptography.fernet import Fernet
        fernet = Fernet(ENCRYPTION_KEY.encode())

        def encrypt(data):
            return fernet.encrypt(data.encode()).decode()

        def decrypt(data):
            return fernet.decrypt(data.encode()).decode()
    else:
        def encrypt(data):
            return data

        def decrypt(data):
            return data
        
    return encrypt, decrypt