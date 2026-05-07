import bcrypt


def hash_password_bcrypt(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password_bcrypt(password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
    except Exception:
        return False


def password_strength(password: str) -> tuple[str, int, list[str]]:
    score = 0
    tips = []

    if len(password) >= 8:
        score += 1
    else:
        tips.append("Use at least 8 characters.")
    if any(ch.isupper() for ch in password):
        score += 1
    else:
        tips.append("Add at least one uppercase letter.")
    if any(ch.islower() for ch in password):
        score += 1
    else:
        tips.append("Add at least one lowercase letter.")
    if any(ch.isdigit() for ch in password):
        score += 1
    else:
        tips.append("Add at least one number.")
    if any(not ch.isalnum() for ch in password):
        score += 1
    else:
        tips.append("Add at least one symbol (e.g. @, #, !).")

    label = "Weak"
    if score >= 5:
        label = "Strong"
    elif score >= 3:
        label = "Moderate"

    return label, score, tips
