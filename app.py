# app.py
import sys
import os
import json
import streamlit as st

# ✅ Ensure project root is in Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from agents.module_extractor import run_extraction

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(
    page_title="Pulse – Module Extraction AI Agent",
    layout="wide"
)

st.title("📦 Pulse – Module Extraction AI Agent")
st.write(
    "Extract structured **product modules and submodules** from "
    "documentation-based help websites."
)

# -------------------------------
# URL Input
# -------------------------------
st.subheader("🔗 Documentation URLs")

urls_input = st.text_area(
    "Enter one or more documentation URLs (one per line)",
    placeholder=(
        "https://help.zluri.com/\n"
        "https://wordpress.org/documentation/\n"
        "https://www.chargebee.com/docs/2.0/"
    )
)

urls = [u.strip() for u in urls_input.splitlines() if u.strip()]

# -------------------------------
# Run Extraction
# -------------------------------
if st.button("🚀 Extract Modules"):
    if not urls:
        st.error("Please enter at least one valid documentation URL.")
    else:
        with st.spinner("Running extraction pipeline..."):
            try:
                result = run_extraction(urls)
            except Exception as e:
                st.error(f"Extraction failed: {e}")
                result = []

        if not result:
            st.warning(
                "No modules were extracted. "
                "The documentation may be dynamic or sparsely structured."
            )
        else:
            st.success("Extraction completed successfully!")

            # -------------------------------
            # Display Results
            # -------------------------------
            st.subheader("📊 Extracted Modules")

            for module in result:
                with st.expander(f"📁 {module['module']}"):
                    st.write(f"**Description:** {module['Description']}")

                    if module.get("Submodules"):
                        st.write("**Submodules:**")
                        for sub, desc in module["Submodules"].items():
                            st.markdown(f"- **{sub}**: {desc}")
                    else:
                        st.write("_No submodules detected._")

            st.subheader("⬇️ Download Output")

            st.download_button(
                label="Download JSON Output",
                data=json.dumps(result, indent=2),
                file_name="module_extraction_output.json",
                mime="application/json"
            )
