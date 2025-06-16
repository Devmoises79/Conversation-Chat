import hashlib
import os

# Função para gerar hash SHA-256 da senha simples (sem salt)
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Função para verificar se a senha bate com o hash armazenado (sem salt)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password


# ----------------------
# Versão com salt manual (mais segura, porém simples)
# A senha armazenada deve salvar o salt + hash juntos, por exemplo:
# salt + hash(salt + password)
# Aqui um exemplo básico:

def hash_password_salted(password: str) -> str:
    salt = os.urandom(16)  # gera 16 bytes aleatórios de salt
    salted_pass = salt + password.encode()
    hash_ = hashlib.sha256(salted_pass).hexdigest()
    # armazenar salt + hash juntos (hex)
    return salt.hex() + hash_

def verify_password_salted(plain_password: str, stored: str) -> bool:
    salt = bytes.fromhex(stored[:32])  # salt tem 16 bytes = 32 hex chars
    stored_hash = stored[32:]
    check_hash = hashlib.sha256(salt + plain_password.encode()).hexdigest()
    return check_hash == stored_hash
