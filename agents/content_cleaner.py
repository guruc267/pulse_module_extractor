# agents/content_cleaner.py

import re


def clean_text(raw_text):
    """
    Clean text WITHOUT destroying document structure.
    """
    text = raw_text.lower()

    # ❌ DO NOT collapse all whitespace
    # ✅ Normalize spaces but KEEP newlines
    text = re.sub(r"[ \t]+", " ", text)

    # Remove common noise
    text = re.sub(r"cookie|privacy policy|terms of service|copyright", "", text)

    return text.strip()


def clean_pages(pages_dict):
    cleaned = {}
    for url, text in pages_dict.items():
        cleaned[url] = clean_text(text)
    return cleaned
