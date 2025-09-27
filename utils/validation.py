from email.utils import parseaddr

def is_valid_email(email: str) -> bool:
    try:
        return '@' in parseaddr(email)[1]
    except Exception:
        return False
