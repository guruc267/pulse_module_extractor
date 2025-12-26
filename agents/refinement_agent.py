# agents/refinement_agent.py

import re

NOISE_KEYWORDS = [
    "welcome",
    "still have questions",
    "featured articles",
    "help center",
    "popular resources",
    "our team is ready",
]

def is_noise_module(name: str) -> bool:
    name_lower = name.lower()
    return any(k in name_lower for k in NOISE_KEYWORDS)


def clean_module_name(name: str) -> str:
    # Remove weird concatenations
    name = re.sub(r"(reports|data|insights)", r" \1", name, flags=re.I)

    # Normalize spaces
    name = re.sub(r"\s+", " ", name).strip()

    return name.title()


def refine_modules(modules):
    refined = []

    for m in modules:
        name = m.get("module", "")

        # Drop noise
        if is_noise_module(name):
            continue

        # Drop very long names
        if len(name.split()) > 12 or len(name) > 80:
            continue

        m["module"] = clean_module_name(name)
        refined.append(m)

    return refined
