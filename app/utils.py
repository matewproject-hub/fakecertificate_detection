import hashlib

def generate_hash(data:bytes) -> str:
    sha=hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()