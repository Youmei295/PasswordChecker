import math as m
def entropyCalculator(password: str) -> float:
    if not password:
        return 0
    
    char_set=0

    lower=upper=num=symbol=False
    for c in password:
        if 'a'<= c <='z':
            lower=True
        elif 'A'<= c <='Z':
            upper=True
        elif '0'<= c <='9':
            num=True
        else:
            symbol=True
        if lower and upper and num and symbol:
            break

    if lower:
        char_set+=26

    if upper:
        char_set+=26

    if num:
        char_set+=10

    if symbol:
        char_set+=32

    return m.log2(char_set)*len(password)

def classify_entropy(entropy) -> str:
    if entropy < 28:
        return "very weak"
    elif entropy < 36:
        return "weak"
    elif entropy < 60:
        return "medium"
    elif entropy < 128:
        return "strong"
    else:
        return "very strong"
    
def password_analyzer(password: str) -> dict:
    entropy=entropyCalculator(password)
    score=classify_entropy(entropy)
    return{
        "entropy":entropy,
        "score":score
    }

