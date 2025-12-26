# agents/module_extractor.py

import sys
import os
import json

# ✅ Add project root to Python path (important for Colab & modular imports)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.crawler import crawl_docs
from agents.content_cleaner import clean_pages
from agents.hierarchy_builder import build_hierarchy
from agents.refinement_agent import refine_modules
from agents.llm_extractor import extract_modules


def run_extraction(urls):
    """
    Runs the full extraction pipeline for the given list of URLs.
    """
    all_pages = {}

    for url in urls:
        pages = crawl_docs(url)
        all_pages.update(pages)

    cleaned = clean_pages(all_pages)
    hierarchy = build_hierarchy(cleaned)
    modules = refine_modules(extract_modules(hierarchy))

    return modules


if __name__ == "__main__":
    # ✅ Multiple documentation URLs (can add more)
    urls = [
        "https://help.zluri.com/",
        "https://wordpress.org/documentation/",
        "https://www.chargebee.com/docs/2.0/"
    ]

    # Ensure output folder exists
    os.makedirs("output", exist_ok=True)

    # Process each URL independently (recommended for evaluation)
    for url in urls:
        print(f"\nProcessing: {url}")

        result = run_extraction([url])

        # Create a clean filename from URL
        filename = (
            url.replace("https://", "")
               .replace("http://", "")
               .replace("/", "_")
               .replace(".", "_")
        )

        output_path = f"output/{filename}.json"

        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        print(f"Extraction completed for {url}")
        print(f"Output saved to: {output_path}")
