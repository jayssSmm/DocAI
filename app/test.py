import string

def is_stateful(prompt: str) -> bool:

    stripped = prompt.strip()

    '''for pattern in _STATEFUL_RE:
        if pattern.search(stripped):
            return True'''

    words = stripped.split()
    word_count = len(words)

    if word_count <= 3:
        if any(w in ["it", "this", "that", "those"] for w in words):
            return True
    if word_count <= 3:
        if any(w in (string.ascii_letters + string.digits) for w in words):
            return True
    if word_count <= 3:
        try:
            if any(int(w) for w in words):
                return True
        except:
            pass
            

    return False

a=input("a= ")
print(is_stateful(a))