# agents/llm_extractor.py

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_topic_candidates(text):
    """
    VERY HIGH-RECALL extraction.
    Any reasonable heading / phrase becomes a candidate.
    """
    candidates = set()

    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        # Skip junk
        if not line:
            continue
        if len(line) > 80:
            continue
        if any(x in line.lower() for x in ["cookie", "privacy policy", "terms"]):
            continue

        # Accept almost everything meaningful
        candidates.add(line.lower())

    return list(candidates)


def cluster_topics(topics, threshold=0.72):
    """
    Semantic deduplication (taxonomy-style).
    """
    if not topics:
        return []

    embeddings = model.encode(topics)
    clusters = []

    for i, topic in enumerate(topics):
        placed = False

        for cluster in clusters:
            rep_idx = cluster["indices"][0]
            sim = cosine_similarity(
                [embeddings[i]],
                [embeddings[rep_idx]]
            )[0][0]

            if sim >= threshold:
                cluster["indices"].append(i)
                cluster["topics"].append(topic)
                placed = True
                break

        if not placed:
            clusters.append({
                "indices": [i],
                "topics": [topic]
            })

    return clusters


def build_modules(clusters):
    modules = []

    for cluster in clusters:
        topics = cluster["topics"]

        module_name = topics[0].title()

        submodules = {}
        for t in topics[1:6]:  # limit submodules
            submodules[t.title()] = (
                f"Functionality related to {t}, as described in the documentation."
            )

        description = (
            f"This module represents functionality related to {module_name.lower()}, "
            f"derived from the product help documentation."
        )

        modules.append({
            "module": module_name,
            "Description": description,
            "Submodules": submodules
        })

    return modules


def extract_modules(hierarchy_data):
    all_candidates = []

    for item in hierarchy_data:
        text = item.get("content", "")
        all_candidates.extend(extract_topic_candidates(text))

    # Deduplicate early
    all_candidates = list(set(all_candidates))

    clusters = cluster_topics(all_candidates)

    modules = build_modules(clusters)

    return modules
