# Pulse Module Extractor
This project implements an AI-powered Module Extraction Agent designed to automatically extract product modules and submodules from documentation-based help websites.
This system structured, human-readable JSON output to comprehend product capabilities at scale. It also crawls help manuals, processes and cleans content, and infers hierarchical structure.
Without the need for manual labelling or hardcoded rules, this approach is designed to function across various external documentation sources (B2B and consumer items).
## Streamlit app Link : https://pulsemoduleextractorgurucharan.streamlit.app/

## K Guru Charan RA2211026010141

# Architecture and Agentic Design

The system is designed as a multi-agent pipeline:

## Crawler Agent
- Recursively traverses URLs for documentation
- Manages redirects, broken links, and domain scoping

- It extracts raw textual content from HTML pages.

## Content Cleaner Agent
- Removes navigation, boilerplate, and other repeated text in a user interface.

- Normalizes whitespace and formatting

Clean text output suitable for further semantic processing
## Hierarchy Builder Agent

- Document structure preserved
- Infers hierarchical, parent–child relationships among topics
Generates hierarchical representations intended to support extraction processes

## LLM Extraction Agent
Identifies candidate modules and submodules
- Produces concise, documentation-based descriptions Hallucination is mitigated, as outputs are restricted to contents derived from extraction. 

## Refinement Agent 
- Deduplicates overlapping or noisy module names Excludes headings that are marketing
- or navigation-specific
- Groups semantically similar modules together


# OUTPUT IMAGES
<img width="1200" height="650" alt="Screenshot (172)" src="https://github.com/user-attachments/assets/5bf85f7d-a2e6-426a-826b-3f1da8855db9" />
<img width="1200" height="650" alt="Screenshot (173)" src="https://github.com/user-attachments/assets/b83e951b-8b87-447d-90de-ed22de814c4a" />
<img width="1200" height="650" alt="Screenshot (174)" src="https://github.com/user-attachments/assets/b6ec6133-edba-4e56-9551-e4b86cf13bfe" />
<img width="1200" height="650" alt="Screenshot (175)" src="https://github.com/user-attachments/assets/508fac84-9f31-4301-b7ad-d8ee5e7703a4" />
