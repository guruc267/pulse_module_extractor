# agents/hierarchy_builder.py

def build_hierarchy(cleaned_pages):
    hierarchy = []

    for url, content in cleaned_pages.items():
        hierarchy.append({
            "source": url,
            "content": content[:4000]  # limit size for LLM
        })

    return hierarchy
