import streamlit as st
import json
from classifier import classify_po

st.set_page_config(page_title="PO Category Classifier", layout="centered")

st.title("PO L1-L2-L3 Classifier")
st.caption("Classify purchase order descriptions into a clean L1/L2/L3 taxonomy.")

left_col, right_col = st.columns([3, 2], gap="large")

if "classification_result" not in st.session_state:
    st.session_state.classification_result = None

with left_col:
    with st.form("po_form"):
        input_col, supplier_col = st.columns([3, 2], gap="medium")
        with input_col:
            po_description = st.text_area(
                "PO Description",
                height=180,
                placeholder="e.g., Annual license renewal for endpoint security software",
                help="Add the main item or service. The more specific the better.",
            )
        with supplier_col:
            supplier = st.text_input(
                "Supplier (optional)",
                placeholder="e.g., CrowdStrike",
                help="If known, the supplier can improve classification accuracy.",
            )

        submit_col, clear_col = st.columns([1, 1], gap="small")
        with submit_col:
            submitted = st.form_submit_button("Classify")
        with clear_col:
            clear_clicked = st.form_submit_button("Clear Result")

with right_col:
    st.subheader("Tips")
    st.write(
        "- Include quantities or units when relevant.\n"
        "- Mention subscription vs. one-time purchases.\n"
        "- Add product family or model if known."
    )
    st.subheader("Example")
    st.code(
        "50 seats of HRIS platform annual subscription, renewals included",
        language="text",
    )

if submitted:
    if not po_description.strip():
        st.warning("Please enter a PO description.")
    else:
        with st.spinner("Classifying..."):
            result = classify_po(po_description, supplier)

        try:
            st.session_state.classification_result = json.loads(result)
            st.success("Classification complete")
        except Exception:
            st.session_state.classification_result = {"raw_response": result}
            st.error("Invalid model response")

if clear_clicked:
    st.session_state.classification_result = None

if st.session_state.classification_result is not None:
    if "raw_response" in st.session_state.classification_result:
        st.code(st.session_state.classification_result["raw_response"], language="json")
    else:
        st.json(st.session_state.classification_result)
        st.download_button(
            "Download JSON",
            data=json.dumps(st.session_state.classification_result, indent=2),
            file_name="po_classification.json",
            mime="application/json",
        )
