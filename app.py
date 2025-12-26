# app.py
import sys
import os
import json
import streamlit as st

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from agents.module_extractor import run_extraction

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Pulse – Module Extraction AI Agent",
    layout="wide"
)

st.title("📦 Pulse – Module Extraction AI Agent")
st.caption(
    "AI-powered extraction of product modules and submodules from "
    "documentation-based help websites."
)
st.caption("— BY K Guru Charan")
st.divider()

# -----------------------------
# Input Section
# -----------------------------
st.subheader("🔗 Input Documentation URLs")

urls_input = st.text_area(
    label="Enter one or more documentation URLs (one per line)",
    height=120,
    placeholder=(
        "https://help.zluri.com/\n"
        "https://wordpress.org/documentation/\n"
        "https://www.chargebee.com/docs/2.0/"
    )
)

urls = [u.strip() for u in urls_input.splitlines() if u.strip()]

run = st.button("🚀 Run Module Extraction")

# -----------------------------
# Execution
# -----------------------------
if run:
    if not urls:
        st.error("Please enter at least one valid documentation URL.")
    else:
        with st.spinner("Running extraction pipeline..."):
            try:
                result = run_extraction(urls)
            except Exception as e:
                st.error(f"Extraction failed: {e}")
                result = []

        st.divider()

        # -----------------------------
        # Result Handling
        # -----------------------------
        if not result:
            st.warning(
                "No modules were extracted.\n\n"
                "This may happen for documentation sites that rely heavily "
                "on dynamic rendering or sparse HTML structure."
            )
        else:
            # Summary
            st.success("Extraction completed successfully!")

            col1, col2 = st.columns(2)
            col1.metric("Total Modules Extracted", len(result))
            col2.metric(
                "Modules With Submodules",
                sum(1 for m in result if m.get("Submodules"))
            )

            st.divider()

            # -----------------------------
            # Module Display
            # -----------------------------
            st.subheader("📊 Extracted Modules")

            for module in result:
                module_name = module.get("module", "Unnamed Module")
                description = module.get("Description", "")
                submodules = module.get("Submodules", {})

                with st.expander(f"📁 {module_name}", expanded=False):
                    st.markdown(f"**Description**  \n{description}")

                    if submodules:
                        st.markdown("**Submodules**")
                        for sub, desc in submodules.items():
                            st.markdown(f"- **{sub}** — {desc}")
                    else:
                        st.caption("No submodules detected for this module.")

            st.divider()

            # -----------------------------
            # Download Section
            # -----------------------------
            st.subheader("⬇️ Export Results")

            st.download_button(
                label="Download JSON Output",
                data=json.dumps(result, indent=2),
                file_name="module_extraction_output.json",
                mime="application/json"
            )

            st.caption(
                "Tip: This output can be further refined or consumed by "
                "product analytics and documentation teams."
            )
