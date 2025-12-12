import streamlit as st
import requests

API_BASE = st.secrets.get("API_BASE", "http://127.0.0.1:5000")

st.set_page_config(page_title="AI Feedback System", layout="wide")

st.title("🟢 User Feedback")

rating = st.slider("Rate your experience", 1, 5, 5)
review = st.text_area("Write your review")

if st.button("Submit"):
    if not review.strip():
        st.warning("Please write a review before submitting.")
    else:
        try:
            with st.spinner("Sending your feedback..."):
                res = requests.post(
                    f"{API_BASE}/api/feedback",
                    json={"rating": rating, "review": review},
                    timeout=20,
                )

            if res.ok:
                data = res.json()
                st.success("✅ Feedback submitted!")

                st.subheader("🤖 AI Response")
                st.info(data.get("ai_response", "No response from AI."))

            else:
                st.error("Server error occurred.")
                st.write(res.text)

        except Exception as e:
            st.error("Backend unreachable.")
            st.exception(e)
