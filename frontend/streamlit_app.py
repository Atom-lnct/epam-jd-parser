import streamlit as st
import requests

st.set_page_config(page_title="JD Parser")
st.title("JD Parser")

BACKEND_URL = "http://localhost:8000/parse-jd"

uploaded_file = st.file_uploader("Upload a Job Description PDF", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Processing..."):
        try:
            response = requests.post(
                BACKEND_URL,
                files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
                timeout=180,
            )
            if response.status_code == 200:
                result = response.json()
                st.subheader("Parsed JD")
                st.json(result["data"])
                if result.get("db_error"):
                    st.warning(f"MongoDB storage failed: {result['db_error']}")
                else:
                    st.success("Saved to MongoDB.")
            else:
                error = response.json().get("detail", "Unknown error occurred.")
                st.error(f"Error: {error}")
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the backend. Make sure the FastAPI server is running.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

