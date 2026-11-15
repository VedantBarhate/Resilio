import hashlib

def stable_seed(case_id: str, family: str, severity: int, variant: int) -> int:
    raw = f"{case_id}|{family}|{severity}|{variant}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(raw).digest()[:8], "big")
