import os
import sys
import requests
import streamlit as st

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from utils.document_formatter import format_docx, format_pdf


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")

st.write(
    "Generate professional legal document drafts using Generative AI."
)

st.warning(
    "⚠️ This document is an AI-generated draft and should be "
    "reviewed by a qualified legal professional."
)


# --------------------------------------------------
# DOCUMENT TYPES
# --------------------------------------------------

document_types = [
    "Employment Contract",
    "NDA",
    "Lease Agreement",
    "Service Agreement",
    "Freelance Contract",
    "Employment Offer Letter"
]


# --------------------------------------------------
# INPUTS
# --------------------------------------------------

document_type = st.selectbox(
    "Document Type",
    document_types
)

parties = st.text_area(
    "Parties Involved",
    placeholder=(
        "Example:\n"
        "Employer: ABC Technologies Pvt Ltd\n"
        "Employee: John Doe"
    )
)

terms = st.text_area(
    "Terms and Conditions",
    placeholder=(
        "Enter the important terms, responsibilities, "
        "payment details, duration, conditions, etc."
    )
)

effective_date = st.date_input(
    "Effective Date"
)


# --------------------------------------------------
# BACKEND URL
# --------------------------------------------------

# For Streamlit Cloud:
# BACKEND_URL will be set in Streamlit Secrets / Environment.
#
# For local development:
# It automatically uses localhost.

backend_url = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

if st.button("🚀 Generate Legal Document", type="primary"):

    if not parties.strip():
        st.error("Please enter the parties involved.")
        st.stop()

    if not terms.strip():
        st.error("Please enter the terms and conditions.")
        st.stop()

    request_data = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "effective_date": str(effective_date)
    }

    try:

        with st.spinner("Generating your legal document..."):

            response = requests.post(
                f"{backend_url}/generate",
                json=request_data,
                timeout=120
            )

        if response.status_code == 200:

            result = response.json()

            if result.get("success"):

                st.session_state["document"] = result["document"]

                st.success("✅ Legal document generated successfully!")

            else:

                st.error("Failed to generate the document.")

        else:

            try:
                error_detail = response.json().get(
                    "detail",
                    response.text
                )
            except Exception:
                error_detail = response.text

            st.error(
                f"Backend error ({response.status_code}): "
                f"{error_detail}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Could not connect to the backend. "
            "Please check the backend URL."
        )

    except requests.exceptions.Timeout:

        st.error(
            "⏳ Request timed out. "
            "The AI generation took too long."
        )

    except Exception as e:

        st.error(
            f"❌ Unexpected error: {str(e)}"
        )


# --------------------------------------------------
# DISPLAY GENERATED DOCUMENT
# --------------------------------------------------

if "document" in st.session_state:

    st.divider()

    st.subheader("📄 Generated Legal Document")

    edited_document = st.text_area(
        "Preview / Edit Document",
        value=st.session_state["document"],
        height=600
    )

    # Update session state with edited content
    st.session_state["document"] = edited_document


    # --------------------------------------------------
    # DOWNLOAD OPTIONS
    # --------------------------------------------------

    st.subheader("⬇️ Download Document")

    col1, col2, col3 = st.columns(3)


    # TXT
    with col1:

        st.download_button(
            label="📄 Download TXT",
            data=edited_document,
            file_name="legal_document.txt",
            mime="text/plain"
        )


    # DOCX
    with col2:

        try:

            docx_file = format_docx(edited_document)

            st.download_button(
                label="📝 Download DOCX",
                data=docx_file,
                file_name="legal_document.docx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                )
            )

        except Exception as e:

            st.error(
                f"DOCX generation failed: {str(e)}"
            )


    # PDF
    with col3:

        try:

            pdf_file = format_pdf(edited_document)

            st.download_button(
                label="📕 Download PDF",
                data=pdf_file,
                file_name="legal_document.pdf",
                mime="application/pdf"
            )

        except Exception as e:

            st.error(
                f"PDF generation failed: {str(e)}"
            )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "LegalEase — AI-powered legal document drafting assistant"
)