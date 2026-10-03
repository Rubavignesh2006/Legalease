import sys
import os

# Add project root (C:\legalease) to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


import streamlit as st
import requests

from utils.document_formatter import (
    format_docx,
    format_pdf
)


# --------------------------------------------------
# PAGE CONFIGURATION
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
    "Generate professional legal document drafts using AI."
)


# --------------------------------------------------
# DOCUMENT TYPE
# --------------------------------------------------

document_type = st.selectbox(
    "Document Type",
    [
        "Employment Contract",
        "NDA",
        "Lease Agreement",
        "Service Agreement",
        "Freelance Contract",
        "Employment Offer Letter"
    ]
)


# --------------------------------------------------
# PARTIES
# --------------------------------------------------

parties = st.text_area(
    "Parties",
    placeholder="Example: ABC Technologies and John Doe"
)


# --------------------------------------------------
# TERMS
# --------------------------------------------------

terms = st.text_area(
    "Terms and Conditions",
    placeholder=(
        "Example: Confidentiality, payment terms, "
        "termination conditions..."
    )
)


# --------------------------------------------------
# EFFECTIVE DATE
# --------------------------------------------------

effective_date = st.date_input(
    "Effective Date"
)


# --------------------------------------------------
# GENERATE DOCUMENT
# --------------------------------------------------

if st.button("🚀 Generate Document"):

    if not parties.strip() or not terms.strip():

        st.warning(
            "⚠️ Please enter the parties and terms."
        )

    else:

        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": str(effective_date)
        }

        try:

            with st.spinner(
                "🤖 Generating your legal document... "
                "Please wait."
            ):

                response = requests.post(
                    "http://127.0.0.1:8000/generate",
                    json=payload,
                    timeout=120
                )


            # ------------------------------------------
            # SUCCESS
            # ------------------------------------------

            if response.status_code == 200:

                result = response.json()

                if result.get("success"):

                    st.session_state["document"] = (
                        result["document"]
                    )

                    st.success(
                        "✅ Document generated successfully!"
                    )

                else:

                    st.error(
                        "❌ Document generation failed."
                    )


            # ------------------------------------------
            # BACKEND ERROR
            # ------------------------------------------

            else:

                st.error(
                    f"❌ Backend error:\n\n"
                    f"{response.text}"
                )


        # ----------------------------------------------
        # CONNECTION ERROR
        # ----------------------------------------------

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to FastAPI backend.\n\n"
                "Make sure the backend is running on "
                "http://127.0.0.1:8000"
            )


        # ----------------------------------------------
        # TIMEOUT ERROR
        # ----------------------------------------------

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ Request timed out.\n\n"
                "The Gemini API is taking too long "
                "to respond."
            )


        # ----------------------------------------------
        # OTHER REQUEST ERROR
        # ----------------------------------------------

        except requests.exceptions.RequestException as e:

            st.error(
                f"❌ Request error: {str(e)}"
            )


# ==================================================
# GENERATED DOCUMENT SECTION
# ==================================================

if "document" in st.session_state:

    st.divider()

    st.subheader("📄 Generated Document")


    # ----------------------------------------------
    # PREVIEW / EDIT
    # ----------------------------------------------

    edited_document = st.text_area(
        "Preview & Edit",
        value=st.session_state["document"],
        height=500
    )


    # Save edited document
    st.session_state["document"] = edited_document


    # ----------------------------------------------
    # TXT DOWNLOAD
    # ----------------------------------------------

    st.download_button(
        label="⬇️ Download TXT",
        data=edited_document,
        file_name="legal_document.txt",
        mime="text/plain"
    )


    # ----------------------------------------------
    # DOCX DOWNLOAD
    # ----------------------------------------------

    try:

        docx_data = format_docx(
            edited_document
        )

        st.download_button(
            label="⬇️ Download DOCX",
            data=docx_data,
            file_name="legal_document.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            )
        )

    except Exception as e:

        st.error(
            f"❌ DOCX generation error: {str(e)}"
        )


    # ----------------------------------------------
    # PDF DOWNLOAD
    # ----------------------------------------------

    try:

        pdf_data = format_pdf(
            edited_document
        )

        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_data,
            file_name="legal_document.pdf",
            mime="application/pdf"
        )

    except Exception as e:

        st.error(
            f"❌ PDF generation error: {str(e)}"
        )