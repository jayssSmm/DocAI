import hashlib
import json
import re
import redis

# ── Redis connection ──────────────────────────────────────────────────────────
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
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
    """
    Return True when a prompt is context-dependent and should NOT be cached.

    A prompt is stateful when:
      • it matches a known follow-up pattern, OR
      • it is very short (≤ 4 words) with no clear standalone subject
        (short prompts almost always refer to the previous exchange)
    """
    stripped = prompt.strip()

    # Very short prompts are almost always references to prior context
    word_count = len(stripped.split())
    if word_count <= 4:
        # Allow short but self-contained prompts like "What is DNA?"
        if not re.search(r"\b(what|who|when|where|why|how|define|explain|describe)\b",
                         stripped, re.IGNORECASE):
            return True

    # Check against all stateful patterns
    for pattern in _STATEFUL_RE:
        if pattern.search(stripped):
            return True

    return False


def make_cache_key(prompt: str) -> str:
    """Deterministic Redis key derived from the normalised prompt text."""
    normalised = prompt.strip().lower()
    digest = hashlib.sha256(normalised.encode()).hexdigest()
    return f"llm:cache:{digest}"


def get_cached_response(prompt: str) -> str | None:
    """
    Return a cached LLM response for *stateless* prompts, or None.
    Stateful prompts always return None (skip cache look-up entirely).
    """
    if is_stateful(prompt):
        return None  # never cache context-dependent prompts

    key = make_cache_key(prompt)
    raw = redis_client.get(key)
    if raw:
        data = json.loads(raw)
        return data.get("response")
    return None


def set_cached_response(prompt: str, response: str) -> bool:
    """
    Persist a prompt→response pair only when the prompt is stateless.
    Returns True if the value was cached, False if it was skipped.
    """
    if is_stateful(prompt):
        return False  # silently skip stateful prompts

    key = make_cache_key(prompt)
    payload = json.dumps({"prompt": prompt, "response": response})
    redis_client.setex(key, CACHE_TTL, payload)
    return True


# ── Flask integration helper ──────────────────────────────────────────────────

def get_llm_response(prompt: str, llm_call_fn) -> dict:
    """
    Drop-in helper for Flask route handlers.

    Usage:
        from smart_cache import get_llm_response

        @app.route("/chat", methods=["POST"])
        def chat():
            prompt = request.json["prompt"]
            result = get_llm_response(prompt, call_my_llm)
            return jsonify(result)

    `llm_call_fn` must be a callable that accepts a prompt string and returns
    the LLM response string, e.g.:
        def call_my_llm(prompt: str) -> str:
            ...

    Returns a dict:
        {
            "response": "<llm text>",
            "cached":   True | False,   # whether the result came from cache
            "stored":   True | False    # whether this response was newly cached
        }
    """
    stateful = is_stateful(prompt)

    # 1. Try cache (only for stateless prompts)
    if not stateful:
        cached = get_cached_response(prompt)
        if cached:
            return {"response": cached, "cached": True, "stored": False}

    # 2. Call the real LLM
    response = llm_call_fn(prompt)

    # 3. Persist if stateless
    stored = set_cached_response(prompt, response)

    return {"response": response, "cached": False, "stored": stored}


# ── Quick self-test ───────────────────────────────────────────────────────────
if __name__ == "__main__":
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