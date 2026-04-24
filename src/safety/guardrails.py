from __future__ import annotations


UNSAFE_PATTERNS = [
    "lie in court",
    "hide evidence",
    "threaten my landlord",
    "fake documents",
]


def detect_unsafe_request(user_text: str) -> bool:
    lowered = user_text.lower()
    return any(pattern in lowered for pattern in UNSAFE_PATTERNS)


def low_support_response() -> str:
    return (
        "I do not have enough grounded North Carolina source support to answer that "
        "reliably. I can help you narrow the issue and point you to legal aid or "
        "court resources instead."
    )
