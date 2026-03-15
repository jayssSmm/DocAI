import hashlib
import re
import redis

# ── Redis connection ──────────────────────────────────────────────────────────
r= redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
CACHE_TTL = 60 * 60 * 24  # 24 hours

# ── Stateful trigger patterns ─────────────────────────────────────────────────
# Prompts that start with (or are dominated by) these patterns depend on prior
# context and must NOT be cached.
STATEFUL_PATTERNS = [
    r"^give\s+(me\s+)?(an?\s+)?example",          # give example / give me an example
    r"^(can\s+you\s+)?elaborate",                  # elaborate / can you elaborate
    r"^(explain\s+)?(that|it|this)\b",             # explain that, explain it
    r"^(tell\s+me\s+)?more(\s+about\s+(it|that))?$",  # more / tell me more
    r"^expand\s+(on\s+)?(it|that|this)",           # expand on it
    r"^what\s+do\s+you\s+mean",                    # what do you mean
    r"^clarify\s+(it|that|this)",                  # clarify that
    r"^(now\s+)?simplify\s+(it|that|this)",        # simplify it
    r"^how\s+(does\s+)?(it|that|this)\s+work",     # how does it work
    r"^why\s+(is\s+)?(it|that|this)\b",            # why is that
    r"^(and\s+)?what\s+about\s+(it|that|this)",    # what about it
    r"^(ok|okay|alright|now|so)[,.]?\s+",          # ok now do X (continuation markers)
    r"^(also|additionally|furthermore|moreover)\b", # additive follow-ups
    r"^continue",                                   # continue
    r"^go\s+on",                                    # go on
    r"^next",                                       # next (step / example)
    r"^(please\s+)?(re)?write\s+(it|that|this)",   # rewrite it/that
    r"\b(above|previous|last|prior)\b",            # references to previous output
    r"\bmentioned\b",                              # "as you mentioned"
    r"\byou\s+(said|mentioned|described)\b",       # "you said / you described"
    r"\bthe\s+(example|explanation|answer|response|code|above)\b",  # "the example"
]

# Pre-compile for performance
_STATEFUL_RE = [re.compile(p, re.IGNORECASE) for p in STATEFUL_PATTERNS]


def is_stateful(prompt: str) -> bool:

    stripped = prompt.strip()

    for pattern in _STATEFUL_RE:
        if pattern.search(stripped):
            return True

    words = stripped.split()
    word_count = len(words)

    if word_count <= 3:
        if any(w in ["it", "this", "that", "those"] for w in words):
            return True

    return False


def make_cache_key(prompt: str) -> str:

    normalised = prompt.strip().lower()
    digest = hashlib.sha256(normalised.encode()).hexdigest()
    return digest


def get_cached_response(prompt: str) -> str | None:

    if is_stateful(prompt):
        return None  # never cache context-dependent prompts

    key = make_cache_key(prompt)
    raw = r.exists(key)
    if raw:
        return r.get(key)
    return None


def set_cached_response(prompt: str, response: str) -> bool:

    if is_stateful(prompt):
        return False  # silently skip stateful prompts

    key = make_cache_key(prompt)
    r.set(key,response)
    r.expire(key,CACHE_TTL)
    
    return True


# ── Quick self-test ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    # the test is written by ai
    test_cases = [
        # (prompt, expected_stateful)
        ("Explain Newton's laws in 1 line", False),
        ("give example", True),
        ("Give me an example", True),
        ("Elaborate more", True),
        ("explain that", True),
        ("Explain Pythagoras theorem in 1 line", False),
        ("What is machine learning?", False),
        ("tell me more", True),
        ("expand on it", True),
        ("ok now give me the formula", True),
        ("What is DNA?", False),
        ("more", True),
        ("How does photosynthesis work?", False),
        ("rewrite it in simple terms", True),
        ("as you mentioned above", True),
        ("Define recursion", False),
    ]

    print(f"{'Prompt':<45} {'Expected':>10} {'Got':>6} {'Pass':>5}")
    print("-" * 70)
    all_pass = True
    for prompt, expected in test_cases:
        got = is_stateful(prompt)
        ok = got == expected
        all_pass = all_pass and ok
        status = "✓" if ok else "✗"
        print(f"{prompt:<45} {str(expected):>10} {str(got):>6}  {status}")

    print("-" * 70)
    print("All tests passed!" if all_pass else "Some tests FAILED.")